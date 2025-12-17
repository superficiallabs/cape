# Assumptions: pptx

> **Source:** [anthropics/skills/document-skills/pptx](https://github.com/anthropics/skills/tree/main/document-skills/pptx)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Category:** No assumptions needed
>
> **Standard:** [ECMA-376 (Office Open XML - PresentationML)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

---

## No Assumptions Required

This skill falls into the **"No Assumptions Needed"** category. All requirements are derived directly from the ECMA-376 standard for PresentationML and structural validation.

### Why No Assumptions?

**1. Strict Schema Definition**

A `.pptx` file is a ZIP archive containing XML that must adhere to the PresentationML schema (`pml.xsd`). Either the file conforms or it doesn't—there's no subjectivity.

**2. Structural Integrity**

While "does it render beautifully" is subjective, "is the structure valid" is objective:
- Invalid geometry coordinates → schema violation
- Corrupt shape definitions → XML error
- Missing references → broken links

We verify structure, not aesthetics.

**3. Reference Resolution**

A presentation referencing missing media is objectively broken:
- Image reference without file → broken reference
- Layout reference to non-existent layout → invalid structure
- Chart without data → empty visualization

These are binary facts, not subjective judgments.

---

## Verification Approach

All predicates use **static file inspection**. No execution or rendering required.

| Analysis Type | Predicates |
|---------------|------------|
| File structure | ZIP archive, required files |
| XML parsing | Well-formedness, schema validation |
| Reference validation | Media, layouts, shapes |
| Content comparison | Speaker notes preservation |
| Arithmetic | Slide counts |

---

## What This Policy Verifies

### T1: Objective Correctness

| Check | Standard | What it verifies |
|-------|----------|------------------|
| ZIP structure | ECMA-376 Part 2 | File is valid ZIP archive |
| Required files | ECMA-376 Part 1 | `ppt/presentation.xml` and `[Content_Types].xml` exist |
| XML well-formed | W3C XML 1.0 | Presentation XML parses without errors |
| Schema valid | ECMA-376 Part 4 | XML conforms to PresentationML schema |
| Slides valid | ECMA-376 Part 1 | No malformed slides or broken shape references |

### T2: Data Integrity

| Check | Standard | What it verifies |
|-------|----------|------------------|
| Media embedded | ECMA-376 Part 1 | All media references resolve to files |
| Charts valid | ECMA-376 DrawingML | Charts have data series |
| Slide count | Arithmetic | Expected slides present after edit |
| Layouts applied | ECMA-376 Part 1 | Slides have valid layout references |
| Speaker notes | ECMA-376 Part 1 | Notes preserved during edits |
| Template consistent | ECMA-376 Part 1 | Valid slide master, no orphaned layouts |

---

## Why Speaker Notes and Templates as T2?

**Speaker notes are content.** Losing speaker notes during an edit is data loss—the same tier as losing slides. It's not a quality preference; it's an integrity failure.

**Broken templates cause incorrect output.** A slide referencing a non-existent layout or orphaned master causes structural issues. This is an integrity problem, not an aesthetic preference.

Both are objectively verifiable—no subjective judgment required.

---

## Not Mapped (Would Require Execution)

| Guidance | Why not mapped |
|----------|----------------|
| "Slides render" | Requires rendering engine |
| "Opens in PowerPoint" | Requires running PowerPoint |
| "Media playable" | Requires media player |
| "Charts render" | Requires chart rendering |

These are verified via structural proxies:
- Valid XML + schema compliance → likely to render
- References resolved → media will load
- Chart has data → chart will display

---

## Media Integrity

The policy verifies all media references resolve:

| Media Type | Verification |
|------------|--------------|
| Images | File exists in `ppt/media/`, referenced in relationships |
| Videos | File exists, relationship valid |
| Audio | File exists, relationship valid |

Missing media is a T2 failure—the presentation is incomplete.

---

## Chart Validation

Charts in PowerPoint are DrawingML objects with embedded data:

| Check | What it catches |
|-------|-----------------|
| Data present | Charts with no data series |
| XML valid | Charts with malformed definitions |

A chart without data is an integrity failure.

---

## Potential T2 Security Extensions

For enterprise deployments, consider adding:

| Check | Rationale |
|-------|-----------|
| No macros | Prevent code execution |
| No external media links | Prevent data exfiltration |
| No embedded objects | Prevent malware vectors |
| Metadata scrubbed | Prevent information leakage |

---

## Summary Table

| Constraint | Standard | Predicate | Tier |
|------------|----------|-----------|------|
| Valid OOXML structure | ECMA-376 | `is_zip_archive()`, `contains_file()` | **T1** |
| Well-formed XML | W3C XML | `xml_wellformed()` | **T1** |
| Schema compliance | ECMA-376 | `xml_schema_valid()` | **T1** |
| Slides valid | ECMA-376 | `malformed_slide_count()`, `broken_shape_reference_count()` | **T1** |
| Media embedded | ECMA-376 | `missing_media_count()` | **T2** |
| Charts valid | DrawingML | `charts_missing_data_count()` | **T2** |
| Slide count preserved | Arithmetic | `slide_count_matches_expected()` | **T2** |
| Layouts valid | ECMA-376 | `slides_with_invalid_layout_count()` | **T2** |
| Speaker notes preserved | ECMA-376 | `speaker_notes_preserved()` | **T2** |
| Template consistent | ECMA-376 | `has_valid_master()`, `orphaned_layout_count()` | **T2** |
