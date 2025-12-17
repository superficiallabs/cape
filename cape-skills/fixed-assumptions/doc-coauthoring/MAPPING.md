# Mapping: doc-coauthoring

> **Source:** [anthropics/skills/doc-coauthoring](https://github.com/anthropics/skills/tree/main/doc-coauthoring)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | Produces document output | T1 | `file_exists(output) == true` | Direct |
| 2 | Valid file format | T1 | `format(output) in config.allowed_formats` | Direct |
| 3 | Well-formed structure | T1 | `document_parseable(output) == true` | Direct |
| 4 | Meaningful content | T1 | `word_count(output) >= config.min_word_count` | Direct |
| 5 | Organized into sections | T1 | `section_count(output) >= config.min_section_count` | Direct |
| 6 | Sections have content | T1 | `min_section_word_count(output) >= config.min_section_word_count` | Direct |
| 7 | Logical heading hierarchy | T3 | `heading_hierarchy_valid(output) == true` | Direct |
| 8 | Reasonable nesting depth | T3 | `max_heading_level(output) <= config.max_heading_depth` | Direct |

---

## Verification Approach

This policy verifies the **document artifact**, not the collaborative process that created it.

The source skill defines a multi-stage workflow (context gathering → brainstorming → drafting → revision → reader testing). These process stages are valuable runtime guidance but cannot be verified through artifact inspection alone.

**What CAPE verifies:** The final document meets structural and content requirements.

**What remains as skill guidance:** The collaborative workflow, question-asking behavior, option generation, and iteration patterns.

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | File exists, valid format, parseable, word count, sections, section content | Missing or broken document = hard failure |
| **T3** | Heading hierarchy, nesting depth | Structural quality preferences |

---

## Not Mapped (Process Verification)

The following guidance describes *how* to create the document, not *what* the document should be:

| Guidance | Why not mapped |
|----------|----------------|
| "Ask clarifying questions" | Requires conversation analysis, not artifact inspection |
| "Provide options for sections" | Process behavior, not output property |
| "Iteratively build" | Multi-turn process, not verifiable from final output |
| "Reader testing stage" | Process step, not artifact property |

These remain in the skill as runtime guidance. The model should follow this workflow, but CAPE verifies the output, not the journey.

---

## Not Mapped (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Effective collaboration" | Subjective process quality | Retained as skill guidance |
| "High-quality document" | Multidimensional content quality | Structural checks only |
| "Appropriate tone" | Context-dependent | Retained as skill guidance |
| "Meets user's needs" | Subjective satisfaction | Retained as skill guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 6 | Fully verified |
| T2 (Governance) | 0 | None in source skill |
| T3 (Quality) | 2 | Verified |
| Process (not mapped) | 4 | Documented as skill guidance |
| Non-verifiable | 4 | Documented |
| **Total** | **16** | — |
