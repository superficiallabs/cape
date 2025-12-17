# Mapping: docx

> **Source:** [anthropics/skills/document-skills/docx](https://github.com/anthropics/skills/tree/main/document-skills/docx)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed
>
> **Standard:** [ECMA-376 (Office Open XML)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "create/edit .docx" | T1 | `is_zip_archive(file) == true` | Direct |
| 2 | "create/edit .docx" | T1 | `contains_file(file, 'word/document.xml') == true` | Direct |
| 3 | "create/edit .docx" | T1 | `contains_file(file, '[Content_Types].xml') == true` | Direct |
| 4 | ".docx is ZIP of XML" | T1 | `xml_wellformed(file, 'word/document.xml') == true` | Direct |
| 5 | OOXML compliance | T1 | `xml_schema_valid(file, 'wml.xsd') == true` | Direct |
| 6 | Content preservation | T2 | `text_content_preserved(ctx.input, file) == true` | Direct |
| 7 | "preserve original run's RSID" | T2 | `insertions_have_rsid(file) == true` | Direct |
| 8 | "preserve original run's RSID" | T2 | `deletions_have_rsid(file) == true` | Direct |
| 9 | Tracked changes | T2 | `insertions_have_author(file) == true` | Direct |
| 10 | Tracked changes | T2 | `deletions_have_author(file) == true` | Direct |
| 11 | "Comments referenced" | T2 | `orphaned_comment_count(file) == 0` | Direct |
| 12 | Formatting preservation | T2 | `styles_preserved(ctx.input, file) == true` | Direct |
| 13 | Formatting preservation | T2 | `fonts_preserved(ctx.input, file) == true` | Direct |
| 14 | Redlining workflow | T2 | `has_tracked_changes(file) == true` (conditional) | Direct |

---

## Verification Approach

All predicates use **static file inspection**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| File structure | ZIP archive check, file presence |
| XML parsing | Well-formedness, parse errors |
| Schema validation | OOXML schema conformance |
| XML inspection | Tracked changes metadata, comments |
| Content diff | Text preservation, style preservation |

A `.docx` file is a ZIP archive containing XML files. All verification is done by inspecting the archive contents and parsing the XML.

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Structure, XML validity, schema | Invalid file = unusable |
| **T2** | Content preservation, tracked changes, comments, formatting | Data integrity and audit trail |

**Note:** No T3 predicates. All DOCX requirements are either correctness (T1) or integrity (T2). There are no subjective quality preferences to verify.

---

## Workflow Handling

The policy uses conditional checks (`where` clauses) to handle different workflows:

| Workflow | Active Checks |
|----------|---------------|
| **Create** | T1 only (structure validity) |
| **Edit** | T1 + T2 (content/formatting preservation) |
| **Redline** | T1 + T2 + tracked changes required |

**How it works:**
- `is_edit_operation(ctx)` detects when an input file exists
- `config.require_tracked_changes` enables redlining enforcement
- Checks that don't apply are skipped via `where` conditions

---

## OOXML Structure Reference

A valid `.docx` file is a ZIP archive containing:

| Required file | Purpose |
|---------------|---------|
| `[Content_Types].xml` | MIME type mappings |
| `word/document.xml` | Main document content |
| `word/_rels/document.xml.rels` | Relationships |

Optional but common:
- `word/styles.xml` — Style definitions
- `word/comments.xml` — Comments
- `word/settings.xml` — Document settings
- `word/media/*` — Embedded images

---

## Content Preservation Logic

For edit operations, we verify:

```
original_text ⊆ (output_text ∪ deleted_text)
```

Where:
- `original_text` = all text in input document
- `output_text` = all text in output document
- `deleted_text` = text marked with `<w:del>` tracked changes

This ensures no content is silently lost—deletions must be explicit.

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 5 | Fully verified |
| T2 (Integrity) | 9 | Fully verified |
| T3 (Quality) | 0 | Not applicable |
| **Total** | **14** | — |
