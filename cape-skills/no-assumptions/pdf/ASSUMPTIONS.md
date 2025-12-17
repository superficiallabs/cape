# Assumptions: pdf

> **Source:** [anthropics/skills/document-skills/pdf](https://github.com/anthropics/skills/tree/main/document-skills/pdf)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Category:** No assumptions needed
>
> **Standard:** [ISO 32000-1:2008 (PDF 1.7)](https://www.iso.org/standard/51502.html)

---

## No Assumptions Required

This skill falls into the **"No Assumptions Needed"** category. All requirements are derived directly from the ISO 32000 standard and mathematical properties of document operations.

### Why No Assumptions?

**1. Binary Validity**

A file is either a valid PDF or it isn't. The ISO 32000 standard defines:
- Required header (`%PDF-x.y`)
- Required trailer (`%%EOF`)
- Cross-reference table structure
- Object stream format

There is no subjectivity in "Is this a valid PDF?"

**2. Mathematical Integrity**

Document operations have mathematically verifiable properties:

**Merge:**
```
page_count(merged) = page_count(A) + page_count(B) + ... + page_count(N)
```

**Split:**
```
page_count(original) = page_count(part_1) + page_count(part_2) + ... + page_count(part_N)
```

These are arithmetic facts, not opinions.

**3. Explicit Form Data**

PDF forms (AcroForms) have explicit fields with typed values:
- Field names are strings
- Field values are deterministic
- Verifying `field["name"].value == "John"` is string comparison

Whether a form field contains the correct value is binary, not subjective.

---

## Verification Approach

All predicates use **static file inspection**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| Byte inspection | PDF header, EOF marker |
| Structure parsing | XRef table, page tree |
| Library parsing | `pdf_parser_succeeds` (PDF parsing library) |
| Text extraction | Parse text streams |
| Form inspection | AcroForm fields, values, types |
| Arithmetic | Page counts for merge/split |

**Note on `pdf_parser_succeeds`:** This uses a PDF parsing library (like PyPDF2, pdf-lib, etc.) to validate the file can be parsed. PDFs are documents, not programs—there is no "execution." This is structural validation, equivalent to parsing JSON or XML.

---

## What This Policy Verifies

### T1: Objective Correctness

| Check | Standard | What it verifies |
|-------|----------|------------------|
| PDF header | ISO 32000-1 §7.5.2 | File starts with `%PDF-` |
| EOF marker | ISO 32000-1 §7.5.9 | File ends with `%%EOF` |
| XRef table | ISO 32000-1 §7.5.8 | Valid cross-reference table |
| Parser accepts | Practical | Standard PDF parsers can read file |
| Version | ISO 32000-1 | PDF version ≥ 1.4 |
| Text extraction | ISO 32000-1 §9 | Text content is extractable |

### T2: Data Integrity

| Check | Standard | What it verifies |
|-------|----------|------------------|
| Form values match | AcroForm spec | Filled values equal requested values |
| Form field types | AcroForm spec | Values match field type constraints |
| Merge page count | Arithmetic | All source pages present |
| Split completeness | Arithmetic | All pages distributed |
| No duplicates | Set theory | No page appears in multiple parts |
| Form structure | AcroForm spec | Field names unchanged after fill |
| Metadata preserved | ISO 32000-1 §14.3 | Title/author not lost |

---

## Why Metadata/Form Structure as T2?

Metadata loss is data loss. Document title and author are data, not formatting preferences. Silently stripping them is an integrity failure.

Form structure modification is incorrect behavior. When filling a form, adding or removing fields is wrong—not just low quality.

These aren't subjective preferences—they're verifiable correctness requirements.

---

## Form Field Verification

AcroForms define field types with validation rules:

| Field Type | Validation |
|------------|------------|
| Text | String value, max length |
| Checkbox | Boolean (checked/unchecked) |
| Radio | One of allowed values |
| Dropdown | One of allowed options |
| Date | Valid date format |
| Number | Numeric value, range |

The policy verifies:
1. All requested fields exist
2. Values match requested values exactly
3. Values conform to field type constraints

---

## Potential T2 Security Extensions

The current policy focuses on correctness and integrity. For enterprise deployments, consider adding:

| Check | Rationale |
|-------|-----------|
| No JavaScript | Prevent code execution |
| No external links | Prevent data exfiltration |
| No embedded files | Prevent malware vectors |
| Encryption status | Verify expected protection |

These would be T2 (governance) checks added via configuration.

---

## Summary Table

| Constraint | Standard | Predicate | Tier |
|------------|----------|-----------|------|
| Valid PDF structure | ISO 32000-1 | `starts_with_pdf_header()`, `ends_with_eof_marker()`, `has_valid_xref()` | **T1** |
| Parser accepts | Practical | `pdf_parser_succeeds()` | **T1** |
| Version supported | ISO 32000-1 | `pdf_version() >= min` | **T1** |
| Text extractable | ISO 32000-1 | `text_extraction_succeeds()` | **T1** |
| Form values correct | AcroForm | `form_field_mismatch_count() == 0` | **T2** |
| Merge integrity | Arithmetic | `page_count() == sum()` | **T2** |
| Split integrity | Arithmetic | `sum(parts) == original` | **T2** |
| Form structure | AcroForm | `form_field_names() unchanged` | **T2** |
| Metadata preserved | ISO 32000-1 | `title_preserved()`, `author_preserved()` | **T2** |
