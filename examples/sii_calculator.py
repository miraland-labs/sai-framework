#!/usr/bin/env python3
"""
SAI Framework — Reference SII Calculator (v0.2)

Implements X (Token Efficiency), Y (Intelligence), Z (Energy Sustainability),
and SII (Sustainable Intelligence Index) per SPEC.md v0.2.

Usage:
    python examples/sii_calculator.py          # Run built-in worked example
    python examples/sii_calculator.py --help     # Show CLI options
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Optional


class WorkloadCategory(str, Enum):
    GENERAL = "general"
    CODING = "coding"
    SCIENTIFIC = "scientific"
    AGENTIC = "agentic"


# Benchmark weights per workload category (must sum to 1.0)
WORKLOAD_WEIGHTS: dict[WorkloadCategory, dict[str, float]] = {
    WorkloadCategory.GENERAL: {
        "mmlu_pro": 0.20,
        "gpqa_diamond": 0.15,
        "math_500": 0.15,
        "aime": 0.05,
        "humaneval_plus": 0.15,
        "swe_bench": 0.10,
        "livecodebench": 0.05,
        "ifeval": 0.10,
        "mt_bench": 0.05,
    },
    WorkloadCategory.CODING: {
        "humaneval_plus": 0.30,
        "swe_bench": 0.35,
        "livecodebench": 0.20,
        "mmlu_pro": 0.10,
        "ifeval": 0.05,
    },
    WorkloadCategory.SCIENTIFIC: {
        "math_500": 0.40,
        "aime": 0.20,
        "gpqa_diamond": 0.25,
        "mmlu_pro": 0.10,
        "ifeval": 0.05,
    },
    WorkloadCategory.AGENTIC: {
        "ifeval": 0.25,
        "mt_bench": 0.25,
        "swe_bench": 0.20,
        "humaneval_plus": 0.15,
        "mmlu_pro": 0.15,
    },
}

# Minimum expected scores for normalization (percent scale unless noted)
BENCHMARK_BASELINES: dict[str, float] = {
    "mmlu_pro": 25.0,
    "gpqa_diamond": 25.0,
    "math_500": 0.0,
    "aime": 0.0,
    "humaneval_plus": 0.0,
    "swe_bench": 0.0,
    "livecodebench": 0.0,
    "ifeval": 0.0,
    "mt_bench": 0.0,  # raw score 0-10, handled separately
}

MAX_EXPECTED = 100.0
MT_BENCH_MAX = 10.0
MIN_COVERAGE = 0.70


@dataclass
class BenchmarkResult:
    """Raw benchmark score on native scale."""

    name: str
    raw_score: float
    is_mt_bench: bool = False


@dataclass
class TokenData:
    """Token consumption for X dimension."""

    total_tokens: int
    baseline_tokens: int
    y_score: float  # Model Y on 0-100 scale
    baseline_y_score: float = 55.0  # GPT-3.5-turbo reference Y


@dataclass
class EnergyData:
    """Energy measurement for Z dimension."""

    total_energy_joules: float
    pue: float = 1.3


@dataclass
class SAIResult:
    """Complete SAI evaluation output."""

    y_score: float
    x_norm: float
    z_score: float
    sii: float
    coverage: float
    normalized_scores: dict[str, float] = field(default_factory=dict)
    workload: str = "general"


def normalize_score(raw: float, min_expected: float, max_expected: float = MAX_EXPECTED) -> float:
    """Normalize a raw benchmark score to 0-100 scale."""
    if max_expected <= min_expected:
        raise ValueError("max_expected must be greater than min_expected")
    normalized = ((raw - min_expected) / (max_expected - min_expected)) * 100.0
    return max(0.0, min(100.0, normalized))


def normalize_mt_bench(raw_score: float) -> float:
    """Convert MT-Bench 0-10 judge score to 0-100 normalized scale."""
    return max(0.0, min(100.0, (raw_score / MT_BENCH_MAX) * 100.0))


def calculate_y(
    results: list[BenchmarkResult],
    workload: WorkloadCategory = WorkloadCategory.GENERAL,
) -> tuple[float, float, dict[str, float]]:
    """
    Calculate Y (Intelligence score), coverage fraction, and per-benchmark normalized scores.

    Returns:
        (y_score, coverage, normalized_scores)
    """
    weights = WORKLOAD_WEIGHTS[workload]
    normalized: dict[str, float] = {}

    for result in results:
        if result.name not in weights:
            continue
        if result.is_mt_bench:
            normalized[result.name] = normalize_mt_bench(result.raw_score)
        else:
            baseline = BENCHMARK_BASELINES.get(result.name, 0.0)
            normalized[result.name] = normalize_score(result.raw_score, baseline)

    available_weight = sum(weights[name] for name in normalized)
    if available_weight == 0:
        raise ValueError("No benchmark results match the selected workload category")

    coverage = available_weight  # weights already sum to 1.0 for full suite
    if coverage < MIN_COVERAGE:
        raise ValueError(
            f"Insufficient benchmark coverage: {coverage:.0%} "
            f"(minimum {MIN_COVERAGE:.0%} required for SAI-Basic)"
        )

    weighted_sum = sum(weights[name] * normalized[name] for name in normalized)
    y_score = weighted_sum / available_weight if available_weight < 1.0 else weighted_sum

    return y_score, coverage, normalized


def calculate_x_norm(tokens: TokenData) -> float:
    """
    Calculate normalized token efficiency (X_norm).

    X_raw = total_tokens / (y_score / 100)
    X_baseline = baseline_tokens / (baseline_y / 100)
    X_norm = X_raw / X_baseline
    """
    if tokens.y_score <= 0:
        raise ValueError("Y score must be > 0 for X calculation")
    if tokens.baseline_y_score <= 0:
        raise ValueError("Baseline Y score must be > 0")

    x_raw = tokens.total_tokens / (tokens.y_score / 100.0)
    x_baseline = tokens.baseline_tokens / (tokens.baseline_y_score / 100.0)
    if x_baseline <= 0:
        raise ValueError("Baseline tokens must be > 0")

    return x_raw / x_baseline


def calculate_z(y_score: float, energy: EnergyData) -> float:
    """Calculate Z (Intelligence Points per Joule)."""
    total_with_pue = energy.total_energy_joules * energy.pue
    if total_with_pue <= 0:
        raise ValueError("Total energy must be > 0")
    return y_score / total_with_pue


def calculate_sii(y_score: float, z_score: float, x_norm: float) -> float:
    """Calculate Sustainable Intelligence Index."""
    if x_norm <= 0:
        raise ValueError("X_norm must be > 0")
    return (y_score * z_score) / x_norm * 100.0


def evaluate(
    results: list[BenchmarkResult],
    tokens: TokenData,
    energy: EnergyData,
    workload: WorkloadCategory = WorkloadCategory.GENERAL,
) -> SAIResult:
    """Run full SAI evaluation pipeline."""
    y_score, coverage, normalized = calculate_y(results, workload)
    x_norm = calculate_x_norm(tokens)
    z_score = calculate_z(y_score, energy)
    sii = calculate_sii(y_score, z_score, x_norm)

    return SAIResult(
        y_score=round(y_score, 2),
        x_norm=round(x_norm, 4),
        z_score=round(z_score, 6),
        sii=round(sii, 2),
        coverage=round(coverage, 4),
        normalized_scores={k: round(v, 2) for k, v in normalized.items()},
        workload=workload.value,
    )


def llama_31_8b_example() -> SAIResult:
    """Worked example from SPEC.md Section 4.2 (Llama-3.1-8B-Instruct)."""
    results = [
        BenchmarkResult("mmlu_pro", 68.0),
        BenchmarkResult("gpqa_diamond", 42.0),
        BenchmarkResult("math_500", 55.0),
        BenchmarkResult("aime", 15.0),
        BenchmarkResult("humaneval_plus", 70.0),
        BenchmarkResult("swe_bench", 28.0),
        BenchmarkResult("livecodebench", 32.0),
        BenchmarkResult("ifeval", 82.0),
        BenchmarkResult("mt_bench", 7.8, is_mt_bench=True),
    ]
    tokens = TokenData(
        total_tokens=145_000,
        baseline_tokens=120_000,
        y_score=50.87,
        baseline_y_score=55.0,
    )
    energy = EnergyData(total_energy_joules=12_500, pue=1.3)
    return evaluate(results, tokens, energy, WorkloadCategory.GENERAL)


def print_result(result: SAIResult) -> None:
    """Pretty-print evaluation result."""
    print(f"\n{'='*50}")
    print("SAI Framework Evaluation Result (v0.2)")
    print(f"{'='*50}")
    print(f"Workload:     {result.workload}")
    print(f"Coverage:     {result.coverage:.0%}")
    print(f"\nNormalized benchmark scores:")
    for name, score in sorted(result.normalized_scores.items()):
        print(f"  {name:20s} {score:6.1f}")
    print(f"\nY (Intelligence):        {result.y_score:.2f}")
    print(f"X_norm (Token Efficiency): {result.x_norm:.4f}")
    print(f"Z (IP/J):                {result.z_score:.6f}")
    print(f"SII:                     {result.sii:.2f}")
    print(f"{'='*50}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="SAI Framework SII Calculator (v0.2)")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON",
    )
    parser.add_argument(
        "--example",
        choices=["llama-3.1-8b"],
        default="llama-3.1-8b",
        help="Run built-in worked example (default: llama-3.1-8b)",
    )
    args = parser.parse_args()

    if args.example == "llama-3.1-8b":
        result = llama_31_8b_example()
    else:
        raise ValueError(f"Unknown example: {args.example}")

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print_result(result)


if __name__ == "__main__":
    main()
