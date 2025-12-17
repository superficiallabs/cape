# Mapping: pdf

> **Source:** [anthropics/skills/document-skills/pdf](https://github.com/anthropics/skills/tree/main/document-skills/pdf)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed
>
> **Standard:** [ISO 32000-1:2008 (PDF 1.7)](https://www.iso.org/standard/51502.html)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "create new PDF" | T1 | `starts_with_pdf_header(file) == true` | Direct |
| 2 | "create new PDF" | T1 | `ends_with_eof_marker(file) == true` | Direct |
| 3 | "create new PDF" | T1 | `has_valid_xref(file) == true` | Direct |
| 4 | "create new PDF" | T1 | `pdf_parser_succeeds(file) == true` | Direct |
| 5 | PDF version | T1 | `pdf_version(file) >= config.min_pdf_version` | Direct |
| 6 | "extract text" | T1 | `text_extraction_succeeds(file) == true` | Direct |
| 7 | "fill PDF form" | T2 | `form_field_mismatch_count(file, ...) == 0` | Direct |
| 8 | "fill PDF form" | T2 | `form_field_type_errors(file) == 0` | Direct |
| 9 | "merging" | T2 | `page_count(file) == sum_page_counts(sources)` | Direct |
| 10 | "splitting" | T2 | `sum_page_counts(parts) == page_count(original)` | Direct |
| 11 | "splitting" | T2 | `no_duplicate_pages(parts) == true` | Direct |
| 12 | "structure preserved" | T2 | `form_field_names(file) == form_field_names(input)` | Direct |
| 13 | Metadata | T2 | `title_preserved(input, file) == true` | Direct |
| 14 | Metadata | T2 | `author_preserved(input, file) == true` | Direct |

---

## Verification Approach

All predicates use **static file inspection**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| Byte inspection | PDF header, EOF marker |
| Structure parsing | XRef table, page tree |
| Library parsing | `pdf_parser_succeeds` (uses PDF parsing library like PyPDF2) |
| Text extraction | Parse text streams |
| Form inspection | AcroForm fields, values, types |
| Arithmetic | Page counts for merge/split |
| Comparison | Metadata, field structure |

**Note on `pdf_parser_succeeds`:** This is static parsing validation—a PDF library attempts to parse the file structure. It does not "execute" the PDF (PDFs are documents, not programs). This is analogous to a JSON parser validating JSON.

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Structure, parser, version, text extraction | Invalid file = unusable |
| **T2** | Form values, merge/split integrity, structure preservation, metadata | Data integrity concerns |

**Note:** No T3 predicates. All PDF requirements are either correctness (T1) or integrity (T2). There are no subjective quality preferences.

---

## Workflow Handling

The policy uses conditional checks (`where` clauses) to handle different operations:

| Operation | Active Checks |
|-----------|---------------|
| **Create** | T1 (structure validity) |
| **Extract** | T1 (structure + text extraction) |
| **Merge** | T1 + T2 (page count integrity) |
| **Split** | T1 + T2 (page distribution + no duplicates) |
| **Form Fill** | T1 + T2 (field values + structure preservation) |

---

## PDF Structure Reference

A valid PDF file must have:

| Component | Requirement | Standard |
|-----------|-------------|----------|
| Header | Starts with `%PDF-x.y` | ISO 32000-1 §7.5.2 |
| Body | Objects and streams | ISO 32000-1 §7.5.4-7 |
| XRef Table | Cross-reference table | ISO 32000-1 §7.5.8 |
| Trailer | Ends with `%%EOF` | ISO 32000-1 §7.5.9 |

---

## Operation Integrity Logic

### Merge Operation
```
page_count(merged) = Σ page_count(source_i)
```
All pages from all source documents must be present in the merged output.

### Split Operation
```
Σ page_count(part_i) = page_count(original)
∩ page_ranges(part_i, part_j) = ∅  (for i ≠ j)
```
All pages must be distributed across parts with no duplicates.

### Form Fill Operation
```
∀ (field, value) ∈ requested: output[field] = value
field_names(output) = field_names(input)
```
Values must match exactly; field structure must not change.

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 6 | Fully verified |
| T2 (Integrity) | 8 | Fully verified |
| T3 (Quality) | 0 | Not applicable |
| **Total** | **14** | — |
