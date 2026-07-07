# Contributing to the SAI Framework

Thank you for your interest in contributing to the **Sustainable AI Intelligence (SAI) Framework**. This is an open, community-driven specification repository.

## Ways to Contribute

- Reporting ambiguities or inconsistencies in the specification
- Proposing clarifications, errata, or normative fixes
- Suggesting benchmark or metric changes (with justification)
- Improving informative examples and the reference calculator
- Proposing conformance criteria refinements
- Web3/tokenization specification ideas (for future versions)

## What Belongs in This Repository

- Specification and protocol documents (`SPEC.md`, guides, conformance rules)
- Schemas for evaluation reports
- Informative worked examples and reference implementations with no external dependencies

## What Belongs Elsewhere

- Inference API integrations, SDKs, and provider-specific tooling
- Benchmark harnesses, notebooks, and evaluation pipelines
- Hardware measurement scripts and deployment automation
- Leaderboards, dashboards, and certification tooling

Conformant implementations are encouraged in separate repositories; link them from Issues or Discussions.

## Development Process

1. **Discuss First**  
   Open an Issue to discuss significant changes (new dimensions, formula changes, benchmark modifications) before submitting a PR.

2. **Fork and Branch**  
   - Fork the repository
   - Create a feature branch (`git checkout -b spec/your-proposal`)

3. **Make Changes**  
   - Keep changes focused and well-documented
   - Update `SPEC.md` for normative changes; update companion guides when affected
   - Mark informative vs normative content clearly

4. **Submit a Pull Request**  
   - Describe the change and its rationale
   - Reference related Issues
   - Note whether the change is backward-compatible with v0.2

## Pull Request Guidelines

- One logical specification change per PR
- Update all cross-referenced documents
- Prefer precise definitions over implementation detail
- Reference implementations should remain stdlib-only unless the community explicitly decides otherwise

## Questions?

Open an Issue or start a discussion. We appreciate your help in making SAI a clear, implementable standard for sustainable AI evaluation.
