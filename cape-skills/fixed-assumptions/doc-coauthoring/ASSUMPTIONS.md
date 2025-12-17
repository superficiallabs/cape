# Assumptions: doc-coauthoring

> **Source:** [anthropics/skills/doc-coauthoring](https://github.com/anthropics/skills/tree/main/doc-coauthoring)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

The doc-coauthoring skill defines a collaborative workflow for document creation. This policy verifies the **document artifact**, not the process that created it.

**Scope clarification:** The skill describes a multi-stage process (context gathering, brainstorming, drafting, revision, reader testing). These stages are valuable runtime guidance but cannot be verified through artifact inspection. CAPE verifies outputs, not conversations.

**What we verify:** Document exists, has valid structure, contains meaningful content.

**What remains as skill guidance:** The collaborative workflow, question-asking, option generation, iteration patterns.

---

## Assumption 1: Minimum Content Length

**Original guidance:**
> "Produces document output"

**Interpretation:**
A co-authored document should have substantive content. Very short outputs suggest incomplete work or abandoned process.

**Predicate:**
```
word_count(output) >= config.min_word_count
```

**Tier:** T1 (Correctness) — below threshold = incomplete output

**Default threshold:** `min_word_count: 100`

**Threshold rationale:**

| Word count | Interpretation |
|------------|----------------|
| < 50 | Stub or placeholder — incomplete |
| 50–100 | Brief note — may be valid for simple requests |
| 100–500 | Short document — typical minimum (default) |
| 500–2000 | Standard document — typical range |
| 2000+ | Long-form document — reports, guides |

**Customization:**
- Quick notes: lower to `min_word_count: 50`
- Formal documents: raise to `min_word_count: 500`
- Length depends on request: make threshold context-dependent

---

## Assumption 2: Section Organization

**Original guidance:**
> "Structured workflow" (implies structured output)

**Interpretation:**
Documents should be organized into sections. A document with no sections is likely a wall of text without structure.

**Predicate:**
```
section_count(output) >= config.min_section_count
```

**Tier:** T1 (Correctness)

**Default threshold:** `min_section_count: 2`

**Threshold rationale:**

| Section count | Interpretation |
|---------------|----------------|
| 0 | No structure — wall of text |
| 1 | Single section — may be valid for simple docs |
| 2–3 | Basic structure — intro/body or intro/body/conclusion (default) |
| 4–6 | Well-organized — clear topic separation |
| 7+ | Complex document — may need simplification |

**What counts as a section:**
- Markdown headings (H1–H6)
- DOCX heading styles
- Clear structural breaks with titles

**Customization:**
- Simple outputs: lower to `min_section_count: 1`
- Complex documents: raise to `min_section_count: 4`

---

## Assumption 3: Section Content Depth

**Original guidance:**
> (Implicit in document quality)

**Interpretation:**
Each section should have meaningful content. Sections with just a heading and a sentence suggest incomplete development.

**Predicate:**
```
min_section_word_count(output) >= config.min_section_word_count
```

**Tier:** T1 (Correctness)

**Default threshold:** `min_section_word_count: 20`

**Threshold rationale:**

| Words per section | Interpretation |
|-------------------|----------------|
| < 10 | Stub — heading with no real content |
| 10–20 | Brief — single short paragraph |
| 20–50 | Adequate — developed point (default minimum) |
| 50–200 | Substantive — well-developed section |
| 200+ | Extensive — may need subdivision |

**Customization:**
- Outline-style docs: lower to `min_section_word_count: 10`
- Detailed documents: raise to `min_section_word_count: 50`

---

## Assumption 4: Heading Hierarchy

**Original guidance:**
> (Implicit in document structure)

**Interpretation:**
Headings should follow logical hierarchy. Skipping levels (H1 → H3) or inconsistent nesting creates confusing structure.

**Predicate:**
```
heading_hierarchy_valid(output) == true
```

**Tier:** T3 (Preference) — broken hierarchy is poor quality, not failure

**What "valid hierarchy" means:**
- No skipped levels (H1 → H3 without H2)
- Consistent nesting (H2 sections contain H3, not H4)
- Document starts with H1 (or configured top level)

**Customization:**
- Lenient: allow single-level skips
- Strict: require perfect nesting
- Flat docs: disable if document style doesn't use hierarchy

---

## Not Mapped (Process Verification)

The skill's collaborative workflow cannot be verified from the final artifact:

| Process Element | Why not artifact-verifiable |
|-----------------|----------------------------|
| Clarifying questions asked | Requires conversation history |
| Options offered per section | Requires conversation history |
| Revision cycles completed | Requires version tracking |
| Reader testing offered | Requires conversation history |
| User approvals | Requires interaction tracking |

These are valuable behaviors but fall outside CAPE's artifact verification model. They remain as skill guidance for runtime behavior.

---

## Not Verified (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Effective collaboration" | Subjective process quality | Retained as skill guidance |
| "High-quality document" | Multidimensional content quality | Structural checks only |
| "Appropriate tone" | Context-dependent | Retained as skill guidance |
| "Meets user's needs" | Subjective satisfaction | Retained as skill guidance |

---

## Configuration Reference

```json
{
  "configuration": {
    "allowed_formats": ["md", "docx", "txt", "pdf"],
    "min_word_count": 100,
    "min_section_count": 2,
    "min_section_word_count": 20,
    "max_heading_depth": 4
  }
}
```

Override thresholds at evaluation time to match your document requirements.
