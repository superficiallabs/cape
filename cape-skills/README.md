# CAPE Skills

**Skills tell models what to do. Policies verify outputs and turn execution into learned capability.**

This repository contains executable CAPE policy specifications for all 16 of Anthropic's published [Agent Skills](https://github.com/anthropics/skills).

## Why policies?

Agent Skills are runtime instructions: markdown files that tell a model how to perform a task. But instructions alone do not guarantee correct execution, and they do not produce training signal for the model to learn the skill.

CAPE policies are **executable specifications**. They define what "correct" looks like using the **CAPE Tier System**, enabling:

| Capability | Skills | CAPE Policies |
|------------|:------:|:-------------:|
| Runtime guidance | ✓ | ✓ |
| Verify correct execution | ✗ | ✓ |
| Filter/weight training data | ✗ | ✓ |
| Embed as learned capability | ✗ | ✓ |

## Core Principles

### Static Verification Only

All policies use **static analysis** of model outputs. No execution harnesses required.

| Output Type | Verification Method |
|-------------|---------------------|
| Documents (docx, pdf, pptx, xlsx) | ZIP structure, XML parsing, schema validation |
| Code (JS, TS, Python) | AST analysis, syntax checking, pattern matching |
| Images (GIF, PNG) | File header parsing, metadata extraction |
| CSS/HTML | Parser validation, property checking |

**Why static?** CAPE verifies *outputs*, not *behaviors*. Whether code runs correctly when executed is downstream of whether the model produced correct code. Static checks catch structural issues that would cause runtime failures.

### Correction Hints Enable Training

Every policy includes `correction_hint` fields that guide the model to fix violations:

```json
{
  "on_violation": {
    "action": "CORRECT",
    "correction_hint": "Add await to async Playwright methods (page.goto, page.click, etc.)"
  }
}
```

This enables the CAPE training loop: **Specify → Verify → Correct → Train**. Violations become training signal, not just pass/fail gates.

## The CAPE Tier System

Every policy uses tiers to distinguish between "broken", "unsafe", and "low-quality":

| Tier | Definition | Violation meaning | Examples |
|------|------------|-------------------|----------|
| **T1** | **Objective correctness** | **Hard failure.** Artifact is broken or unusable. | Invalid syntax, corrupted file, missing required elements |
| **T2** | **Governance & safety** | **Compliance failure.** Artifact is unsafe or non-compliant. | PII exposure, hardcoded secrets, accessibility violations |
| **T3** | **Structural preference** | **Quality failure.** Artifact works but is off-spec. | Generic output, low variety, poor structure |

> **Note:** T3 constraints use *structural proxies*—measurable properties that correlate with subjective goals. "Avoid AI slop" becomes "use ≥3 unique border-radius values."

## Results

We converted all 16 Anthropic skills to CAPE policies:

| Category | Count | Description |
|----------|------:|-------------|
| **No assumptions needed** | 7 (44%) | Technical skills with objective requirements (T1/T2 only) |
| **Assumptions documented** | 9 (56%) | Skills requiring explicit thresholds for T3 proxies |
| **Total specifiable** | 16 (100%) | **Every skill becomes specifiable once assumptions are explicit** |

**There are no unverifiable skills. Only underspecified ones.**

## Repository Structure

```
cape-skills/
├── README.md
├── METHODOLOGY.md
├── analysis/
│   └── specifiability-matrix.md
├── no-assumptions/
│   ├── artifacts-builder/
│   ├── docx/
│   ├── pdf/
│   ├── pptx/
│   ├── slack-gif-creator/
│   ├── webapp-testing/
│   └── xlsx/
└── fixed-assumptions/
    ├── algorithmic-art/
    ├── brand-guidelines/
    ├── canvas-design/
    ├── doc-coauthoring/
    ├── frontend-design/
    ├── internal-comms/
    ├── mcp-builder/
    ├── skill-creator/
    └── theme-factory/
```

## Policy Structure

Each skill directory contains:

```
skill-name/
├── policy.cpl        # Executable CAPE specification
├── MAPPING.md        # Audit trail: SKILL.md guidance → predicates
└── ASSUMPTIONS.md    # Explicit thresholds and proxy rationale
```

**No-assumptions skills** have simpler ASSUMPTIONS.md files explaining why no T3 proxies are needed.

## Getting Started

**Cleanest example (no assumptions):**
- [slack-gif-creator](no-assumptions/slack-gif-creator/) — Platform constraints, file format specs

**Best T3 proxy example:**
- [frontend-design](fixed-assumptions/frontend-design/) — "Anti-slop" proxies with full rationale

## Quick Example

**Skill says:**
> "Create GIFs optimized for Slack's 64KB emoji limit."

**Policy verifies (static file inspection):**

```json
{
  "id": "policy.slack_gif.file_constraints",
  "tier": "T1",
  "scope": { "kind": "output_file", "filter": { "extension": "gif" } },
  "assert": [
    { "expr": "file_size_bytes(file) <= 65536", "msg": "GIF exceeds 64KB limit" },
    { "expr": "width(file) == 128", "msg": "Width must be 128px" },
    { "expr": "height(file) == 128", "msg": "Height must be 128px" },
    { "expr": "frame_count(file) > 1", "msg": "Must be animated" }
  ],
  "on_violation": {
    "action": "CORRECT",
    "correction_hint": "Reduce file size: fewer frames, smaller color palette, or lossy compression"
  }
}
```

All predicates use static file inspection—no GIF player or Slack API required.

## Usage

CAPE policies are executable specifications. Use them at any stage:

| Stage | Use case |
|-------|----------|
| **Training** | Filter/weight data by policy compliance |
| **Inference** | Verify outputs, trigger correction on violation |
| **Batch eval** | Audit existing outputs against policies |
| **Flywheel** | Verified production outputs → training data |

## Contributing

We welcome community-contributed policy packs. See [METHODOLOGY.md](METHODOLOGY.md) for the conversion approach. Submit a PR with:

- `policy.cpl` — The executable specification (static verification only)
- `MAPPING.md` — Audit trail from source guidance to predicates
- `ASSUMPTIONS.md` — Threshold rationale (even for no-assumptions skills)

## Related

- [Anthropic Agent Skills](https://github.com/anthropics/skills)
- [CAPE Paper](https://arxiv.org/abs/xxxx.xxxxx)
- [Superficial Labs](https://superficiallabs.com)
- [CapabilityBench](https://capabilitybench.com)

## License

Apache 2.0 (policies). Original skill content subject to Anthropic's licensing.
