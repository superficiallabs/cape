# Assumptions: skill-creator

> **Source:** [anthropics/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

The skill-creator skill asks for "effective" skills with "clear and comprehensive" descriptions. These are subjective qualities that we convert to measurable proxies: length bounds, content counts, and structural completeness.

**Philosophy:** An "effective" skill is one Claude can learn from. We verify the presence of teaching materials (instructions, examples, guidelines) without judging their quality. Quantity is a proxy for completeness.

**Verification approach:** All predicates use static file and content analysis—no execution required.

---

## Configuration Profiles

These thresholds define what "effective" means for your context:

**Public library skill:**
- `min_description_chars: 100`
- `max_description_chars: 400`
- `min_instruction_words: 200`
- `min_examples: 3`
- `min_guidelines: 2`

**Internal team skill:**
- `min_description_chars: 50`
- `max_description_chars: 500`
- `min_instruction_words: 100`
- `min_examples: 2`
- `min_guidelines: 1`

**Personal tooling skill:**
- `min_description_chars: 30`
- `max_description_chars: 600`
- `min_instruction_words: 50`
- `min_examples: 1`
- `min_guidelines: 0`

The policy doesn't define quality—you do. These predicates verify your definition objectively.

---

## Assumption 1: Description Length (Clarity)

**Original guidance:**
> "clear and comprehensive description so Claude knows when to use the skill"

**Interpretation:**
A good description is neither too short (uninformative) nor too long (overwhelming). We enforce length bounds as a proxy for appropriate information density.

**Predicates:**
```
description_length(skill) >= config.min_description_chars
description_length(skill) <= config.max_description_chars
```

**Tier:** T3 (Preference)

**Default thresholds:** `min_description_chars: 50`, `max_description_chars: 500`

**Threshold rationale:**

| Length | Interpretation |
|--------|----------------|
| < 30 | Too terse—likely missing context |
| 30–50 | Borderline—may be sufficient for simple skills |
| 50–200 | Good—concise and informative (sweet spot) |
| 200–500 | Detailed—comprehensive but scannable |
| > 500 | Too long—hard to scan, may indicate scope creep |

**What counts:**
- Character count of `description` field in frontmatter
- Excludes whitespace trimming (counts actual content)

**Customization:**
- Simple utility skills: lower max to `300`
- Complex multi-step skills: raise max to `800`
- Strict style guide: narrow range to `100-300`

---

## Assumption 2: Instruction Word Count (Actionability)

**Original guidance:**
> "effective skill" / "extend Claude's capabilities"

**Interpretation:**
An effective skill must have enough instructions for Claude to understand what to do. We measure instruction content volume.

**Predicate:**
```
instruction_word_count(skill) >= config.min_instruction_words
```

**Tier:** T3 (Preference)

**Default threshold:** `min_instruction_words: 100`

**Threshold rationale:**

| Word count | Interpretation |
|------------|----------------|
| < 50 | Stub—insufficient guidance |
| 50–100 | Minimal—covers basics only |
| 100–300 | Good—actionable instructions (default minimum) |
| 300–500 | Detailed—comprehensive guidance |
| > 500 | Extensive—may need restructuring |

**What counts as "instructions":**
- Main content of SKILL.md (excluding frontmatter, examples, code blocks)
- Prose describing what Claude should do
- Step-by-step guidance

**What doesn't count:**
- Code blocks (counted separately)
- Example sections (counted separately)
- Frontmatter fields

**Customization:**
- Simple skills: lower to `50`
- Tutorial-style skills: raise to `200`

---

## Assumption 3: Example Count (Learnability)

**Original guidance:**
> "effective skill"

**Interpretation:**
Claude learns from examples. Skills with multiple examples enable better generalization than single-example skills.

**Predicate:**
```
example_count(skill) >= config.min_examples
```

**Tier:** T3 (Preference)

**Default threshold:** `min_examples: 2`

**Threshold rationale:**

| Example count | Interpretation |
|---------------|----------------|
| 0 | No examples—hard to learn from |
| 1 | Single example—may not generalize |
| 2 | Multiple examples—enables pattern recognition (default) |
| 3–5 | Good variety—covers edge cases |
| 5+ | Comprehensive—may be redundant |

**What counts as an "example":**
- Clearly marked example sections (## Example, ### Example 1)
- Code blocks with usage demonstrations
- Input/output pairs

**What doesn't count:**
- Code snippets in instructions (unless demonstrating usage)
- References to external examples

**Customization:**
- Simple skills: lower to `1`
- Complex skills: raise to `3` or more

---

## Assumption 4: Guideline Count (Safety/Clarity)

**Original guidance:**
> "effective skill"

**Interpretation:**
Effective skills include usage guidelines—notes on when to use, when not to use, limitations, or warnings.

**Predicate:**
```
guideline_count(skill) >= config.min_guidelines
```

**Tier:** T3 (Preference)

**Default threshold:** `min_guidelines: 1`

**Threshold rationale:**

| Guideline count | Interpretation |
|-----------------|----------------|
| 0 | No guidance—Claude may misuse skill |
| 1 | Basic guidance—minimum acceptable (default) |
| 2–3 | Good guidance—covers common cases |
| 4+ | Comprehensive—may need organization |

**What counts as a "guideline":**
- Usage notes ("Use this skill when...")
- Warnings ("Do not use for...")
- Limitations ("This skill cannot...")
- Best practices sections

**What doesn't count:**
- Instructions (how to do it, not when to do it)
- Examples (demonstrations, not guidance)

**Customization:**
- Internal tools: may not need warnings—keep at `1`
- Public skills: raise to `2` for safety notes

---

## Not Verified (T1 Only)

These constraints are objectively verifiable without assumptions:

| Constraint | Tier | Why no assumption needed |
|------------|------|--------------------------|
| SKILL.md exists | T1 | File presence check |
| SKILL.md in root | T1 | Path check |
| Valid YAML frontmatter | T1 | Parse check |
| `name` field present | T1 | Field existence |
| `description` field present | T1 | Field existence |
| No extra frontmatter fields | T1 | Field enumeration |
| Name matches directory | T1 | String comparison |
| Internal links resolve | T1 | File existence check |
| Scripts have shebang | T1 | Content check |

---

## Not Verified (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Effective" | Semantic effectiveness | Completeness proxies |
| "Clear" | Prose clarity | Length bounds as proxy |
| "Useful" | Context-dependent | Retained as guidance |
| "Well-written" | Prose quality | Retained as guidance |
| "Comprehensive" | Completeness judgment | Content counts as proxy |

---

## Potential T2 Extensions

The current policy has no T2 (governance) checks. Consider adding:

| Check | Rationale |
|-------|-----------|
| No dangerous commands in scripts | Security—prevent rm -rf, etc. |
| No PII in examples | Privacy—redact real data |
| No hardcoded secrets | Security—use placeholders |
| License file present | Compliance—for public skills |

---

## Configuration Reference

```json
{
  "configuration": {
    "min_description_chars": 50,
    "max_description_chars": 500,
    "min_instruction_words": 100,
    "min_examples": 2,
    "min_guidelines": 1,
    "required_frontmatter_fields": ["name", "description"],
    "allowed_frontmatter_fields": ["name", "description"]
  }
}
```

Override any threshold at evaluation time to match your skill quality standards.
