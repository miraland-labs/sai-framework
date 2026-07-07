# SAI Conformance Guide

**SAI Framework v0.2**  
**Date:** July 2026

This document defines conformance levels, badge eligibility, and a self-assessment checklist for SAI evaluations. It implements [SPEC.md](SPEC.md) Section 6.

## Conformance Levels Overview

| Level | Badge | Energy Tier | Benchmark Coverage | Primary Use Case |
|-------|-------|-------------|-------------------|------------------|
| SAI-Basic | SAI-Basic v0.2 | Tier 2+ | ≥70% weight in one category | Public scorecards, API providers |
| SAI-Full | SAI-Full v0.2 | Tier 1 | 100% in one category + 2 categories total | Research, procurement, leaderboards |
| SAI-Certified | SAI-Certified | Tier 1 + audit | All 4 categories | Future (v1.0+) |

Tier 3 (literature-based energy) is **not** sufficient for any conformance level.

## SAI-Basic Conformance

### Requirements

1. **Benchmark coverage:** ≥70% of total weight in at least one workload category
2. **Energy measurement:** Tier 2 (API-based estimation) or Tier 1 (hardware)
3. **Methodology:** Published document describing evaluation procedure
4. **Environment disclosure:** Hardware and software per SPEC.md Section 5.1
5. **Inference config:** Documented per SPEC.md Section 5.2
6. **Timeliness:** Results published within 60 days of evaluation date
7. **Statistics:** Confidence intervals on Y, Z, X_norm, and SII where applicable

### Badge Text

```
SAI-Basic v0.2 (General)
```

Replace `(General)` with the evaluated workload category: `Coding`, `Scientific`, or `Agentic`.

### Self-Assessment Checklist

```markdown
- [ ] Workload category declared: _______________
- [ ] Benchmark coverage: _____% (minimum 70%)
- [ ] Energy tier: [ ] 1  [ ] 2
- [ ] Energy source cited (Tier 2): _______________
- [ ] Environment YAML complete
- [ ] Inference config matches SPEC (temperature=0.0, seed=42, etc.)
- [ ] Evaluation date: _______________
- [ ] Report published within 60 days
- [ ] Confidence intervals reported
- [ ] schemas/evaluation_report.yaml filled
```

## SAI-Full Conformance

### Requirements

All SAI-Basic requirements, plus:

1. **Benchmark coverage:** 100% of weights in the primary workload category
2. **Energy measurement:** Tier 1 hardware measurement only
3. **Phase-aware energy:** Prefill and decode reported separately
4. **Cross-category:** Evaluated in at least **two** workload categories
5. **Reproducibility package:** Code, configs, and prompt hashes or full prompts
6. **Verification:** Third-party reproduction option documented
7. **Monitoring:** Quarterly re-evaluation recommended (not enforced in v0.2)

### Badge Text

```
SAI-Full v0.2 (General, Coding)
```

List all evaluated categories.

### Additional Checklist Items

```markdown
- [ ] 100% benchmark coverage in primary category
- [ ] Tier 1 energy with tool name: _______________
- [ ] Phase breakdown: prefill ___ J, decode ___ J
- [ ] Second workload category: _______________
- [ ] Reproducibility package URL: _______________
- [ ] Prompt verification method: [ ] full prompts  [ ] SHA-256 hashes
- [ ] Third-party verification contact/process documented
```

## SAI-Certified (Future — v1.0+)

Not available in v0.2. Planned requirements:

- Independent laboratory verification
- All four workload categories
- Carbon footprint certification
- Immutable audit trail
- Optional on-chain publication
- Annual re-certification

## Energy Tier Quick Reference

| Tier | Method | Accuracy | Conformance |
|------|--------|----------|-------------|
| 1 | NVML, nvidia-smi, TokenPowerBench | ±2% | SAI-Full (required), SAI-Basic (accepted) |
| 2 | API tokens × published J/token | ±10–15% | SAI-Basic (minimum) |
| 3 | Literature / model cards | ±20–30% | Informational only |

See [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) for procedures.

## Workload Category Coverage Calculation

Coverage = sum of weights for benchmarks with reported scores in the chosen category.

**Example (General, missing AIME and LiveCodeBench):**

```
Available: 20+15+15+15+10+10+5 = 90% (missing 5% AIME + 5% LiveCodeBench)
Coverage: 90% → qualifies for SAI-Basic (≥70%)
```

Use [examples/sii_calculator.py](examples/sii_calculator.py) to compute Y with partial coverage; the calculator enforces the 70% minimum.

## Submission Process (v0.2)

SAI v0.2 is a **self-declared open standard**. There is no central certifying body yet.

To publish a conformant evaluation:

1. Complete [schemas/evaluation_report.yaml](schemas/evaluation_report.yaml)
2. Run the self-assessment checklist above
3. Publish the report (GitHub, Hugging Face model card, or project website)
4. Display the badge only if all requirements for that level are met
5. Link to methodology and reproducibility artifacts

Misrepresenting conformance may be challenged via GitHub Issues; the community maintains reputational enforcement until v1.0 certification exists.

## Common Failure Modes

| Issue | Impact | Fix |
|-------|--------|-----|
| Tier 3 energy only | Cannot claim Basic or Full | Upgrade to Tier 2 with cited J/token data |
| Coverage <70% | Invalid Y / SII | Add benchmarks or switch to a narrower category |
| No confidence intervals | Fails Basic reporting | Bootstrap or report run variance |
| Wrong inference config | Non-reproducible | Set temperature=0.0, document seed |
| LiveCodeBench untagged | Incomparable scores | Add `LiveCodeBench-YYYY-MM` version tag |
| Missing PUE documentation | Invalid Z | Document measured or default PUE with source |

## Reference Materials

- [SPEC.md](SPEC.md) — Metric definitions
- [BENCHMARK_GUIDE.md](BENCHMARK_GUIDE.md) — Benchmark execution
- [MEASUREMENT_PROTOCOL.md](MEASUREMENT_PROTOCOL.md) — Energy tiers
- [examples/worked_example.md](examples/worked_example.md) — Full walkthrough
- [examples/sii_calculator.py](examples/sii_calculator.py) — Programmatic validation

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.2 | July 2026 | Initial conformance guide; three tiers; self-assessment checklists |
| 0.1 | July 2026 | High-level Basic/Full mentioned in SPEC only |
