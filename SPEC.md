# SAI Framework Specification

**Sustainable AI Intelligence (SAI) Framework**  
**Version:** 0.1 (Draft)  
**Date:** July 2026  
**Status:** Proposed Open Standard  
**License:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 1. Abstract

The SAI Framework defines a standardized 3D evaluation system for LLMs consisting of Token Efficiency (X), Intelligence/Value Generation (Y), and Energy Sustainability (Z). It produces the **Sustainable Intelligence Index (SII)** as a primary composite metric.

The framework aims to reduce evaluation fragmentation and enable a reliable bridge between AI token consumption and Web3 tokenomics through standardization and normalization.

## 2. Motivation

Current LLM evaluations are fragmented. SAI creates a unified standard that normalizes AI token consumption, value generation, and sustainability, enabling direct economic relationships with Web3 tokens.

## 3. Core Dimensions (3D Coordinate System)

### 3.1 X: Token Efficiency (Consumption)
**Definition:** Effective token usage relative to delivered value.  
**Primary Metric:** Effective Tokens per Value Unit = (Total Tokens Processed) / Normalized Y Score component.  
**Lower values are better.**

### 3.2 Y: Intelligence / Value Generation (Performance)
**Definition:** Composite measure of capability and usefulness.  
**Primary Metric:** Normalized Value Score (0–100).  
**Higher values are better.**

**Mandatory Minimum Benchmark Suite (v0.1):**

| Pillar                        | Suggested Weight | Recommended Benchmarks |
|-------------------------------|------------------|------------------------|
| Broad Reasoning & Knowledge   | 35%             | MMLU-Pro, GPQA Diamond, Humanity's Last Exam |
| Mathematical & Scientific     | 20%             | MATH-500, AIME |
| Coding & Software Engineering | 25%             | HumanEval+, SWE-Bench Verified, LiveCodeBench |
| Instruction Following         | 15%             | MT-Bench, Arena-Hard, IFEval |
| Safety, Alignment & Creativity| 5% (optional)   | TruthfulQA, agent benchmarks |

**Aggregation Rule:** Weighted average of normalized (0–100) benchmark scores. Alternative: Elo ranking when head-to-head data available.

### 3.3 Z: Energy Sustainability (Green)
**Definition:** Energy and carbon cost per unit of intelligence.  
**Primary Metric:** Value per Joule = Y Score / Total Joules consumed (or Tokens per kWh).  
**Higher values are better.**

**Measurement Protocol:**
- Phase-aware (prefill vs. decode) using TokenPowerBench or equivalent.
- Include GPU, CPU, RAM, and PUE (default 1.3 if not measured).
- Optional: Carbon adjustment using regional grid intensity.

## 4. Sustainable Intelligence Index (SII)

**Default Formula (v0.1):**  
`SII = Y / (X_norm × Z_cost)`  

Where:
- `X_norm` = X score normalized against a chosen baseline (configurable per category)
- `Z_cost` = Energy per Value Unit (Joules per Y point)

Exact baselines and category-specific weights will be defined in future versions.

## 5. Evaluation Workflow and Conformance

**SAI-Basic Conformance:**
- Use the mandatory benchmark suite
- Evaluate on at least one workload category
- Measure X, Y, Z and compute SII
- Publish results with full methodology, tool versions, and hardware disclosure

**SAI-Full Conformance:**
- All mandatory benchmarks across multiple categories
- Phase-aware energy measurement
- Reproducibility package (seeds, prompts or hashes, code)

**Reproducibility Requirements:**
- Fixed random seeds
- Public or hashed prompt sets
- Complete environment and hardware disclosure

## 6. Bridging to Web3 Tokenomics

The SAI Framework standardizes AI LLM token consumption and normalizes it into verifiable intelligence units. This creates a direct bridge to Web3 tokenomics by enabling:

- **Tokenization** of SII scores and 3D coordinates as on-chain assets (e.g., ERC-721 SAI Certificates)
- **Incentive alignment** through staking on high-SII models and green yield mechanisms
- **Decentralized oracles** for periodic SII updates
- **Composable primitives** such as agent routing, derivatives, and agent-to-agent economies

## 7. Governance

- Open contribution via GitHub Issues and Pull Requests
- Major changes (formula, mandatory benchmarks, conformance levels) require a 2-week discussion period and community consensus
- Goal: Transition to a neutral foundation or formal standards body by v1.0

## 8. References

- TokenPowerBench
- Hugging Face AI Energy Score and Open LLM Leaderboard
- ML.Energy Leaderboard
- MLPerf, TPCx-AI, and related standards