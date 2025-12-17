# Assumptions: docx

> **Source:** [anthropics/skills/document-skills/docx](https://github.com/anthropics/skills/tree/main/document-skills/docx)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Category:** No assumptions needed
>
> **Standard:** [ECMA-376 (Office Open XML)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

---

## No Assumptions Required

This skill falls into the **"No Assumptions Needed"** category. All requirements are derived directly from the OOXML standard (ECMA-376) and mathematical properties of document editing.

### Why No Assumptions?

**1. Strict Schema Definition**

A `.docx` file is either valid OOXML or it isn't. The ECMA-376 standard defines:
- Required file structure (ZIP containing specific XML files)
- XML schema (WordprocessingML)
- Element semantics

There is no subjectivity in "Is this a valid document?"

**2. Explicit Content Semantics**

The definition of "editing" is mathematically provable:

```
original_text ⊆ (output_text ∪ deleted_text)
```

If text from the original is missing from the output AND not marked as deleted, that's data loss—an objective failure.

**3. Standardized Metadata**

Tracked changes and comments have specific XML tags defined by the standard:
- `<w:ins>` — Insertions
- `<w:del>` — Deletions
- `<w:comment>` — Comments
- `w:rsid` attribute — Revision session ID
- `w:author` attribute — Author identification

Whether these exist and are well-formed is binary, not subjective.

---

## Verification Approach

All predicates use **static file inspection**. No execution required.

A `.docx` file is a ZIP archive containing XML files. Verification involves:
1. Checking ZIP structure and required files
2. Parsing XML and validating against schema
3. Inspecting specific elements for metadata
4. Diffing content between input and output (for edits)

---

## What This Policy Verifies

### T1: Objective Correctness

| Check | Standard | What it verifies |
|-------|----------|------------------|
| ZIP structure | ECMA-376 Part 2 | File is valid ZIP archive |
| Required files | ECMA-376 Part 1 | `word/document.xml` and `[Content_Types].xml` exist |
| XML well-formed | W3C XML 1.0 | Document XML parses without errors |
| Schema valid | ECMA-376 Part 4 | XML conforms to WordprocessingML schema |

### T2: Data Integrity

| Check | Standard | What it verifies |
|-------|----------|------------------|
| Content preserved | Set theory | No silent data loss during edits |
| Tracked changes valid | ECMA-376 Part 1 | Insertions/deletions have required metadata |
| Comments anchored | ECMA-376 Part 1 | Comments reference valid document locations |
| Formatting preserved | Practical | Styles and fonts not unintentionally modified |
| Redlining enforced | Configuration | Tracked changes present when required |

---

## Why T2 for Data Integrity (Not T1)?

Data integrity issues don't make the file invalid—they make it incorrect for the use case:

- A file with silent deletions still opens (T1 passes)
- But the user's content is lost (T2 fails)

This distinction matters for error handling:
- T1 failure → file is broken, cannot proceed
- T2 failure → file is usable but may have data issues

---

## Formatting Preservation: Why T2?

Formatting preservation during edits is T2 (integrity), not T3 (preference), because:

1. **Unintentional changes are defects.** If the user asks to "add a paragraph," changing all fonts is incorrect.

2. **It's objectively verifiable.** We can diff styles before and after—no subjective judgment needed.

3. **It's not about preference.** "Preserve formatting" isn't asking "do you like this font?"—it's asking "did you change something you shouldn't have?"

---

## Configuration Options

| Option | Default | Purpose |
|--------|---------|---------|
| `max_file_size_mb` | 50 | Reject oversized files |
| `require_tracked_changes` | false | Enable for redlining workflows |

When `require_tracked_changes: true`, all edit operations must include tracked changes, enabling audit trails.

---

## Summary Table

| Constraint | Standard | Predicate | Tier |
|------------|----------|-----------|------|
| Valid OOXML structure | ECMA-376 | `is_zip_archive()`, `contains_file()` | **T1** |
| Well-formed XML | W3C XML | `xml_wellformed()` | **T1** |
| Schema compliance | ECMA-376 | `xml_schema_valid()` | **T1** |
| Content preserved | Set theory | `text_content_preserved()` | **T2** |
| Tracked changes valid | ECMA-376 | `insertions_have_rsid()`, etc. | **T2** |
| Comments intact | ECMA-376 | `orphaned_comment_count()` | **T2** |
| Formatting preserved | Practical | `styles_preserved()`, `fonts_preserved()` | **T2** |

---

## Potential T2 Security Extensions

The current policy focuses on correctness and integrity. For enterprise deployments, consider adding:

| Check | Rationale |
|-------|-----------|
| No macros | Prevent code execution |
| No external links | Prevent data exfiltration |
| No embedded objects | Prevent malware vectors |
| Metadata scrubbed | Prevent information leakage |

These would be T2 (governance) checks added via configuration.
