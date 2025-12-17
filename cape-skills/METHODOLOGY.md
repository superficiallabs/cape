# Methodology: Converting Skills to Policies

This document explains the process used to convert Anthropic Agent Skills into CAPE policy specifications.

## Core Principles

### 1. Static Verification Only

**All verification must be static analysis of model outputs.** No execution harnesses, no runtime testing, no external service calls.

| ✓ Static (allowed) | ✗ Execution (not allowed) |
|-------------------|--------------------------|
| Parse file structure | Run code and check output |
| Validate XML schema | Open file in application |
| Check AST for patterns | Execute tests |
| Count/measure properties | Call external APIs |
| Compare before/after | Render and screenshot |

**Why?** CAPE verifies *outputs*, not *behaviors*. The model produces artifacts (code, documents, images). We verify those artifacts are structurally correct. Whether they behave correctly when executed is downstream—and often depends on context outside the model's control.

**Practical implication:** Predicates like `opens_in_excel(file)` are replaced with structural equivalents like `xml_schema_valid(file, 'sml.xsd')`. If structural checks pass, the file will open.

### 2. Correction Hints Are Mandatory

Every policy must include `on_violation.correction_hint` fields:

```json
{
  "on_violation": {
    "action": "CORRECT",
    "correction_hint": "Add type annotations to function signatures"
  }
}
```

**Why?** The CAPE training loop is: **Specify → Verify → Correct → Train**

Without correction hints, violations are just pass/fail signals. With hints, violations become training data:
- `(prompt, failing_output, violation)` → negative example
- `(prompt, corrected_output)` → positive example

Hints should be specific enough to guide correction but not so specific that they give away the answer.

### 3. Verify Artifacts, Not Processes

Policies verify the **output artifact**, not the **process** that created it.

| ✓ Artifact verification | ✗ Process verification |
|------------------------|----------------------|
| "Document has required sections" | "User was asked clarifying questions" |
| "Code has type annotations" | "Code was written incrementally" |
| "Form fields are filled" | "Form was reviewed before submission" |

**Why?** We can inspect artifacts statically. We cannot reliably verify conversation flow or multi-turn processes from the final output alone.

---

## The Conversion Process

### Step 1: Audit the Skill

Read the entire `SKILL.md` and categorize every statement:

| Type | CAPE Tier | Definition | Action |
|------|-----------|------------|--------|
| **Hard constraint** | **T1** | Protocol violations, broken files, fatal errors | Write predicate |
| **Safety/Compliance** | **T2** | Security risks, PII exposure, policy violations | Write predicate |
| **Soft constraint** | **T3** | Quality, style, structural preferences | Write predicate with proxy |
| **Non-verifiable** | None | Subjective or context-dependent | Document only |

Record this audit in `MAPPING.md`.

### Step 2: Extract Direct Predicates (T1/T2)

For hard constraints and safety rules, identify the verifiable property and write a predicate.

**Example: Platform Limit (T1)**

| Source | Predicate |
|--------|-----------|
| "GIFs must be under 64KB for Slack emoji" | `file_size_bytes(file) <= 65536` |

```json
{
  "id": "policy.slack_gif.size_limit",
  "tier": "T1",
  "assert": [
    { "expr": "file_size_bytes(file) <= 65536", "msg": "GIF exceeds Slack's 64KB limit" }
  ],
  "on_violation": {
    "action": "CORRECT",
    "correction_hint": "Reduce file size: fewer frames, smaller palette, lossy compression"
  }
}
```

**Example: Security Rule (T2)**

| Source | Predicate |
|--------|-----------|
| "No hardcoded secrets in code" | `hardcoded_secret_count(code) == 0` |

```json
{
  "id": "policy.security.no_secrets",
  "tier": "T2",
  "assert": [
    { "expr": "hardcoded_secret_count(code, config.secret_patterns) == 0", "msg": "Hardcoded secrets detected" }
  ],
  "on_violation": {
    "action": "CORRECT",
    "correction_hint": "Move secrets to environment variables: process.env.API_KEY"
  }
}
```

### Step 3: Fix Assumptions for Soft Constraints (T3)

Subjective guidance cannot be verified directly. Define a **structural proxy**—a measurable property that correlates with the subjective goal.

**Example: "Avoid AI Slop"**

| Source | Interpretation | Proxy |
|--------|----------------|-------|
| "Avoid generic AI aesthetics" | Slop = uniformity, lack of variety | Verify variety in design tokens |

```json
{
  "id": "policy.frontend.design_variety",
  "tier": "T3",
  "assert": [
    { "expr": "unique_border_radius_count(css) >= 3", "msg": "Uniform border-radius" },
    { "expr": "unique_color_count(css) >= 4", "msg": "Limited color palette" }
  ],
  "on_violation": {
    "action": "CORRECT",
    "correction_hint": "Add intentional variety: different border radii for buttons, cards, inputs"
  }
}
```

**What makes a good proxy?**

| Criterion | Good | Bad |
|-----------|------|-----|
| **Measurable** | Token count, unique values | "Feels professional" |
| **Correlates** | Low variety → likely generic | High variety → not necessarily good |
| **Actionable** | "Add more color variety" | "Be more creative" |
| **Configurable** | Threshold can be adjusted | Binary with no gradation |

**Document every assumption** in `ASSUMPTIONS.md`:
- Original guidance (verbatim)
- Interpretation (what we think it means)
- Proxy chosen (what we measure)
- Default thresholds (with rationale)
- Customization guidance

### Step 4: Parameterize Thresholds

Replace hardcoded values with configuration parameters:

```json
{
  "configuration": {
    "min_color_variety": 4,
    "max_font_families": 3,
    "min_contrast_ratio": 4.5
  }
}
```

Users override at evaluation time without modifying the policy.

### Step 5: Handle Non-Verifiable Guidance

Some guidance cannot be converted to predicates:

| Type | Example | Handling |
|------|---------|----------|
| Context-dependent | "Appropriate tone for audience" | Requires context specification |
| Requires judgment | "Balance creativity with clarity" | No measurable proxy |
| Process-oriented | "Iterate based on feedback" | Describes workflow, not output |

For these:
1. Document in MAPPING.md as "Non-verifiable"
2. Do not write a predicate
3. Retain in skill guidance for human readers

> **Note:** "Context-dependent" items become verifiable once context is specified. See the paper's "contextual objectivity" principle.

---

## Scope Specification

The `scope` field specifies what the policy evaluates:

```json
{
  "scope": {
    "kind": "output_file",
    "filter": { "extension": "docx" }
  }
}
```

| Kind | Description | Example filters |
|------|-------------|-----------------|
| `output_file` | Binary or text file | `{ "extension": "pdf" }` |
| `code_output` | Source code | `{ "type": ["jsx", "tsx"] }` |
| `css_output` | Stylesheet | — |
| `text_content` | Plain text/markdown | — |

---

## Output Structure

Each converted skill produces:

### 1. `policy.cpl`

The executable specification:

```json
{
  "id": "capability.skill_name",
  "version": "1.0.0",
  "description": "...",
  "source": "anthropics/skills/skill-name",
  
  "configuration": { ... },
  
  "scope": {
    "kind": "...",
    "filter": { ... }
  },
  
  "policies": [
    {
      "id": "policy.skill_name.check_name",
      "tier": "T1|T2|T3",
      "description": "...",
      "where": [ ... ],  // optional conditions
      "assert": [ ... ],
      "on_violation": {
        "action": "CORRECT",
        "correction_hint": "..."
      }
    }
  ]
}
```

### 2. `MAPPING.md`

Audit trail from skill guidance to predicates:

```markdown
| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "Under 64KB" | T1 | `file_size_bytes <= 65536` | Direct |
| 2 | "Professional tone" | T3 | `sentiment_score >= 0` | Proxy |
| 3 | "Engaging" | — | (non-verifiable) | — |
```

### 3. `ASSUMPTIONS.md`

Documents threshold rationale:

```markdown
## Assumption: Color Variety

**Original:** "Avoid generic AI aesthetics"

**Interpretation:** Generic outputs show uniformity; intentional design shows variety.

**Proxy:** `unique_color_count(css) >= config.min_colors`

**Default:** 4 (primary, secondary, accent, neutral minimum)

**Customization:** Minimalist designs may use 2; complex dashboards may need 8+.
```

---

## Validation Checklist

Before submitting:

| Check | Question |
|-------|----------|
| **Static only** | Do all predicates use static analysis? No execution? |
| **Correction hints** | Does every policy have a correction_hint? |
| **Completeness** | Is every SKILL.md statement in MAPPING.md? |
| **Tier accuracy** | T1=broken, T2=unsafe, T3=low-quality? |
| **Parameterized** | Are thresholds configurable, not hardcoded? |
| **Documented** | Are all assumptions explained with rationale? |

---

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Execution predicates** | `renders_successfully()`, `opens_in_app()` | Replace with structural checks |
| **Missing hints** | No correction guidance | Add specific, actionable hints |
| **Process verification** | Checking conversation flow | Verify artifacts only |
| **Hardcoded thresholds** | Not reusable | Parameterize everything |
| **Bad proxies** | Don't correlate with goal | Test against known-good/bad examples |
| **Tier inflation** | Preferences as T1/T2 | T1=broken, T2=unsafe only |

---

## Examples

**Cleanest (no assumptions):**
- [slack-gif-creator](no-assumptions/slack-gif-creator/) — Platform specs, file format

**Best T3 proxies:**
- [frontend-design](fixed-assumptions/frontend-design/) — Anti-slop with full rationale

**Document skills:**
- [docx](no-assumptions/docx/) — OOXML schema validation
- [xlsx](no-assumptions/xlsx/) — Formula and type checking
