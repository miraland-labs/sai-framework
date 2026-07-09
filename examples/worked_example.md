# Worked Example: Llama-3.1-8B-Instruct SAI Evaluation

**SAI Framework v0.2.1**  
**Model:** meta-llama/Llama-3.1-8B-Instruct  
**Workload:** General / Reasoning  
**Date:** July 2026  
**Status:** Informative example (illustrative scores)

This walkthrough mirrors [SPEC.md](../SPEC.md) §4.2. Published scores use §4.4 rounding; the reference calculator is authoritative.

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
measurement_tier: 1
energy_scope: suite  # Total_Energy is for the full benchmark suite
```

## Step 1: Benchmark Suite

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

**Coverage:** 100% (General category)

### Token Consumption (suite)

```
Input tokens:     98,400
Output tokens:    46,600
Total tokens:    145,000
```

## Step 2: Y (Intelligence)

| Benchmark | Raw | Min | Normalized |
|-----------|-----|-----|------------|
| MMLU-Pro | 68.0 | 25 | 57.33 |
| GPQA Diamond | 42.0 | 25 | 22.67 |
| MATH-500 | 55.0 | 0 | 55.00 |
| AIME | 15.0 | 0 | 15.00 |
| HumanEval+ | 70.0 | 0 | 70.00 |
| SWE-Bench | 28.0 | 0 | 28.00 |
| LiveCodeBench | 32.0 | 0 | 32.00 |
| IFEval | 82.0 | 0 | 82.00 |
| MT-Bench | 7.8 | 0 | 78.00 |

```
Y = Σ(w_i × n_i) / Σ(w_i) = 50.8666… → published 50.87
```

## Step 3: X_norm

Baseline: `gpt-3.5-turbo-0125`, Baseline_Y = 55.0, Baseline_Tokens = 120,000

```
X_raw      = 145000 / (Y/100) = 285,059.21…
X_baseline = 120000 / 0.55    = 218,181.81…
X_norm     = 1.3065 (published)
```

Interpretation: ~30.7% more tokens than baseline per intelligence unit.

## Step 4: Z (suite energy)

```
Suite energy (Tier 1): 12,500 J
PUE (default-cloud):   1.3
Total with PUE:        16,250 J

Z = Y / 16250 = 0.003130 IP/J
```

Phase breakdown (SAI-Full energy reporting):
- Prefill: 3,200 J
- Decode: 9,300 J

## Step 5: SII

```
SII = (Y × Z) / X_norm × 100 = 12.19 (moderate)
```

## Verify

```bash
python3 examples/sii_calculator.py
python3 examples/sii_calculator.py --self-test
```

Expected:

```
Y (Intelligence):          50.87
X_norm (Token Efficiency): 1.3065
Z (IP/J):                  0.003130
SII:                       12.19 (moderate)
```

## Conformance Note

This single-category example satisfies **SAI-Basic** requirements for coverage and Tier 1 energy. **SAI-Full** additionally requires a second workload category (e.g., Coding) with its own Y/SII — not shown here.

| Requirement | This example |
|-------------|--------------|
| ≥70% coverage | ✅ 100% General |
| Energy Tier 1 | ✅ NVML / suite energy |
| Environment + inference disclosure | ✅ |
| Statistical CI | ✅ (illustrative) |
| Phase-aware energy | ✅ |
| Second workload category | ❌ (needed for SAI-Full) |

**Eligible designation for this report alone:** SAI-Basic v0.2.1 (General)

## Optional Carbon

```
16,250 J = 0.004514 kWh
× 400 gCO2/kWh → ≈ 1.81 gCO2
```

## Report Export

Fill [schemas/evaluation_report.yaml](../schemas/evaluation_report.yaml). See [CONFORMANCE.md](../CONFORMANCE.md).
