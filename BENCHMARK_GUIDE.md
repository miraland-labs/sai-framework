# Benchmark Execution Guide

**SAI Framework — Intelligence / Value Generation (Y Dimension)**  
**Version:** 0.2.1  
**Date:** July 2026

## Overview

This document defines how to execute, score, and report the mandatory benchmark suite for SAI v0.2 evaluations. It complements [SPEC.md](SPEC.md) Section 3.2 and [CONFORMANCE.md](CONFORMANCE.md).

All evaluators must follow these standards to produce comparable Y scores and valid SII results.

## Mandatory Benchmark Suite

| Benchmark | Version | Weight (General) | Min Baseline | Scoring Metric |
|-----------|---------|------------------|--------------|----------------|
| MMLU-Pro | 12k questions (2024) | 20% | 25% (4-choice) | Accuracy |
| GPQA Diamond | 448 questions | 15% | 25% (4-choice) | Accuracy |
| MATH-500 | Hendrycks 2021, 500 subset | 15% | 0% | Pass@1 |
| AIME | 2023–2024 problems | 5% | 0% | Pass@1 |
| HumanEval+ | v0.2.0 (164 problems) | 15% | 0% | Pass@1 |
| SWE-Bench Verified | 500-problem subset | 10% | 0% | Resolved rate |
| LiveCodeBench | Rolling 3-month window | 5% | 0% | Pass@1 |
| IFEval | v1.0 (541 prompts) | 10% | 0% | Strict instruction accuracy |
| MT-Bench | v1.0 | 5% | 0% | GPT-4 judge score / 10 |

**Minimum coverage for SAI-Basic:** ≥70% of total weight in one workload category.

## Workload Categories

Select the category that matches your deployment scenario. Each category reweights benchmarks; formulas remain the same.

### General / Reasoning (default)

Use for business analysis, writing, general QA, and research.

| Benchmark | Weight |
|-----------|--------|
| MMLU-Pro | 20% |
| GPQA Diamond | 15% |
| MATH-500 | 15% |
| AIME | 5% |
| HumanEval+ | 15% |
| SWE-Bench Verified | 10% |
| LiveCodeBench | 5% |
| IFEval | 10% |
| MT-Bench | 5% |

### Coding

Use for software development, code review, and debugging.

| Benchmark | Weight |
|-----------|--------|
| HumanEval+ | 30% |
| SWE-Bench Verified | 35% |
| LiveCodeBench | 20% |
| MMLU-Pro | 10% |
| IFEval | 5% |

### Scientific / Mathematical

Use for research, data analysis, and calculations.

| Benchmark | Weight |
|-----------|--------|
| MATH-500 | 40% |
| AIME | 20% |
| GPQA Diamond | 25% |
| MMLU-Pro | 10% |
| IFEval | 5% |

### Agentic / Tool-Use

Use for autonomous agents, multi-step tasks, and automation.

| Benchmark | Weight |
|-----------|--------|
| IFEval | 25% |
| MT-Bench | 25% |
| SWE-Bench Verified | 20% |
| HumanEval+ | 15% |
| MMLU-Pro | 15% |

## Score Normalization

For each benchmark *i*:

```
Normalized_Score_i = ((Raw_Score_i - Min_Expected) / (Max_Expected - Min_Expected)) × 100
```

Where:
- `Raw_Score_i` = model accuracy or pass rate (0–100 scale, or 0–10 for MT-Bench)
- `Min_Expected` = random or zero baseline (see table above)
- `Max_Expected` = 100% (or 10 for MT-Bench)

**MT-Bench:** Convert judge score to 0–100 before aggregation: `Normalized = (score / 10) × 100`.

**Examples:**
- MMLU-Pro at 70% → `((70 - 25) / 75) × 100 = 60.0`
- HumanEval+ at 65% → `65.0`
- MT-Bench at 7.8/10 → `78.0`

## Y Aggregation

### Full coverage

```
Y = Σ(weight_i × normalized_score_i)
```

### Partial coverage (≥70% weight required)

Same formula as full coverage — renormalize by available weight:

```
Y = Σ(weight_i × normalized_score_i) / Σ(weight_i for available benchmarks)
```

Weights are fractions (e.g., 0.20 for MMLU-Pro). Normalized scores are 0–100, so Y is 0–100. Do **not** multiply by an extra ×100 after dividing by available weight.

Report omitted benchmarks and coverage fraction.

## Execution Standards

### Inference configuration

All benchmark runs must use:

```yaml
temperature: 0.0
top_p: 1.0
top_k: -1
max_tokens: 2048
seed: 42
batch_size: 1
retry_policy: none
```

Non-deterministic models: run each problem 3 times and report the median score; document variance.

### Prompt formatting

- Use each model's official chat template (Hugging Face `apply_chat_template` or provider equivalent).
- Do not mix templates across models in the same leaderboard row.
- Document template version and tokenizer in the evaluation report.

### Few-shot settings

| Benchmark | Few-shot |
|-----------|----------|
| MMLU-Pro | 5-shot |
| MATH-500 | 4-shot (chain-of-thought optional; document if used) |
| GPQA Diamond | 0-shot |
| AIME | 0-shot |
| HumanEval+ | 0-shot |
| SWE-Bench Verified | Agent scaffold as per official harness |
| LiveCodeBench | 0-shot |
| IFEval | 0-shot |
| MT-Bench | Multi-turn (official protocol) |

### Timeouts and retries

- Per-problem timeout: **120 seconds**
- No automatic retries on failure
- Failed or timed-out problems count as incorrect

### Judge model (open-ended tasks)

For MT-Bench and any custom open-ended scoring:

```yaml
judge_model: gpt-4o-2024-05-13
judge_temperature: 0.0
judge_seed: 42
```

Document judge version in the report; re-evaluate if the judge model is deprecated.

## Per-Benchmark Notes

### MMLU-Pro

- **Source:** [TIGER-Lab/MMLU-Pro](https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro)
- Extract letter answer; exact match against gold label
- Report macro-average across subjects

### GPQA Diamond

- **Source:** [Idavidrein/gpqa](https://huggingface.co/datasets/Idavidrein/gpqa) (diamond subset)
- 448 expert-level multiple-choice questions
- 0-shot only; no retrieval augmentation unless declared as a separate evaluation track

### MATH-500

- Fixed 500-problem subset of Hendrycks MATH
- Publish subset hash or use the reference list in your reproducibility package
- Accept `\boxed{}` final-answer extraction or equivalent standardized parser

### AIME

- Use 2023 and 2024 AIME I/II problems (30 problems total if both years included)
- Integer answer exact match
- If access is restricted, document source and omit from Y (coverage drops accordingly)

### HumanEval+

- **Version:** v0.2.0 with extended unit tests
- Pass@1 with `k=1`; temperature 0.0
- Execute in sandboxed environment; report execution backend (Docker, E2B, etc.)

### SWE-Bench Verified

- Use the official 500-instance verified subset unless full Verified is explicitly declared
- Report agent framework (e.g., SWE-agent, OpenHands) if used
- Resolved = patch applied and tests pass

### LiveCodeBench (rolling)

- **Version tag:** `LiveCodeBench-YYYY-MM` (month of dataset snapshot)
- Use a contiguous 3-month window ending at evaluation date
- Always report the version tag in results; do not compare across different window tags without noting the change

### IFEval

- **Version:** v1.0 (541 prompts)
- Use strict instruction-following accuracy (all constraints satisfied)
- Report per-instruction-type breakdown when possible

### MT-Bench

- **Version:** v1.0
- Single judge: gpt-4o-2024-05-13
- Report category averages (writing, roleplay, reasoning, math, coding, extraction, STEM, humanities)

## Token Counting (X Dimension Link)

For each benchmark run, record:

```yaml
tokens:
  input: <sum of prompt tokens>
  output: <sum of completion tokens>
  reasoning: <CoT/reasoning tokens if reported separately>
  total: <input + output + reasoning>
```

Sum tokens across all benchmark problems for suite-level X calculation. See SPEC.md Section 3.1.

## Reproducibility Package

SAI-Full evaluators must publish:

1. Evaluation script or config (version-pinned dependencies)
2. Model identifier and revision hash
3. Prompt hashes (SHA-256) or full prompt files
4. Raw per-benchmark scores and normalized scores
5. Token counts per benchmark
6. Inference and judge configuration YAML

## Reporting Checklist

Before publishing Y scores:

- [ ] Workload category declared
- [ ] Benchmark versions documented
- [ ] LiveCodeBench month tag recorded (if applicable)
- [ ] Coverage ≥70% for SAI-Basic (100% for SAI-Full)
- [ ] Normalization formula applied consistently
- [ ] Partial-coverage renormalization documented
- [ ] Token totals captured for X
- [ ] Confidence intervals reported where bootstrap or multiple runs apply

## Reference Implementation

See [examples/sii_calculator.py](examples/sii_calculator.py) for programmatic Y aggregation and [examples/worked_example.md](examples/worked_example.md) for a full end-to-end walkthrough.

## References

- [SPEC.md](SPEC.md) — Core Y definitions
- [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) — Z dimension
- [schemas/evaluation_report.yaml](schemas/evaluation_report.yaml) — Report schema
- Hugging Face Open LLM Leaderboard: https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
