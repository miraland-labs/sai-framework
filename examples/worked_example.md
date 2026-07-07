# Worked Example: Llama-3.1-8B-Instruct SAI Evaluation

**SAI Framework v0.2**  
**Model:** meta-llama/Llama-3.1-8B-Instruct  
**Workload:** General / Reasoning  
**Date:** July 2026

This document walks through a complete SAI evaluation from benchmark execution to final SII score. It mirrors [SPEC.md](../SPEC.md) Section 4.2 with additional reporting detail.

## Evaluation Setup

```yaml
model:
  id: meta-llama/Llama-3.1-8B-Instruct
  revision: main
  format: FP16

environment:
  gpu: NVIDIA A100 80GB
  inference_framework: vLLM v0.4.2
  location: us-west-2 (AWS)

inference_config:
  temperature: 0.0
  max_tokens: 2048
  seed: 42
  batch_size: 1

workload: general
measurement_tier: 1  # Hardware energy measurement
```

## Step 1: Run Benchmark Suite

Execute all nine mandatory benchmarks per [BENCHMARK_GUIDE.md](../BENCHMARK_GUIDE.md).

### Raw Results

| Benchmark | Raw Score | Metric |
|-----------|-----------|--------|
| MMLU-Pro | 68.0% | Accuracy |
| GPQA Diamond | 42.0% | Accuracy |
| MATH-500 | 55.0% | Pass@1 |
| AIME | 15.0% | Pass@1 |
| HumanEval+ | 70.0% | Pass@1 |
| SWE-Bench Verified | 28.0% | Resolved |
| LiveCodeBench | 32.0% | Pass@1 |
| IFEval | 82.0% | Strict accuracy |
| MT-Bench | 7.8/10 | GPT-4o judge |

**Coverage:** 100% (all benchmarks present)

### Token Consumption

Total tokens across the full benchmark suite:

```
Input tokens:     98,400
Output tokens:    46,600
Total tokens:    145,000
```

## Step 2: Calculate Y (Intelligence)

### Normalization

Apply the formula from SPEC.md Section 3.2.2:

```
Normalized = ((Raw - Min) / (Max - Min)) × 100
```

| Benchmark | Raw | Min | Normalized |
|-----------|-----|-----|------------|
| MMLU-Pro | 68.0 | 25 | 57.3 |
| GPQA Diamond | 42.0 | 25 | 22.7 |
| MATH-500 | 55.0 | 0 | 55.0 |
| AIME | 15.0 | 0 | 15.0 |
| HumanEval+ | 70.0 | 0 | 70.0 |
| SWE-Bench | 28.0 | 0 | 28.0 |
| LiveCodeBench | 32.0 | 0 | 32.0 |
| IFEval | 82.0 | 0 | 82.0 |
| MT-Bench | 7.8 | 0 | 78.0 |

### Weighted Aggregation (General workload)

```
Y = (20% × 57.3) + (15% × 22.7) + (15% × 55.0) + (5% × 15.0)
  + (15% × 70.0) + (10% × 28.0) + (5% × 32.0) + (10% × 82.0) + (5% × 78.0)

Y = 11.46 + 3.41 + 8.25 + 0.75 + 10.5 + 2.8 + 1.6 + 8.2 + 3.9
Y = 50.87
```

**Result: Y = 50.87 ± 1.2 (95% CI)**

## Step 3: Calculate X_norm (Token Efficiency)

Using GPT-3.5-turbo (Jan 2024) as baseline:

```
X_raw = Total_Tokens / (Y / 100)
      = 145,000 / 0.5087
      = 285,051 tokens per intelligence unit

X_baseline = Baseline_Tokens / (Baseline_Y / 100)
           = 120,000 / 0.55
           = 218,182 tokens per intelligence unit

X_norm = X_raw / X_baseline = 285,051 / 218,182 = 1.31
```

**Interpretation:** Llama-3.1-8B uses 31% more tokens than the GPT-3.5 baseline for equivalent intelligence output.

**Result: X_norm = 1.31 ± 0.05**

## Step 4: Calculate Z (Energy Efficiency)

Tier 1 hardware measurement (NVML, 100 runs, 2048 input / 512 output):

```
Measured energy (benchmark suite): 12,500 J
PUE (cloud deployment):            1.3
Total energy with PUE:             12,500 × 1.3 = 16,250 J

Z = Y / Total_Energy_with_PUE
  = 50.87 / 16,250
  = 0.00313 IP/J (Intelligence Points per Joule)
```

Phase breakdown (SAI-Full):
- Prefill: 3,200 J (26%)
- Decode: 9,300 J (74%)

**Result: Z = 0.00313 ± 0.00008 IP/J**

## Step 5: Calculate SII

```
SII = (Y × Z) / X_norm × 100
    = (50.87 × 0.00313) / 1.31 × 100
    = 0.1592 / 1.31 × 100
    = 12.15
```

**Result: SII = 12.15 ± 0.4**

### Interpretation

Per SPEC.md Section 4.3, SII = 12.15 falls in the **Moderate** range (8–15). The model delivers reasonable intelligence but is less token-efficient than baseline and deployed on cloud infrastructure with standard PUE overhead.

## Verify with Reference Code

```bash
python examples/sii_calculator.py
```

Expected output:

```
Y (Intelligence):          50.87
X_norm (Token Efficiency): 1.3064
Z (IP/J):                  0.003130
SII:                       12.19
```

Values may differ slightly from hand-calculated rounding in Step 2–5 above; the reference implementation uses full-precision normalization.

JSON output:

```bash
python examples/sii_calculator.py --json
```

## Conformance Assessment

| Requirement | Status |
|-------------|--------|
| ≥70% benchmark coverage | ✅ 100% |
| Energy Tier 1 (hardware) | ✅ NVML |
| Environment disclosure | ✅ Published |
| Inference config documented | ✅ temperature=0.0, seed=42 |
| Statistical reporting | ✅ CI reported |
| Phase-aware energy (Full) | ✅ Prefill/decode split |

**Designation:** SAI-Full v0.2 (General)

## Optional: Carbon Footprint

```
Energy:          16,250 J = 0.00451 kWh
Grid intensity:  400 gCO2/kWh (California, ElectricityMap)
Carbon cost:     0.00451 × 400 = 1.80 gCO2
```

## Report Export

Fill [schemas/evaluation_report.yaml](../schemas/evaluation_report.yaml) with these values for publication. See [CONFORMANCE.md](../CONFORMANCE.md) for badge eligibility.
