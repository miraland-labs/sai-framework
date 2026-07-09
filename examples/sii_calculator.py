#!/usr/bin/env python3
"""
SAI Framework — Reference SII Calculator (v0.2.1)

Informative reference implementation of X, Y, Z, and SII per SPEC.md.
Python standard library only — no third-party dependencies.

Usage:
    python3 examples/sii_calculator.py
    python3 examples/sii_calculator.py --json
    python3 examples/sii_calculator.py --self-test
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass, field
from enum import Enum


SPEC_VERSION = "0.2.1"


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

# Min expected raw scores on 0–100 percent scale (MT-Bench handled separately)
BENCHMARK_MIN: dict[str, float] = {
    "mmlu_pro": 25.0,
    "gpqa_diamond": 25.0,
    "math_500": 0.0,
    "aime": 0.0,
    "humaneval_plus": 0.0,
    "swe_bench": 0.0,
    "livecodebench": 0.0,
    "ifeval": 0.0,
    "mt_bench": 0.0,
}

MAX_EXPECTED = 100.0
MT_BENCH_MAX = 10.0
MIN_COVERAGE = 0.70

# Provisional baseline constants (SPEC §3.1.4) until baseline dataset is published
BASELINE_MODEL_ID = "gpt-3.5-turbo-0125"
BASELINE_Y_SCORE = 55.0

# Published score rounding (SPEC §4.4)
ROUND_Y = 2
ROUND_X = 4
ROUND_Z = 6
ROUND_SII = 2


@dataclass
class BenchmarkResult:
    """Raw benchmark score on native scale (percent, or 0–10 for MT-Bench)."""

    name: str
    raw_score: float
    is_mt_bench: bool = False


@dataclass
class TokenData:
    """Token consumption for X dimension (suite-level totals)."""

    total_tokens: int
    baseline_tokens: int
    baseline_y_score: float = BASELINE_Y_SCORE


@dataclass
class EnergyData:
    """
    Energy for the same evaluation workload that produced Y (suite-level).

    For Tier 2, estimate suite energy as:
        total_energy_joules = suite_tokens × energy_per_token
    where energy_per_token comes from a cited probe or published benchmark.
    """

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
    spec_version: str = SPEC_VERSION
    sii_band: str = ""


def validate_workload_weights() -> None:
    """Raise if any workload category weights do not sum to 1.0."""
    for category, weights in WORKLOAD_WEIGHTS.items():
        total = sum(weights.values())
        if not math.isclose(total, 1.0, abs_tol=1e-9):
            raise ValueError(f"{category.value} weights sum to {total}, expected 1.0")


def normalize_score(raw: float, min_expected: float, max_expected: float = MAX_EXPECTED) -> float:
    """Normalize a raw percent score to 0–100. Clamps to [0, 100]."""
    if max_expected <= min_expected:
        raise ValueError("max_expected must be greater than min_expected")
    normalized = ((raw - min_expected) / (max_expected - min_expected)) * 100.0
    return max(0.0, min(100.0, normalized))


def normalize_mt_bench(raw_score: float) -> float:
    """Convert MT-Bench 0–10 judge score to 0–100."""
    return max(0.0, min(100.0, (raw_score / MT_BENCH_MAX) * 100.0))


def calculate_y(
    results: list[BenchmarkResult],
    workload: WorkloadCategory = WorkloadCategory.GENERAL,
) -> tuple[float, float, dict[str, float]]:
    """
    Calculate Y (0–100), coverage fraction, and per-benchmark normalized scores.

    Partial coverage (SPEC §3.2.3):
        Y = Σ(w_i × n_i) / Σ(w_i for available)
    where w_i are weight fractions and n_i are normalized scores on 0–100.
    """
    weights = WORKLOAD_WEIGHTS[workload]
    normalized: dict[str, float] = {}

    for result in results:
        if result.name not in weights:
            continue
        if result.is_mt_bench or result.name == "mt_bench":
            normalized[result.name] = normalize_mt_bench(result.raw_score)
        else:
            min_expected = BENCHMARK_MIN.get(result.name, 0.0)
            normalized[result.name] = normalize_score(result.raw_score, min_expected)

    available_weight = sum(weights[name] for name in normalized)
    if available_weight == 0:
        raise ValueError("No benchmark results match the selected workload category")

    if available_weight < MIN_COVERAGE:
        raise ValueError(
            f"Insufficient benchmark coverage: {available_weight:.0%} "
            f"(minimum {MIN_COVERAGE:.0%} required for SAI-Basic)"
        )

    weighted_sum = sum(weights[name] * normalized[name] for name in normalized)
    y_score = weighted_sum / available_weight

    return y_score, available_weight, normalized


def calculate_x_norm(
    total_tokens: int,
    baseline_tokens: int,
    y_score: float,
    baseline_y_score: float = BASELINE_Y_SCORE,
) -> float:
    """
    X_raw = Total_Tokens / (Y / 100)
    X_baseline = Baseline_Tokens / (Baseline_Y / 100)
    X_norm = X_raw / X_baseline
    """
    if y_score <= 0:
        raise ValueError("Y score must be > 0 for X calculation (failed suite)")
    if baseline_y_score <= 0:
        raise ValueError("Baseline Y score must be > 0")
    if total_tokens <= 0 or baseline_tokens <= 0:
        raise ValueError("Token counts must be > 0")

    x_raw = total_tokens / (y_score / 100.0)
    x_baseline = baseline_tokens / (baseline_y_score / 100.0)
    return x_raw / x_baseline


def calculate_z(y_score: float, energy: EnergyData) -> float:
    """Z = Y / (Total_Energy_Joules × PUE). Unit: IP/J."""
    if y_score < 0:
        raise ValueError("Y score must be >= 0")
    total_with_pue = energy.total_energy_joules * energy.pue
    if total_with_pue <= 0:
        raise ValueError("Total energy with PUE must be > 0")
    return y_score / total_with_pue


def calculate_sii(y_score: float, z_score: float, x_norm: float) -> float:
    """SII = (Y × Z) / X_norm × 100."""
    if x_norm <= 0:
        raise ValueError("X_norm must be > 0")
    return (y_score * z_score) / x_norm * 100.0


def sii_band(sii: float) -> str:
    """Provisional interpretation bands (SPEC §4.3)."""
    if sii > 40:
        return "exceptional"
    if sii >= 25:
        return "excellent"
    if sii >= 15:
        return "good"
    if sii >= 8:
        return "moderate"
    return "poor"


def evaluate(
    results: list[BenchmarkResult],
    tokens: TokenData,
    energy: EnergyData,
    workload: WorkloadCategory = WorkloadCategory.GENERAL,
) -> SAIResult:
    """Run full SAI evaluation. Uses computed Y for X and Z (not a caller-supplied Y)."""
    y_score, coverage, normalized = calculate_y(results, workload)
    x_norm = calculate_x_norm(
        tokens.total_tokens,
        tokens.baseline_tokens,
        y_score,
        tokens.baseline_y_score,
    )
    z_score = calculate_z(y_score, energy)
    sii = calculate_sii(y_score, z_score, x_norm)

    return SAIResult(
        y_score=round(y_score, ROUND_Y),
        x_norm=round(x_norm, ROUND_X),
        z_score=round(z_score, ROUND_Z),
        sii=round(sii, ROUND_SII),
        coverage=round(coverage, 4),
        normalized_scores={k: round(v, ROUND_Y) for k, v in normalized.items()},
        workload=workload.value,
        spec_version=SPEC_VERSION,
        sii_band=sii_band(sii),
    )


def llama_31_8b_example() -> SAIResult:
    """Worked example from SPEC.md §4.2 (Llama-3.1-8B-Instruct, General)."""
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
        baseline_y_score=BASELINE_Y_SCORE,
    )
    energy = EnergyData(total_energy_joules=12_500, pue=1.3)
    return evaluate(results, tokens, energy, WorkloadCategory.GENERAL)


def run_self_tests() -> None:
    """Lightweight conformance checks for the reference formulas."""
    validate_workload_weights()

    # Normalization
    assert abs(normalize_score(70.0, 25.0) - 60.0) < 1e-9
    assert abs(normalize_score(65.0, 0.0) - 65.0) < 1e-9
    assert abs(normalize_mt_bench(7.8) - 78.0) < 1e-9
    assert normalize_score(10.0, 25.0) == 0.0  # below random → clamp

    # Full-coverage Y for worked example
    result = llama_31_8b_example()
    assert result.y_score == 50.87, result.y_score
    assert result.x_norm == 1.3065, result.x_norm
    assert result.z_score == 0.00313, result.z_score
    assert result.sii == 12.19, result.sii
    assert result.coverage == 1.0
    assert result.sii_band == "moderate"

    # Partial coverage: omit aime (5%) + livecodebench (5%) → 90%
    partial = [
        BenchmarkResult("mmlu_pro", 68.0),
        BenchmarkResult("gpqa_diamond", 42.0),
        BenchmarkResult("math_500", 55.0),
        BenchmarkResult("humaneval_plus", 70.0),
        BenchmarkResult("swe_bench", 28.0),
        BenchmarkResult("ifeval", 82.0),
        BenchmarkResult("mt_bench", 7.8, is_mt_bench=True),
    ]
    y, cov, _ = calculate_y(partial, WorkloadCategory.GENERAL)
    assert abs(cov - 0.90) < 1e-9, cov
    # Y = weighted_sum / 0.90 (no extra ×100)
    assert 50.0 < y < 60.0, y

    # Coverage below 70% must fail
    thin = [BenchmarkResult("mmlu_pro", 68.0), BenchmarkResult("ifeval", 82.0)]
    try:
        calculate_y(thin, WorkloadCategory.GENERAL)
        raise AssertionError("expected coverage error")
    except ValueError as exc:
        assert "coverage" in str(exc).lower()

    # Coding workload weights usable
    coding = [
        BenchmarkResult("humaneval_plus", 70.0),
        BenchmarkResult("swe_bench", 28.0),
        BenchmarkResult("livecodebench", 32.0),
        BenchmarkResult("mmlu_pro", 68.0),
        BenchmarkResult("ifeval", 82.0),
    ]
    y_c, cov_c, _ = calculate_y(coding, WorkloadCategory.CODING)
    assert cov_c == 1.0
    assert 0 < y_c <= 100

    print("All self-tests passed.")


def print_result(result: SAIResult) -> None:
    print(f"\n{'=' * 50}")
    print(f"SAI Framework Evaluation Result (v{result.spec_version})")
    print(f"{'=' * 50}")
    print(f"Workload:     {result.workload}")
    print(f"Coverage:     {result.coverage:.0%}")
    print("\nNormalized benchmark scores:")
    for name, score in sorted(result.normalized_scores.items()):
        print(f"  {name:20s} {score:6.1f}")
    print(f"\nY (Intelligence):          {result.y_score:.2f}")
    print(f"X_norm (Token Efficiency): {result.x_norm:.4f}")
    print(f"Z (IP/J):                  {result.z_score:.6f}")
    print(f"SII:                       {result.sii:.2f} ({result.sii_band})")
    print(f"{'=' * 50}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=f"SAI Framework SII Calculator (v{SPEC_VERSION})")
    parser.add_argument("--json", action="store_true", help="Output result as JSON")
    parser.add_argument(
        "--example",
        choices=["llama-3.1-8b"],
        default="llama-3.1-8b",
        help="Built-in worked example (default: llama-3.1-8b)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run reference formula self-tests and exit",
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_tests()
        return

    validate_workload_weights()

    if args.example == "llama-3.1-8b":
        result = llama_31_8b_example()
    else:
        raise ValueError(f"Unknown example: {args.example}")

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        print_result(result)


if __name__ == "__main__":
    try:
        main()
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        sys.exit(1)
