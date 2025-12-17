# Assumptions: xlsx

> **Source:** [anthropics/skills/document-skills/xlsx](https://github.com/anthropics/skills/tree/main/document-skills/xlsx)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Category:** No assumptions needed
>
> **Standard:** [ECMA-376 (Office Open XML - SpreadsheetML)](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/)

---

## No Assumptions Required

This skill falls into the **"No Assumptions Needed"** category. All requirements are derived from the ECMA-376 standard for SpreadsheetML and mathematical properties of spreadsheet editing.

### Why No Assumptions?

**1. Strict Schema Definition**

An `.xlsx` file is a ZIP archive containing XML that must adhere to the SpreadsheetML schema (`sml.xsd`). Either the file conforms or it doesn't—there's no subjectivity.

**2. Formula Determinism**

Formula syntax is strictly defined by the standard:
- `=SUM(A1:A10)` — valid
- `=SUM(A1:A)` — invalid (incomplete range)
- `=SUM(A1:A10` — invalid (missing parenthesis)

A formula parser can deterministically identify syntax errors.

**3. Type Safety**

OOXML defines cell types explicitly:
- `t="s"` for strings
- `t="n"` for numbers
- `t="b"` for booleans

A numeric cell containing text is an objective schema violation.

**4. Data Preservation is Mathematical**

For edit operations:
```
original_cells ⊆ (output_cells ∪ deleted_cells)
```

If data from the original is missing and not marked as deleted, that's data loss—an objective failure.

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

## What This Policy Verifies

### T1: Objective Correctness

| Check | Standard | What it verifies |
|-------|----------|------------------|
| ZIP structure | ECMA-376 Part 2 | File is valid ZIP archive |
| Required files | ECMA-376 Part 1 | `xl/workbook.xml` and `[Content_Types].xml` exist |
| XML well-formed | W3C XML 1.0 | Workbook XML parses without errors |
| Schema valid | ECMA-376 Part 4 | XML conforms to SpreadsheetML schema |
| Has sheets | ECMA-376 Part 1 | At least one worksheet exists |

### T2: Data Integrity

| Check | Standard | What it verifies |
|-------|----------|------------------|
| Formula syntax | ECMA-376 Part 1 | All formulas parse correctly |
| Formula references | ECMA-376 Part 1 | Cell references resolve |
| Data types | ECMA-376 Part 1 | Values match declared types |
| Data preserved | Set theory | No silent data loss during edits |
| Charts valid | DrawingML | Charts have valid data ranges |
| Formatting preserved | ECMA-376 Part 1 | Styles not lost during edits |
| Conditional formatting | ECMA-376 Part 1 | Conditional rules preserved |
| Named ranges | ECMA-376 Part 1 | Named ranges have valid references |
| Calc chain | ECMA-376 Part 1 | Calculation order is valid |

---

## Why Formatting as T2?

Formatting is T2 (integrity), not T3 (quality preference), because:

**1. Conditional formatting encodes business logic.**
A spreadsheet where cells turn red when values exceed thresholds isn't just "pretty"—it's functional. Losing that conditional formatting breaks the spreadsheet's purpose.

**2. Cell styles can encode meaning.**
Currency formatting, percentage formatting, and date formatting affect how users interpret data. Losing these is a semantic change, not just aesthetic.

**3. It's objectively verifiable.**
Style preservation is a deterministic comparison—no subjective judgment required.

---

## Why Named Ranges as T2?

Broken named ranges cause formula errors. A formula like `=SUM(SalesData)` fails if the `SalesData` named range is invalid. This is an integrity issue, not a quality preference.

---

## Formula Validation Details

| Error type | Example | Detection |
|------------|---------|-----------|
| Syntax error | `=SUM(A1:A10` | Parser failure |
| Reference error | `=A1:ZZZ999999` | Invalid range |
| Circular reference | `A1 = A1 + 1` | Dependency analysis |
| Unknown function | `=SUMM(A1:A10)` | Function lookup |
| Type error | `="text" + 5` | Type checking |

---

## Data Type Validation

| Type | XML attribute | Valid content |
|------|---------------|---------------|
| String | `t="s"` | Index into sharedStrings.xml |
| Number | `t="n"` | Numeric value (integer or float) |
| Boolean | `t="b"` | `0` or `1` |
| Date | `t="d"` | ISO 8601 date string |
| Error | `t="e"` | Error code (#REF!, #VALUE!, etc.) |
| Inline string | `t="inlineStr"` | Direct string value |
| Formula | (none, with `<f>`) | Formula expression |

A cell with `t="n"` containing `"hello"` is invalid.

---

## Potential Security Extensions

For enterprise deployments, consider adding T2 checks:

| Check | Rationale |
|-------|-----------|
| No macros (VBA) | Prevent code execution |
| No external links | Prevent data exfiltration |
| No external data connections | Prevent uncontrolled data refresh |
| Metadata scrubbed | Prevent information leakage |

---

## Configuration Reference

```json
{
  "configuration": {
    "max_file_size_mb": 50,
    "require_calc_chain": true
  }
}
```

**`require_calc_chain`:** When `true`, verifies the calculation chain (`xl/calcChain.xml`) is present and valid. Important for spreadsheets with complex formula dependencies.

---

## Summary Table

| Constraint | Standard | Predicate | Tier |
|------------|----------|-----------|------|
| Valid OOXML structure | ECMA-376 | `is_zip_archive()`, `contains_file()` | **T1** |
| Well-formed XML | W3C XML | `xml_wellformed()` | **T1** |
| Schema compliance | ECMA-376 | `xml_schema_valid()` | **T1** |
| Has worksheets | ECMA-376 | `sheet_count() > 0` | **T1** |
| Formula syntax | ECMA-376 | `formula_syntax_error_count() == 0` | **T2** |
| Formula references | ECMA-376 | `formula_reference_error_count() == 0` | **T2** |
| Data types correct | ECMA-376 | `type_mismatch_count() == 0` | **T2** |
| Data preserved | Set theory | `data_preserved() == true` | **T2** |
| Charts valid | DrawingML | `charts_with_invalid_range_count() == 0` | **T2** |
| Formatting preserved | ECMA-376 | `cell_styles_preserved()`, `conditional_formats_preserved()` | **T2** |
| Named ranges valid | ECMA-376 | `invalid_named_range_count() == 0` | **T2** |
| Calc chain valid | ECMA-376 | `calc_chain_valid() == true` | **T2** |
