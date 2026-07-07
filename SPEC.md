# SAI Framework Specification

**Sustainable AI Intelligence (SAI) Framework**  
**Version:** 0.2 (Draft)  
**Date:** July 2026  
**Status:** Proposed Open Standard  
**License:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

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
X_raw = Total_Tokens / Task_Success_Score

Where:
- Total_Tokens = Input_Tokens + Output_Tokens + Reasoning_Tokens (if applicable)
- Task_Success_Score = Normalized benchmark accuracy (0-1 scale)

X_norm = X_raw / X_baseline

Where:
- X_baseline = Token efficiency of reference model (GPT-3.5-turbo as of January 2024)
```

**Interpretation:**
- X_norm < 1.0: More efficient than baseline (better)
- X_norm = 1.0: Same efficiency as baseline
- X_norm > 1.0: Less efficient than baseline (worse)

#### 3.1.2 Tokenizer Normalization

Different models use different tokenizers, affecting token counts. For standardization:

```
Normalized_Tokens = Actual_Tokens × (Baseline_Tokens_Per_Word / Model_Tokens_Per_Word)

Where:
- Tokens_Per_Word = Total tokens / Total words for standard corpus
- Standard corpus: First 10,000 words of English Wikipedia
- Baseline: GPT-3.5-turbo tokenizer (cl100k_base)
```

**Alternative (Simpler):** Accept token counts as-is if all comparisons use the same tokenizer or API-reported counts.

#### 3.1.3 Edge Cases

- **Failed Tasks:** If Task_Success_Score = 0, exclude from X calculation or assign X = infinity (worst case)
- **Chain-of-Thought Tokens:** Include all reasoning tokens in Total_Tokens
- **Tool Use:** Include tool invocation tokens but not tool execution output
- **Multi-turn Conversations:** Sum all tokens across turns for the complete task

#### 3.1.4 Baseline Reference

**GPT-3.5-turbo (gpt-3.5-turbo-0125, January 2024 snapshot)**

Reference token efficiency values:
- MMLU-Pro: ~1,200 tokens per problem (avg)
- HumanEval+: ~800 tokens per problem (avg)
- MATH-500: ~1,500 tokens per problem (avg)

*Note: Exact baseline values will be published in a supplementary baseline dataset.*

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

**Complete Coverage (all benchmarks available):**
```
Y = Σ(weight_i × normalized_score_i)
```

**Partial Coverage (missing benchmarks):**
```
Y = Σ(weight_i × normalized_score_i) / Σ(weight_i for available benchmarks) × 100
```

**Requirement:** Must have ≥70% total weight represented.

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
Z = Y_score / Total_Energy_with_PUE

Where:
- Y_score = Intelligence score (0-100)
- Total_Energy_with_PUE = Total_Energy_Joules × PUE
- PUE = Power Usage Effectiveness (data center efficiency multiplier)
```

**Higher Z values indicate better energy efficiency.**

#### 3.3.2 Energy Measurement Protocol

SAI defines a **three-tier measurement system** to balance rigor with accessibility:

**Tier 1: Hardware Measurement (Highest Confidence)**
- Direct GPU/CPU power measurement using nvidia-smi, NVML, or TokenPowerBench
- Required for SAI-Full conformance
- See [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) for details

**Tier 2: API-Based Estimation (Medium Confidence)**
- Use provider-reported token counts + published energy benchmarks
- Formula: `Energy (J) = Tokens × Energy_per_Token (J/token)` from reference data
- Acceptable for SAI-Basic conformance
- Must cite energy benchmark source

**Tier 3: Literature-Based Estimation (Informational Only)**
- Use published energy measurements from academic papers or leaderboards
- Not sufficient for formal conformance
- Useful for preliminary comparisons

#### 3.3.3 Standardized Test Conditions

To ensure comparability, hardware measurements should follow these standards:

```
Standard Configuration:
- Batch size: 1 (single-user simulation)
- Input context: 2048 tokens (representative document)
- Output length: 512 tokens (typical response)
- Number of runs: 100 (for statistical reliability)
- Temperature: 0.0 (deterministic)
```

#### 3.3.4 Phase-Aware Measurement

LLM inference has two distinct phases with different power characteristics:

```
Total_Energy = Prefill_Energy + Decode_Energy

Prefill_Energy = Power_prefill (W) × Time_prefill (s)
Decode_Energy = Power_decode (W) × Tokens_generated × Time_per_token (s)
```

**Tier 1 measurements must report both phases separately.**

#### 3.3.5 PUE (Power Usage Effectiveness)

PUE accounts for data center overhead (cooling, networking, etc.):

```
Total_Energy_with_PUE = Measured_Energy × PUE

Default PUE values:
- Cloud providers (AWS, Azure, GCP): 1.3
- On-premises data centers: 1.5
- Measured PUE: Use actual facility measurements (preferred)
- Consumer hardware (local GPU): 1.0 (no data center overhead)
```

#### 3.3.6 Carbon Intensity (Optional)

For environmental impact reporting:

```
Carbon_Cost = Total_Energy_kWh × Grid_Intensity (gCO2/kWh)

Recommended sources:
- ElectricityMap API (real-time regional data)
- EPA eGRID (US)
- IEA emissions factors
- Default: 475 gCO2/kWh (2025 global average)
```

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

### 4.2 Worked Example

**Model: Llama-3.1-8B-Instruct evaluated on General/Reasoning workload**

#### Step 1: Calculate Y (Intelligence)
```
Benchmark results:
- MMLU-Pro: 68% → Normalized: ((68-25)/(100-25)) × 100 = 57.3
- GPQA Diamond: 42% → Normalized: ((42-25)/(100-25)) × 100 = 22.7
- MATH-500: 55% → Normalized: 55.0
- AIME: 15% → Normalized: 15.0
- HumanEval+: 70% → Normalized: 70.0
- SWE-Bench: 28% → Normalized: 28.0
- LiveCodeBench: 32% → Normalized: 32.0
- IFEval: 82% → Normalized: 82.0
- MT-Bench: 7.8/10 → Normalized: 78.0

Y = (20% × 57.3) + (15% × 22.7) + (15% × 55.0) + (5% × 15.0) + 
    (15% × 70.0) + (10% × 28.0) + (5% × 32.0) + (10% × 82.0) + (5% × 78.0)
Y = 11.46 + 3.41 + 8.25 + 0.75 + 10.5 + 2.8 + 1.6 + 8.2 + 3.9
Y = 50.87
```

#### Step 2: Calculate X_norm (Token Efficiency)
```
Total tokens for benchmark suite: 145,000
GPT-3.5-turbo baseline: 120,000 tokens

X_raw = 145,000 / 0.5087 = 285,051 tokens per intelligence point
X_baseline = 120,000 / 0.55 = 218,182 tokens per intelligence point
  (assuming GPT-3.5 scores Y=55 on same benchmarks)

X_norm = 285,051 / 218,182 = 1.31
```

#### Step 3: Calculate Z (Energy Efficiency)
```
Measurement (Tier 1 - Hardware):
- Total energy for benchmark suite: 12,500 Joules
- PUE: 1.3 (cloud deployment)
- Total energy with PUE: 12,500 × 1.3 = 16,250 J

Z = Y / Total_Energy_with_PUE
Z = 50.87 / 16,250 = 0.00313 IP/J
```

#### Step 4: Calculate SII
```
SII = (Y × Z) / X_norm × 100
SII = (50.87 × 0.00313) / 1.31 × 100
SII = 0.1592 / 1.31 × 100
SII = 12.15
```

**Result: Llama-3.1-8B-Instruct SII = 12.15**

### 4.3 SII Interpretation Ranges

Based on preliminary evaluations (subject to refinement):

- **SII > 40:** Exceptional sustainable intelligence (frontier models, optimal deployment)
- **SII 25-40:** Excellent sustainable intelligence (production-ready, efficient)
- **SII 15-25:** Good sustainable intelligence (capable models, acceptable efficiency)
- **SII 8-15:** Moderate sustainable intelligence (entry-level models or inefficient deployment)
- **SII < 8:** Poor sustainable intelligence (consider alternatives)

*Note: These ranges are provisional and will be calibrated as more evaluations are completed.*

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
Z: 0.00313 ± 0.00008 IP/J (based on 100 runs)
X_norm: 1.31 ± 0.05
SII: 12.15 ± 0.4
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

### v0.2 (July 2026)
- ✅ Added precise mathematical definitions for X, Y, Z
- ✅ Defined three-tier energy measurement system
- ✅ Specified GPT-3.5-turbo as normalization baseline
- ✅ Added worked example with Llama-3.1-8B
- ✅ Defined four workload categories with specific weights
- ✅ Added SII scaling factor (×100) for readability
- ✅ Expanded reproducibility requirements
- ✅ Added conformance level details
- ✅ Published BENCHMARK_GUIDE.md, CONFORMANCE.md, evaluation report schema
- ✅ Reference SII calculator and worked example documentation

### v0.1 (July 2026)
- Initial specification release
- Core 3D framework definition
- Basic SII formula
- High-level benchmark guidance

---

**For implementation guidance, see:**
- [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) - Energy measurement procedures
- [BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md) - Benchmark execution standards
- [CONFORMANCE.md](CONFORMANCE.md) - Conformance levels and self-assessment
- [examples/sii_calculator.py](examples/sii_calculator.py) - Reference implementation
- [examples/worked_example.md](examples/worked_example.md) - Complete evaluation example
- [schemas/evaluation_report.yaml](schemas/evaluation_report.yaml) - Standard report template
