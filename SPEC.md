# SAI Framework Specification

**Sustainable AI Intelligence (SAI) Framework**  
**Version:** 0.1 (Draft)  
**Date:** July 2026  
**Status:** Proposed Open Standard  
**License:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## 1. Abstract

The Sustainable AI Intelligence (SAI) Framework provides a standardized, multi-dimensional methodology for evaluating Large Language Models (LLMs) and generative AI systems. It defines three core dimensions — Token Efficiency, Intelligence/Value Generation, and Energy Sustainability — and derives the **Sustainable Intelligence Index (SII)**.

The framework enables consistent comparison, sustainable decision-making, and serves as a bridge between AI token consumption and Web3 tokenomics.

## 2. Motivation

Current LLM evaluations are fragmented. SAI creates a unified standard that normalizes AI token consumption, value, and sustainability, enabling direct economic relationships with Web3 tokens.

## 3. Core Dimensions (3D Coordinate System)

### 3.1 X: Token Efficiency (Consumption)
**Definition:** Effective token usage relative to delivered value.  
**Primary Metric:** Effective Tokens per Value Unit = (Total Tokens Processed) / Normalized Output Quality Score.  
**Lower values are better.**

### 3.2 Y: Intelligence / Value Generation (Performance)
**Definition:** Composite measure of capability and usefulness.  
**Primary Metric:** Normalized Value Score (0–100).  
**Higher values are better.**

**Required Pillars and Benchmarks:**

| Pillar                        | Suggested Weight | Recommended Benchmarks |
|-------------------------------|------------------|------------------------|
| Broad Reasoning & Knowledge   | 35%             | MMLU-Pro, GPQA Diamond, Humanity's Last Exam |
| Mathematical & Scientific     | 20%             | MATH/AIME, SciCode |
| Coding & Software Engineering | 25%             | HumanEval+, SWE-Bench Verified, LiveCodeBench |
| Instruction Following         | 15%             | MT-Bench, Arena-Hard, IFEval |
| Safety, Alignment & Creativity| 5% (optional)   | TruthfulQA, agent benchmarks |

**Aggregation:** Weighted average or pairwise Elo ranking. Scores must be versioned.

### 3.3 Z: Energy Sustainability (Green)
**Definition:** Energy and carbon cost per unit of intelligence.  
**Primary Metric:** Value per Joule = Y Score / Joules Consumed (or Tokens per kWh).  
**Higher values are better.**

**Measurement Protocol:**
- Use phase-aware tooling (e.g., TokenPowerBench).
- Include GPU + CPU + RAM + PUE.
- Optional carbon conversion using grid intensity.

## 4. Sustainable Intelligence Index (SII)

**Default Formula:**  
`SII = (Y × w_y) / (X_factor × Z_cost)`

Weights are configurable per workload category.

## 5. Evaluation Workflow (Conformance)

**Basic Conformance:**
1. Select workload category.
2. Run standardized task set with fixed seeds.
3. Measure X, Y, Z raw values.
4. Compute normalized scores and SII.
5. Publish results with full methodology disclosure.

**Full Conformance** includes reproducibility requirements, hardware disclosure, and multi-category evaluation.

**Reproducibility Rules:**
- Fixed random seeds
- Public or hashed prompt sets
- Complete hardware/software transparency

## 6. Bridging to Web3 Tokenomics

The SAI Framework standardizes and normalizes AI LLM token consumption into verifiable intelligence units. This creates a direct bridge to Web3 tokenomics by enabling:

- **Tokenization** of SII scores and 3D coordinates as on-chain assets (e.g., ERC-721 SAI Certificates).
- **Incentive alignment** through staking on high-SII models and green yield mechanisms.
- **Decentralized oracles** for periodic, trust-minimized SII updates.
- **Composable primitives** such as agent routing, derivatives, and agent-to-agent economies based on real-time coordinates.

This standardization reduces information asymmetry and allows AI tokens (consumption + value) to interact programmatically with Web3 economic systems.

## 7. Governance

This is an open specification. Contributions are welcome via Pull Requests and Issues. Major changes require community consensus. Future versions may seek formal standardization.

## 8. References

- TokenPowerBench
- Hugging Face AI Energy Score & Open LLM Leaderboard
- ML.Energy Leaderboard
- MLPerf, TPCx-AI, and related standards
