# Mapping: xlsx

> **Source:** [anthropics/skills/document-skills/xlsx](https://github.com/anthropics/skills/tree/main/document-skills/xlsx)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed
>
> **Standard:** [ECMA-376 (Office Open XML - SpreadsheetML)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "create/edit .xlsx" | T1 | `is_zip_archive(file) == true` | Direct |
| 2 | "create/edit .xlsx" | T1 | `contains_file(file, 'xl/workbook.xml') == true` | Direct |
| 3 | "create/edit .xlsx" | T1 | `contains_file(file, '[Content_Types].xml') == true` | Direct |
| 4 | "create/edit .xlsx" | T1 | `xml_wellformed(file, ...) == true` | Direct |
| 5 | OOXML compliance | T1 | `xml_schema_valid(file, 'sml.xsd') == true` | Direct |
| 6 | Workbook structure | T1 | `sheet_count(file) > 0` | Direct |
| 7 | "support for formulas" | T2 | `formula_syntax_error_count(file) == 0` | Direct |
| 8 | "support for formulas" | T2 | `formula_reference_error_count(file) == 0` | Direct |
| 9 | "data analysis" | T2 | `type_mismatch_count(file) == 0` | Direct |
| 10 | Content preservation | T2 | `data_preserved(ctx.input, file) == true` | Direct |
| 11 | "visualization" | T2 | `charts_with_invalid_range_count(file) == 0` | Direct |
| 12 | "visualization" | T2 | `charts_with_missing_data_count(file) == 0` | Direct |
| 13 | "formatting" | T2 | `cell_styles_preserved(ctx.input, file) == true` | Direct |
| 14 | "formatting" | T2 | `conditional_formats_preserved(ctx.input, file) == true` | Direct |
| 15 | Named ranges | T2 | `invalid_named_range_count(file) == 0` | Direct |
| 16 | Calculation chain | T2 | `calc_chain_valid(file) == true` | Direct |

---

## Verification Approach

All predicates use **static file inspection**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| File structure | ZIP archive, required files |
| XML parsing | Well-formedness, schema validation |
| Formula parsing | Syntax errors, reference errors |
| Type checking | Cell value vs declared type |
| Content comparison | Data preservation, style preservation |
| Reference validation | Named ranges, chart ranges |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Structure, XML validity, has sheets | Invalid file = unusable |
| **T2** | Formulas, data types, preservation, charts, named ranges, calc chain | Data integrity concerns |

**Note:** No T3 predicates. Formatting and named ranges are T2 because:
- Lost formatting is data loss (conditional formatting encodes business logic)
- Broken named ranges cause formula errors
- Both are objectively verifiable integrity issues

---

## Workflow Handling

| Operation | Active Checks |
|-----------|---------------|
| **Create** | T1 (validity) + T2 (formulas, charts, data types) |
| **Edit** | T1 + T2 (all, including preservation checks) |
| **Analyze** | T1 only (extraction feasibility) |

---

## OOXML Structure Reference

A valid `.xlsx` file is a ZIP archive containing:

| Required file | Purpose |
|---------------|---------|
| `[Content_Types].xml` | MIME type mappings |
| `xl/workbook.xml` | Workbook structure |
| `xl/_rels/workbook.xml.rels` | Relationships |
| `xl/worksheets/sheet*.xml` | Worksheet content |
| `xl/sharedStrings.xml` | Shared string table |

Optional:
- `xl/styles.xml` — Cell styles
- `xl/calcChain.xml` — Calculation chain
- `xl/charts/*.xml` — Embedded charts
- `xl/media/*` — Embedded images

---

## Formula Validation

| Check | What it catches |
|-------|-----------------|
| Syntax errors | Missing parentheses, invalid operators |
| Reference errors | `#REF!` errors, invalid ranges |
| Circular references | Self-referential formulas |
| Unknown functions | Misspelled or unsupported functions |

Formula syntax is strictly defined by ECMA-376 Part 1.

---

## Data Type Validation

OOXML defines cell types:

| Type code | Meaning | Valid values |
|-----------|---------|--------------|
| `t="s"` | String | Index into shared strings |
| `t="n"` | Number | Numeric value |
| `t="b"` | Boolean | 0 or 1 |
| `t="d"` | Date | ISO 8601 date |
| `t="e"` | Error | Error codes (#REF!, #VALUE!, etc.) |
| (none) | Inline | Direct value |

A cell with type `n` containing non-numeric data is a schema violation.

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 6 | Static analysis |
| T2 (Integrity) | 10 | Static analysis |
| T3 (Quality) | 0 | Not applicable |
| **Total** | **16** | — |
