# SAI Framework Specification

**Sustainable AI Intelligence (SAI) Framework**  
**Version:** 0.2.1 (Draft)  
**Date:** July 2026  
**Status:** Proposed Open Standard  
**License:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

### Document Conventions

- **MUST / REQUIRED:** Normative requirements for conformant evaluations
- **SHOULD / RECOMMENDED:** Strong guidance; deviations MUST be documented
- **MAY / OPTIONAL:** Permitted alternatives
- **Informative:** Examples, ranges, and Web3 vision are non-normative unless marked otherwise

Companion documents ([BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md), [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md), [CONFORMANCE.md](CONFORMANCE.md)) are **normative** for their respective domains unless a section is labeled informative.

## 1. Abstract

The SAI Framework defines a standardized 3D evaluation system for Large Language Models (LLMs) consisting of Token Efficiency (X), Intelligence/Value Generation (Y), and Energy Sustainability (Z). It produces the **Sustainable Intelligence Index (SII)** as a primary composite metric for comparing models across performance, resource consumption, and environmental impact.

This specification provides precise mathematical definitions, measurement protocols, and reproducibility requirements to enable reliable, comparable LLM evaluation and create a bridge between AI token consumption and Web3 tokenomics.

## 2. Motivation

Current LLM evaluations are fragmented across disparate benchmarks, with inconsistent measurement methodologies and no standardized approach to resource efficiency or sustainability. SAI creates a unified standard that:

- Normalizes AI token consumption, value generation, and sustainability into comparable metrics
- Enables direct economic relationships with Web3 tokens through standardized intelligence units
- Provides actionable guidance for model selection, optimization, and procurement
- Supports transparent comparison across models, providers, and deployment configurations

## 3. Core Dimensions (3D Coordinate System)

### 3.1 X: Token Efficiency

**Definition:** The number of tokens consumed per unit of value delivered, normalized against a baseline model.

**Primary Metric:** Token Efficiency Score (dimensionless ratio)

#### 3.1.1 Calculation

```
X_raw = Total_Tokens / (Y / 100)

X_baseline = Baseline_Tokens / (Baseline_Y / 100)

X_norm = X_raw / X_baseline
```

Where:
- `Total_Tokens` = Input_Tokens + Output_Tokens + Reasoning_Tokens (if reported separately), summed over the **same evaluation suite** used for Y
- `Y` = Intelligence score from §3.2 (0–100)
- `Baseline_Tokens` = Token total for the baseline model on the same suite (§3.1.4)
- `Baseline_Y` = Baseline model Y on the same suite and workload category

**Units:** `X_raw` and `X_baseline` are tokens per intelligence unit (dimensionless Y fraction). `X_norm` is a dimensionless ratio.

**Interpretation:**
- X_norm < 1.0: More token-efficient than baseline (better)
- X_norm = 1.0: Same efficiency as baseline
- X_norm > 1.0: Less efficient than baseline (worse)

#### 3.1.2 Tokenizer Policy

Token counts MUST come from the inference provider or tokenizer used for the evaluation run (API usage metadata or local tokenizer).

**Cross-model comparisons (REQUIRED for published leaderboards):** Apply tokenizer normalization:

```
Normalized_Tokens = Actual_Tokens × (Baseline_Tokens_Per_Word / Model_Tokens_Per_Word)

Where:
- Tokens_Per_Word = Total tokens / Total words for the standard corpus
- Standard corpus: First 10,000 words of English Wikipedia (fixed dump; publish dump ID)
- Baseline tokenizer: GPT-3.5-turbo (cl100k_base)
```

**Same-tokenizer comparisons (MAY):** If all models in a comparison use identical API-reported token accounting, raw counts MAY be used without normalization. The report MUST state which policy was used.

#### 3.1.3 Edge Cases

- **Failed suite (Y = 0):** X_norm is undefined. Do not publish SII; report Y = 0 and omit X/SII, or mark evaluation as failed.
- **Chain-of-Thought / reasoning tokens:** MUST be included in Total_Tokens when the runtime reports them separately.
- **Tool use:** Include tool-invocation tokens in the prompt/completion stream; exclude tool execution payloads returned by external tools.
- **Multi-turn:** Sum all tokens across turns for the complete task or conversation under evaluation.

#### 3.1.4 Baseline Reference

**Baseline model:** `gpt-3.5-turbo-0125` (January 2024 snapshot)

**Provisional Baseline_Y (General workload):** 55.0 until the supplementary baseline dataset is published.

Illustrative per-benchmark token averages (informative; not for conformance):
- MMLU-Pro: ~1,200 tokens per problem
- HumanEval+: ~800 tokens per problem
- MATH-500: ~1,500 tokens per problem

Evaluators MUST cite the baseline token total and Baseline_Y used. When the official baseline dataset ships, those values supersede provisional constants.
### 3.2 Y: Intelligence / Value Generation

**Definition:** Composite measure of model capability and usefulness across standardized benchmarks.

**Primary Metric:** Normalized Value Score (0–100 scale)

#### 3.2.1 Mandatory Benchmark Suite (v0.2)

| Benchmark | Version | Weight | Domain |
|-----------|---------|--------|--------|
| MMLU-Pro | 12k questions (2024) | 20% | Broad Knowledge & Reasoning |
| GPQA Diamond | 448 questions | 15% | Expert-level Science |
| MATH-500 | Hendrycks 2021, 500 subset | 15% | Mathematical Reasoning |
| AIME | 2023-2024 problems | 5% | Advanced Mathematics |
| HumanEval+ | v0.2.0 (164 problems) | 15% | Code Generation |
| SWE-Bench Verified | 500 problems subset | 10% | Real-world Software Engineering |
| LiveCodeBench | Rolling 3-month window | 5% | Contemporary Coding |
| IFEval | v1.0 (541 prompts) | 10% | Instruction Following |
| MT-Bench | v1.0 | 5% | Multi-turn Conversation |

**Total Weight:** 100%

**Minimum Coverage:** At least 70% of total weight must be evaluated for SAI-Basic conformance.

#### 3.2.2 Score Normalization

For each benchmark:

```
Normalized_Score_i = ((Raw_Score_i - Min_Expected) / (Max_Expected - Min_Expected)) × 100

Where:
- Raw_Score_i = Model's raw accuracy/pass rate on benchmark i
- Min_Expected = Random baseline (e.g., 25% for 4-choice MCQ, 0% for code generation)
- Max_Expected = 100% (perfect score)
```

**Examples:**
- MMLU-Pro (4-choice): Min = 25%, Model scores 70% → Normalized = ((70-25)/(100-25)) × 100 = 60.0
- HumanEval+ (pass@1): Min = 0%, Model scores 65% → Normalized = 65.0

#### 3.2.3 Aggregation Formula

Weights are fractions that sum to 1.0 within a workload category (e.g., MMLU-Pro = 0.20). Normalized scores are on a 0–100 scale.

**Complete or partial coverage:**
```
Y = Σ(weight_i × normalized_score_i) / Σ(weight_i for available benchmarks)
```

When all benchmarks are present, `Σ(weight_i) = 1.0` and the formula reduces to a simple weighted sum.

**Coverage requirement:** Available weight MUST be ≥ 0.70 (70%) of the chosen workload category for SAI-Basic. SAI-Full requires 1.0 (100%) in the primary category.

**Reporting:** Omit unavailable benchmarks from the sum; publish the coverage fraction and the list of missing benchmarks.
#### 3.2.4 Workload-Specific Categories

Different use cases prioritize different capabilities. SAI defines four workload categories with adjusted weights:

**General/Reasoning Workload** (default weights above)
- Use case: Business analysis, writing, general QA, research

**Coding Workload**
- HumanEval+ 30%, SWE-Bench 35%, LiveCodeBench 20%, MMLU-Pro 10%, IFEval 5%
- Use case: Software development, code review, debugging

**Scientific/Mathematical Workload**
- MATH-500 40%, AIME 20%, GPQA 25%, MMLU-Pro 10%, IFEval 5%
- Use case: Research, data analysis, calculations

**Agentic/Tool-Use Workload**
- IFEval 25%, MT-Bench 25%, SWE-Bench 20%, HumanEval+ 15%, MMLU-Pro 15%
- Use case: Autonomous agents, multi-step tasks, automation

*Evaluators should select the category matching their deployment scenario.*

### 3.3 Z: Energy Sustainability

**Definition:** Intelligence value delivered per unit of energy consumed.

**Primary Metric:** Intelligence Points per Joule (IP/J)

#### 3.3.1 Calculation

```
Z = Y / Total_Energy_with_PUE

Where:
- Y = Intelligence score (0–100) from §3.2
- Total_Energy_with_PUE = Total_Energy_Joules × PUE
- PUE = Power Usage Effectiveness (data center overhead multiplier)
```

**Unit:** Intelligence Points per Joule (IP/J). Higher Z is better.

#### 3.3.2 Energy Scope (REQUIRED)

`Total_Energy_Joules` MUST be the energy attributable to the **same evaluation suite** that produced Y (all included benchmark problems), not a single probe run alone.

**Tier 1:** Prefer direct measurement over the suite. If suite-length measurement is impractical, measure a standardized probe (§3.3.3), derive energy-per-token (or per-phase rates), and scale to suite token counts / phase timings. Document the scaling method.

**Tier 2:** `Total_Energy_Joules = Suite_Tokens × Energy_per_Token`, with Energy_per_Token from a cited published source matching the model family and hardware class as closely as possible.

#### 3.3.3 Energy Measurement Tiers

**Tier 1: Hardware Measurement (Highest Confidence)**
- Direct GPU/CPU power measurement (e.g., NVML, nvidia-smi, TokenPowerBench, or equivalent)
- REQUIRED for SAI-Full
- See [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md)

**Tier 2: Token × Intensity Estimation (Medium Confidence)**
- Provider-reported suite token counts × published J/token (or equivalent intensity)
- Acceptable for SAI-Basic
- MUST cite energy intensity source and date

**Tier 3: Literature-Based Estimation (Informative Only)**
- Published totals from papers or model cards without suite-specific token accounting
- NOT sufficient for SAI-Basic or SAI-Full

#### 3.3.4 Standardized Probe Conditions (Tier 1)

When using a probe to derive intensity for suite scaling, use:

```
batch_size: 1
input_context: 2048 tokens
output_length: 512 tokens
num_runs: 100 (excluding ≥10 warmup runs)
temperature: 0.0
```

#### 3.3.5 Phase-Aware Measurement

```
Total_Energy = Prefill_Energy + Decode_Energy

Prefill_Energy = Power_prefill (W) × Time_prefill (s)
Decode_Energy  = Power_decode (W) × Time_decode (s)
```

Where `Time_decode` is the wall-clock duration of the decode phase (equivalently: Tokens_generated × Time_per_token). Do **not** multiply by both tokens and total decode time.

**SAI-Full Tier 1:** MUST report prefill and decode energy separately.
#### 3.3.6 PUE (Power Usage Effectiveness)

```
Total_Energy_with_PUE = Measured_Energy × PUE
```

Default PUE values (use measured facility PUE when available):
- Cloud providers (AWS, Azure, GCP): 1.3
- On-premises data centers: 1.5
- Consumer / local GPU: 1.0

Reports MUST document PUE and its source (`measured` | `default-cloud` | `default-onprem` | `default-local`).

#### 3.3.7 Carbon Intensity (OPTIONAL)

```
Carbon_Cost = Total_Energy_kWh × Grid_Intensity (gCO2/kWh)
Total_Energy_kWh = Total_Energy_with_PUE / 3_600_000
```

Recommended sources: ElectricityMap, EPA eGRID, IEA. Default if unspecified: 475 gCO2/kWh (2025 global average, informative).
## 4. Sustainable Intelligence Index (SII)

The SII combines all three dimensions into a single composite metric for overall model comparison.

### 4.1 Formula

```
SII = (Y × Z) / X_norm × 100

Where:
- Y: Intelligence score (0-100)
- Z: Energy efficiency (IP/J)
- X_norm: Normalized token efficiency (dimensionless)

Scaling factor: ×100 for readability (produces scores typically 10-100)
```

**Interpretation:**
- Higher SII = Better overall sustainable intelligence
- SII accounts for performance, efficiency, and sustainability simultaneously
- Models with high intelligence but poor efficiency/sustainability score lower

### 4.2 Worked Example (Informative)

**Model:** Llama-3.1-8B-Instruct · **Workload:** General/Reasoning

Numbers below use full-precision intermediates; published scores use §4.4 rounding. The reference calculator is authoritative for this example.

#### Step 1: Y (Intelligence)

| Benchmark | Raw | Normalized |
|-----------|-----|------------|
| MMLU-Pro | 68% | 57.333… |
| GPQA Diamond | 42% | 22.666… |
| MATH-500 | 55% | 55.0 |
| AIME | 15% | 15.0 |
| HumanEval+ | 70% | 70.0 |
| SWE-Bench | 28% | 28.0 |
| LiveCodeBench | 32% | 32.0 |
| IFEval | 82% | 82.0 |
| MT-Bench | 7.8/10 | 78.0 |

```
Y = 0.20×57.333… + 0.15×22.666… + 0.15×55 + 0.05×15
  + 0.15×70 + 0.10×28 + 0.05×32 + 0.10×82 + 0.05×78
Y = 50.8666… → published 50.87
```

#### Step 2: X_norm

```
Suite tokens = 145,000; Baseline tokens = 120,000; Baseline_Y = 55.0

X_raw      = 145000 / (50.8666…/100) = 285,059.21…
X_baseline = 120000 / (55/100)       = 218,181.81…
X_norm     = 1.3065 (published)
```

#### Step 3: Z

```
Suite energy = 12,500 J; PUE = 1.3 → 16,250 J
Z = 50.8666… / 16250 = 0.003130 (published)
```

#### Step 4: SII

```
SII = (50.8666… × 0.003130) / 1.3065 × 100 = 12.19 (published)
```

**Result: SII = 12.19 (moderate)** — verify with `python3 examples/sii_calculator.py`.

### 4.3 SII Interpretation Ranges (Informative / Provisional)

- **SII > 40:** Exceptional
- **SII 25–40:** Excellent
- **SII 15–25:** Good
- **SII 8–15:** Moderate
- **SII < 8:** Poor

Bands will be recalibrated as more evaluations accumulate.

### 4.4 Published Score Rounding (REQUIRED)

| Metric | Decimal places |
|--------|----------------|
| Y | 2 |
| X_norm | 4 |
| Z (IP/J) | 6 |
| SII | 2 |

Compute with full precision; round only for publication and badges.
## 5. Reproducibility Requirements

### 5.1 Evaluation Environment Disclosure

All SAI evaluations must publish:

```yaml
environment:
  hardware:
    gpu: "NVIDIA A100 80GB"
    cpu: "AMD EPYC 7763 64-Core"
    ram: "512GB DDR4-3200"
    storage: "NVMe SSD"
    location: "us-west-2 / AWS"
  software:
    inference_framework: "vLLM v0.4.2"
    model_format: "FP16 / AWQ 4-bit"
    cuda_version: "12.1"
    driver_version: "535.104.05"
    os: "Ubuntu 22.04 LTS"
  measurement:
    tool: "nvidia-smi / TokenPowerBench v1.0"
    sampling_rate: "100Hz"
    tier: 1  # Hardware measurement
```

### 5.2 Inference Configuration

```yaml
inference_config:
  temperature: 0.0  # Deterministic for reproducibility
  top_p: 1.0
  top_k: -1  # Disabled
  max_tokens: 2048
  seed: 42
  batch_size: 1
  num_beams: 1  # No beam search
  repetition_penalty: 1.0
```

### 5.3 Benchmark Execution

```yaml
benchmark_config:
  prompt_format: "model_specific"  # Follow model's chat template
  few_shot_examples: 5  # Where applicable (MMLU, MATH)
  timeout: 120  # seconds per problem
  retry_policy: "none"  # No retries on failure
  judge_model: "gpt-4o-2024-05-13"  # For open-ended evaluations
  judge_config:
    temperature: 0.0
    seed: 42
```

### 5.4 Prompt Sets

**Option A (Preferred):** Publish full prompt dataset in evaluation package

**Option B:** Publish cryptographic hashes of prompts:
```
SHA-256 hash of each prompt
Merkle tree root for entire dataset
Third-party verification available on request
```

### 5.5 Statistical Reporting

Report all measurements with confidence intervals:

```
Y: 50.87 ± 1.2 (95% CI)
Z: 0.003130 ± 0.00008 IP/J (based on 100 runs)
X_norm: 1.3065 ± 0.05
SII: 12.19 ± 0.4
```

## 6. Conformance Levels

### 6.1 SAI-Basic Conformance

**Requirements:**
1. ✅ Minimum 70% benchmark coverage by weight in one workload category
2. ✅ Energy measurement (Tier 2 or higher)
3. ✅ Published methodology document
4. ✅ Hardware and software disclosure (section 5.1)
5. ✅ Inference configuration documentation (section 5.2)
6. ✅ Results published within 60 days of evaluation
7. ✅ Statistical reporting with confidence intervals

**Designation:** Models may display "SAI-Basic Conformant" badge with version (e.g., "SAI-Basic v0.2")

### 6.2 SAI-Full Conformance

**Requirements:**
1. ✅ 100% benchmark coverage in chosen workload category
2. ✅ Energy measurement Tier 1 (hardware measurement)
3. ✅ Phase-aware energy reporting (prefill vs decode)
4. ✅ Cross-category evaluation (minimum 2 workload categories)
5. ✅ Reproducibility package (code, configs, prompt hashes)
6. ✅ Third-party verification option available
7. ✅ Public dataset or cryptographic prompt verification
8. ✅ Continuous monitoring commitment (quarterly re-evaluation recommended)

**Designation:** Models may display "SAI-Full Conformant" badge with version and categories (e.g., "SAI-Full v0.2 (General, Coding)")

### 6.3 SAI-Certified (Future - v1.0+)

**Requirements:**
1. Independent laboratory verification
2. All four workload categories evaluated
3. Carbon footprint certification
4. Audit trail with immutable logging
5. On-chain score publication (optional)
6. Annual re-certification required

**Designation:** "SAI-Certified" badge with certification date and certifying body

## 7. Bridging to Web3 Tokenomics

The SAI Framework standardizes AI LLM token consumption and normalizes it into verifiable intelligence units. This creates a direct bridge to Web3 tokenomics by enabling:

### 7.1 Tokenization of Intelligence

- **SAI Scores as NFTs:** ERC-721 tokens representing conformant evaluations
- **SII as DeFi Primitive:** Use SII scores in lending protocols, derivatives, or yield farming
- **Intelligence Futures:** Trade future model performance improvements

### 7.2 On-Chain Verification

- **Decentralized Oracles:** Chainlink or UMA-based oracle networks publish verified SII scores
- **Immutable Records:** Store evaluation hashes on Arweave or IPFS
- **Proof of Evaluation:** Cryptographic verification of methodology compliance

### 7.3 Economic Mechanisms

- **Staking on Models:** Lock tokens on high-SII models for yield
- **Green AI Rewards:** Bonus yield for models with superior Z scores
- **Model Routing:** Agents automatically select models based on SII and task requirements
- **Carbon Credits:** Convert Z improvements into verified carbon offset tokens

*Detailed Web3 integration specifications will be published in v0.3 (Q4 2026).*

## 8. Governance

### 8.1 Specification Updates

- **Minor updates** (clarifications, examples, tooling): 1-week discussion period
- **Major updates** (formula changes, benchmark modifications): 4-week discussion period + community vote
- **Breaking changes** (new version number): 8-week discussion + migration guide

### 8.2 Benchmark Evolution

- **Rolling benchmarks** (LiveCodeBench): Version controlled by month (e.g., "LiveCodeBench-2026-07")
- **Deprecated benchmarks:** 6-month transition period with dual reporting
- **New benchmarks:** Community proposal via GitHub Issues, requires implementation in reference code

### 8.3 Community Participation

- Open contribution via GitHub Issues and Pull Requests
- Monthly community calls (starting Q4 2026)
- Working groups for specialized domains (energy measurement, Web3 integration, etc.)

### 8.4 Long-term Governance

Goal: Transition to neutral foundation (Linux Foundation, IEEE, or similar) by v1.0 (2027)

## 9. References

- **TokenPowerBench:** https://github.com/foundation-model-stack/power-benchmarks
- **Hugging Face Open LLM Leaderboard:** https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
- **ML.Energy Leaderboard:** https://ml.energy/leaderboard
- **MMLU-Pro:** https://huggingface.co/datasets/TIGER-Lab/MMLU-Pro
- **SWE-Bench:** https://www.swebench.com/
- **LiveCodeBench:** https://livecodebench.github.io/

## Appendix A: Changelog

### v0.2.1 (July 2026)
- Fixed partial-coverage Y formula (removed erroneous ×100)
- Clarified X uses suite Y; tokenizer policy (required vs optional)
- Defined energy scope: suite-level energy for Z; probe-scaling rules
- Corrected decode-phase energy formula (power × time, not double-counted)
- Added published score rounding rules (§4.4)
- Aligned worked example with reference calculator (SII = 12.19)
- Added RFC-style MUST/SHOULD/MAY conventions

### v0.2 (July 2026)
- Precise X, Y, Z definitions; three-tier energy system
- GPT-3.5-turbo baseline; four workload categories
- SII ×100 scaling; conformance levels; companion guides
- Reference SII calculator and worked example

### v0.1 (July 2026)
- Initial conceptual 3D framework and SII formula

---

**For implementation guidance, see:**
- [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) - Energy measurement procedures
- [BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md) - Benchmark execution standards
- [CONFORMANCE.md](CONFORMANCE.md) - Conformance levels and self-assessment
- [examples/sii_calculator.py](examples/sii_calculator.py) - Reference implementation
- [examples/worked_example.md](examples/worked_example.md) - Complete evaluation example
- [schemas/evaluation_report.yaml](schemas/evaluation_report.yaml) - Standard report template
