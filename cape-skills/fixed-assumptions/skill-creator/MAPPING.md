# Mapping: skill-creator

> **Source:** [anthropics/skills/skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "SKILL.md required" | T1 | `file_exists(skill, 'SKILL.md') == true` | Direct |
| 2 | "SKILL.md required" | T1 | `skill_md_in_root(skill) == true` | Direct |
| 3 | "Frontmatter" | T1 | `has_yaml_frontmatter(skill) == true` | Direct |
| 4 | "Frontmatter" | T1 | `yaml_parse_error_count(skill) == 0` | Direct |
| 5 | "Frontmatter fields" | T1 | `has_frontmatter_field(skill, 'name') == true` | Direct |
| 6 | "Frontmatter fields" | T1 | `has_frontmatter_field(skill, 'description') == true` | Direct |
| 7 | "Frontmatter fields" | T1 | `extra_frontmatter_field_count(skill, ...) == 0` | Direct |
| 8 | "Name consistency" | T1 | `frontmatter_name(skill) == directory_name(skill)` | Direct |
| 9 | "Link integrity" | T1 | `broken_link_count(skill) == 0` | Direct |
| 10 | "Scripts work" | T1 | `scripts_missing_shebang_count(skill) == 0` | Direct |
| 11 | "clear description" | T3 | `description_length(skill) in [50, 500]` | Proxy |
| 12 | "effective skill" | T3 | `instruction_word_count(skill) >= 100` | Proxy |
| 13 | "effective skill" | T3 | `example_count(skill) >= 2` | Proxy |
| 14 | "effective skill" | T3 | `guideline_count(skill) >= 1` | Proxy |

---

## Verification Approach

All predicates use **static file and content analysis**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| File presence | SKILL.md exists, in root |
| YAML parsing | Frontmatter valid, fields present |
| String comparison | Name matches directory |
| Link resolution | Internal links resolve to files |
| Content parsing | Shebang present in scripts |
| Text metrics | Description length, word count, section counts |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | File structure, frontmatter, name match, links, scripts | Invalid structure = broken skill |
| **T3** | Description length, instructions, examples, guidelines | Quality/completeness preferences |

**Note:** No T2 (governance) constraints in this skill. Could be extended with security checks (no dangerous commands in scripts, no PII in examples).

---

## Skill Structure Requirements

Per the Agent Skills specification:

| Requirement | Verified by | Tier |
|-------------|-------------|------|
| SKILL.md exists in root | `file_exists()`, `skill_md_in_root()` | T1 |
| Valid YAML frontmatter | `has_yaml_frontmatter()`, `yaml_parse_error_count()` | T1 |
| `name` field present | `has_frontmatter_field()` | T1 |
| `description` field present | `has_frontmatter_field()` | T1 |
| No extra frontmatter fields | `extra_frontmatter_field_count()` | T1 |
| Name matches directory | `frontmatter_name() == directory_name()` | T1 |
| Internal links resolve | `broken_link_count()` | T1 |
| Scripts have shebang | `scripts_missing_shebang_count()` | T1 |

---

## Quality Metrics

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Description length | 50–500 chars | Long enough to be informative, short enough to scan |
| Instruction words | ≥100 words | Sufficient detail for Claude to understand task |
| Example count | ≥2 examples | Multiple examples improve generalization |
| Guideline count | ≥1 guideline | At least one usage note or warning |

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Effective" | Semantic effectiveness | Completeness proxies |
| "Clear" | Subjective clarity | Length bounds as proxy |
| "Useful" | Context-dependent | Retained as guidance |
| "Well-written" | Prose quality | Retained as guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 10 | Fully verified |
| T2 (Governance) | 0 | None in source skill |
| T3 (Quality) | 4 | Verified via proxies |
| Non-verifiable | 4 | Documented |
| **Total** | **18** | — |
