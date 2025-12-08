# CAPE

**Capability Achievement via Policy Execution**

An open specification for representing, evaluating, and sharing AI capabilities as executable policies.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Schema Version](https://img.shields.io/badge/schema-v1.0.0-green.svg)](schemas/)
[![Validation](https://github.com/superficiallabs/cape/actions/workflows/validate.yml/badge.svg)](https://github.com/superficiallabs/cape/actions/workflows/validate.yml)

---

## What is CAPE?

CAPE defines three standards for executable AI capabilities:

| Component | Description |
|-----------|-------------|
| **PredicateGraph** | Structured representation of model outputs |
| **CPL** | Capability Policy Language for specifying requirements |
| **Policy Packs** | Versioned collections of executable policies |

These enable deterministic, auditable capability testing for AI systems.

---

## Current Scope

This release (v1.0.0) includes specifications for both verification modes described in the CAPE paper:

| Component | Status | Description |
|-----------|--------|-------------|
| **PredicateGraph** | Complete | Structured output representation |
| **CPL (Symbolic Policies)** | Complete | Executable policies for structural properties |
| **Learned Verifier Rubrics** | Complete | Specifications for semantic verification |
| **Core Policy Packs** | Complete | Arithmetic, citations, code safety |
| **Example Rubrics** | Complete | Argument soundness, proof validity, plan feasibility |

### What's Included

- Full specifications for PredicateGraph, CPL, and Learned Verifiers
- JSON Schemas for validation
- Core policy packs with examples
- Example verifier rubrics for reasoning domains

### What's NOT Included

This repository contains **specifications**, not implementations:

| Component | Status | Notes |
|-----------|--------|-------|
| PredicateGraph Extractors | Not included | Implementation-specific |
| CPL Runtime (policy execution) | Not included | Implementation-specific |
| Learned Verifier Weights | Not included | Training required |
| Correction Engine | Not included | Implementation-specific |
| Training Loop | Not included | Implementation-specific |

Reference implementations are available separately from Superficial Labs.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/superficiallabs/cape.git
cd cape

# Install validator dependencies
pip install -r validator/requirements.txt

# Validate all artifacts
python validator/validate.py --all

# Validate a single file
python validator/validate.py --file examples/tool-use/tip-calc-violation.json --kind predicategraph
```

---

## Repository Contents

### Directory Structure

```
CAPE/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── .gitignore
├── .editorconfig
│
├── specs/
│   ├── predicate-graph.md
│   ├── cpl.md
│   ├── policy-packs.md
│   ├── learned-verifiers.md
│   ├── extraction.md
│   ├── correction.md
│   ├── glossary.md
│   ├── governance.md
│   └── compatibility-matrix.md
│
├── schemas/
│   ├── predicate-graph-v1.0.0.json
│   ├── cpl-policy-v1.0.0.json
│   ├── policy-pack-v1.0.0.json
│   └── verifier-rubric-v1.0.0.json
│
├── packs/
│   ├── core.tool-use.v1.json
│   ├── core.citation-grounding.v1.json
│   ├── core.safe-code.v1.json
│   └── example.customer-support.v1.json
│
├── rubrics/
│   ├── reasoning.argument-soundness.v1.json
│   ├── mathematics.proof-validity.v1.json
│   └── agents.plan-feasibility.v1.json
│
├── examples/
│   ├── README.md
│   ├── tool-use/
│   │   ├── tip-calc-violation.json
│   │   └── tip-calc-violation.expectations.json
│   ├── citation-grounding/
│   │   ├── factual-no-citation.json
│   │   └── factual-no-citation.expectations.json
│   ├── safe-code/
│   │   ├── python-unsafe.json
│   │   └── python-unsafe.expectations.json
│   ├── customer-support/
│   │   ├── no-acknowledgment.json
│   │   └── no-acknowledgment.expectations.json
│   └── reasoning/
│       ├── argument-unsound.json
│       └── argument-unsound.expectations.json
│
└── validator/
    ├── README.md
    ├── requirements.txt
    └── validate.py
```

### Specifications

| File | Description |
|------|-------------|
| specs/predicate-graph.md | PredicateGraph specification |
| specs/cpl.md | CPL language specification |
| specs/policy-packs.md | Policy Pack specification |
| specs/learned-verifiers.md | Learned Verifier specification |
| specs/extraction.md | Extraction specification |
| specs/correction.md | Correction specification |
| specs/glossary.md | Terminology |
| specs/governance.md | Governance model |
| specs/compatibility-matrix.md | Version compatibility |

### Schemas

| File | Description |
|------|-------------|
| schemas/predicate-graph-v1.0.0.json | PredicateGraph JSON Schema |
| schemas/cpl-policy-v1.0.0.json | CPL Policy JSON Schema |
| schemas/policy-pack-v1.0.0.json | Policy Pack JSON Schema |
| schemas/verifier-rubric-v1.0.0.json | Verifier Rubric JSON Schema |

### Policy Packs

| Pack | Description |
|------|-------------|
| core.tool-use.v1 | Tool call correctness |
| core.citation-grounding.v1 | Citation verification |
| core.safe-code.v1 | Code safety |
| example.customer-support.v1 | Customer support (example) |

### Examples

Each example includes a PredicateGraph and expected policy outcomes:

- **tool-use/** — Tool argument mismatch
- **citation-grounding/** — Missing citations
- **safe-code/** — Dangerous code patterns
- **customer-support/** — Support quality
- **reasoning/** — Argument soundness violation

---

## Versioning

CAPE uses semantic versioning:

- **MAJOR**: Breaking changes
- **MINOR**: Backward-compatible additions
- **PATCH**: Documentation fixes

See [compatibility-matrix.md](specs/compatibility-matrix.md) for details.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

Apache License 2.0

---

## Citation

```bibtex
@article{superficiallabs2025cape,
  title={CAPE: Capability Achievement via Policy Execution},
  author={Superficial Labs},
  year={2025},
  url={https://github.com/superficiallabs/cape}
}
```

---

## Contact

- **Website**: [superficiallabs.com](https://superficiallabs.com)
- **Email**: research@superficiallabs.com




