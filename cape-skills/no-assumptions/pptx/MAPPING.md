# Mapping: pptx

> **Source:** [anthropics/skills/document-skills/pptx](https://github.com/anthropics/skills/tree/main/document-skills/pptx)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed
>
> **Standard:** [ECMA-376 (Office Open XML - PresentationML)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "valid pptx" | T1 | `is_zip_archive(file) == true` | Direct |
| 2 | "valid pptx" | T1 | `contains_file(file, 'ppt/presentation.xml') == true` | Direct |
| 3 | "valid pptx" | T1 | `contains_file(file, '[Content_Types].xml') == true` | Direct |
| 4 | "valid pptx" | T1 | `xml_wellformed(file, ...) == true` | Direct |
| 5 | OOXML compliance | T1 | `xml_schema_valid(file, 'pml.xsd') == true` | Direct |
| 6 | "slides render" | T1 | `malformed_slide_count(file) == 0` | Direct |
| 7 | "slides render" | T1 | `broken_shape_reference_count(file) == 0` | Direct |
| 8 | "media" | T2 | `missing_media_count(file) == 0` | Direct |
| 9 | "charts" | T2 | `charts_missing_data_count(file) == 0` | Direct |
| 10 | Edit integrity | T2 | `slide_count_matches_expected(file, ctx) == true` | Direct |
| 11 | "layouts" | T2 | `slides_with_invalid_layout_count(file) == 0` | Direct |
| 12 | "speaker notes" | T2 | `speaker_notes_preserved(ctx.input, file) == true` | Direct |
| 13 | "templates" | T2 | `has_valid_master(file) == true` | Direct |
| 14 | "templates" | T2 | `orphaned_layout_count(file) == 0` | Direct |

---

## Verification Approach

All predicates use **static file inspection**. No execution or rendering required.

| Analysis Type | Predicates |
|---------------|------------|
| File structure | ZIP archive, required files |
| XML parsing | Well-formedness, parse errors |
| Schema validation | PresentationML conformance |
| XML inspection | Slides, shapes, references |
| Reference validation | Media files, layout references |
| Content comparison | Speaker notes preservation |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Structure, XML, schema, slide structure | Invalid file = unusable |
| **T2** | Media, charts, slide count, layouts, notes, templates | Data integrity concerns |

**Note:** No T3 predicates. Speaker notes and template consistency are T2 because:
- Lost speaker notes = data loss (integrity issue)
- Broken layouts/templates = incorrect output (not just quality preference)

---

## Not Mapped (Would Require Execution)

| Guidance | Why not mapped |
|----------|----------------|
| "Slides render correctly" | Requires rendering engine |
| "Opens in PowerPoint" | Requires running PowerPoint |
| "Media playable" | Requires media player |
| "Charts render" | Requires chart rendering |

These are verified via structural proxies (valid XML, schema compliance, references resolved) rather than runtime behavior.

---

## Workflow Handling

| Operation | Active Checks |
|-----------|---------------|
| **Create** | T1 (validity) + T2 (media, charts) |
| **Edit** | T1 + T2 (all, including notes preservation) |
| **Analyze** | T1 only (extraction feasibility) |

---

## OOXML Structure Reference

A valid `.pptx` file is a ZIP archive containing:

| Required file | Purpose |
|---------------|---------|
| `[Content_Types].xml` | MIME type mappings |
| `ppt/presentation.xml` | Main presentation structure |
| `ppt/_rels/presentation.xml.rels` | Relationships |
| `ppt/slides/slide*.xml` | Individual slide content |
| `ppt/slideMasters/slideMaster*.xml` | Slide master definitions |
| `ppt/slideLayouts/slideLayout*.xml` | Layout definitions |

Optional:
- `ppt/media/*` — Embedded images, videos, audio
- `ppt/charts/*` — Chart definitions
- `ppt/notesSlides/*` — Speaker notes

---

## Slide Count Integrity

For edit operations:
```
expected_count = original_count + additions - deletions
actual_count = slide_count(output)
```

If `actual_count ≠ expected_count`, slides were unexpectedly added or lost.

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 7 | Static analysis |
| T2 (Integrity) | 7 | Static analysis |
| T3 (Quality) | 0 | Not applicable |
| **Total** | **14** | — |
