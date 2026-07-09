# SAI Framework — Sustainable AI Intelligence Framework

**Version:** 0.2.1 (Draft)  
**Date:** July 2026  
**License:** [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## Overview

The **Sustainable AI Intelligence (SAI) Framework** is an open specification for evaluating Large Language Models (LLMs) across three dimensions — Token Efficiency, Intelligence/Value Generation, and Energy Sustainability — and combining them into the **Sustainable Intelligence Index (SII)**.

This repository contains the normative and informative documents that define the standard. It is not an application, SDK, or provider integration.

## Core Dimensions

| Dimension | Name | Primary Metric |
|-----------|------|----------------|
| **X** | Token Efficiency | Normalized tokens per intelligence unit (`X_norm`) |
| **Y** | Intelligence / Value | Weighted benchmark score (0–100) |
| **Z** | Energy Sustainability | Intelligence Points per Joule (IP/J) |

**SII:** `SII = (Y × Z) / X_norm × 100`

Full definitions are in **[SPEC.md](SPEC.md)**.

## Specification Documents

| Document | Role |
|----------|------|
| [SPEC.md](SPEC.md) | Normative core — metrics, SII, governance |
| [BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md) | Normative — benchmark execution and Y scoring |
| [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) | Normative — energy measurement (Z dimension) |
| [CONFORMANCE.md](CONFORMANCE.md) | Normative — SAI-Basic / SAI-Full requirements |
| [schemas/evaluation_report.yaml](schemas/evaluation_report.yaml) | Report schema for published evaluations |

## Informative Examples

| Document | Role |
|----------|------|
| [examples/worked_example.md](examples/worked_example.md) | End-to-end evaluation walkthrough |
| [examples/sii_calculator.py](examples/sii_calculator.py) | Reference implementation (Python stdlib only) |

```bash
python3 examples/sii_calculator.py
python3 examples/sii_calculator.py --self-test
```

Benchmark harnesses, inference APIs, and hardware tooling belong in separate projects that conform to this specification.

## Workload Categories

- **General / Reasoning** — business analysis, writing, QA (default)
- **Coding** — software development, debugging
- **Scientific / Mathematical** — research, calculations
- **Agentic / Tool-Use** — autonomous agents, automation

## Conformance Levels

- **SAI-Basic v0.2.1** — ≥70% benchmark coverage, Tier 2+ energy, suite-scoped Z
- **SAI-Full v0.2.1** — 100% primary coverage, Tier 1 energy, ≥2 workload categories
- **SAI-Certified** — planned for v1.0 (independent verification)

See [CONFORMANCE.md](CONFORMANCE.md).

## Web3 Tokenomics (Informative)

SAI defines a bridge between AI token consumption and verifiable intelligence units. Detailed Web3 integration is planned for v0.3.

## Governance and Contributions

See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).

## Related Work

- TokenPowerBench
- Hugging Face Open LLM Leaderboard
- ML.Energy Leaderboard
- MLPerf, TPCx-AI

## License

[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)
