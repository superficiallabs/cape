# Specifiability Matrix

Complete analysis of all 16 Anthropic Agent Skills and their CAPE policy conversions.

> **Methodology:** See [METHODOLOGY.md](../METHODOLOGY.md) for the conversion process used in this analysis.
>
> **Last updated:** December 2025 | **Skills version:** anthropics/skills@v2024-10

---

## Summary

| Category | Count | Percentage |
|----------|------:|------------|
| No assumptions needed | 7 | 44% |
| Fixed assumptions required | 9 | 56% |
| **Total specifiable** | **16** | **100%** |

**Key finding:** 100% of skills are specifiable. The 56% requiring assumptions aren't "unverifiable"—they're underspecified. Making assumptions explicit converts subjective guidance into objective predicates.

---

## Core Principle: Static Verification Only

All predicates use **static analysis** of model outputs. No execution harnesses required.

| ✓ Static (used) | ✗ Execution (avoided) |
|-----------------|----------------------|
| File structure parsing | Running code |
| XML/JSON schema validation | Opening in applications |
| AST analysis | Rendering output |
| Pattern matching | Lighthouse/browser tests |
| Algorithmic metrics (contrast, entropy) | External API calls |

**Why?** CAPE verifies *outputs*, not *behaviors*. Whether code runs correctly when executed is downstream of whether the model produced structurally correct code.

---

## Tier Definitions

Based on the CAPE Protocol (Section 6.3):

| Tier | Name | Violation means | Example |
|------|------|-----------------|---------|
| **T1** | Objective Correctness | Hard failure—artifact is broken | Invalid syntax, wrong dimensions, corrupted file |
| **T2** | Governance/Safety | Compliance failure—artifact is unsafe | Brand violation, accessibility failure, PII exposure |
| **T3** | Structural Preference | Quality degradation—artifact works but is off-spec | Low complexity, poor tone, generic aesthetics |

---

## Category: No Assumptions Needed

These skills have clear, verifiable constraints that convert directly to predicates. All constraints are T1 (correctness) or T2 (governance) with no subjective interpretation required.

| Skill | Domain | Key Constraints | Primary Tiers |
|-------|--------|-----------------|---------------|
| [docx](#docx) | Document | Valid OOXML, content preserved, tracked changes metadata | T1, T2 |
| [pdf](#pdf) | Document | Valid PDF structure, form fields typed, text extractable | T1, T2 |
| [pptx](#pptx) | Document | Valid PPTX structure, slides complete, layouts valid | T1, T2 |
| [xlsx](#xlsx) | Document | Valid XLSX, formulas parse, types correct | T1, T2 |
| [webapp-testing](#webapp-testing) | Technical | Valid test syntax, assertions present, proper async | T1, T3 |
| [slack-gif-creator](#slack-gif-creator) | Technical | Size limit, dimensions, frame count, animation | T1, T3 |
| [artifacts-builder](#artifacts-builder) | Technical | Valid JSX, imports resolve, valid Tailwind, hooks rules | T1 |

---

## Category: Fixed Assumptions Required

These skills contain subjective guidance that requires explicit interpretation. We document assumptions in `ASSUMPTIONS.md` to make them verifiable.

| Skill | Domain | Subjective Guidance | Proxy Strategy | Primary Tiers |
|-------|--------|---------------------|----------------|---------------|
| [algorithmic-art](#algorithmic-art) | Creative | "gallery-quality art" | Code structure + image metrics | T1, T3 |
| [brand-guidelines](#brand-guidelines) | Enterprise | "on brand" | Exact color/font matching | T2 |
| [canvas-design](#canvas-design) | Creative | "beautiful visual art" | Format validity + palette compliance | T1, T2 |
| [doc-coauthoring](#doc-coauthoring) | Process | "effective collaboration" | Structure + content metrics | T1, T2, T3 |
| [frontend-design](#frontend-design) | Creative | "avoid AI slop" | Design token variety | T1, T2, T3 |
| [internal-comms](#internal-comms) | Enterprise | "professional tone" | Slang detection + sentiment + reading level | T2, T3 |
| [mcp-builder](#mcp-builder) | Technical | "high-quality MCP server" | Schema validation + code structure | T1 |
| [skill-creator](#skill-creator) | Meta | "effective skill" | Structure validation + content metrics | T1, T3 |
| [theme-factory](#theme-factory) | Creative | "professional themes" | Contrast ratios + CSS validity | T1, T2, T3 |

---

## Detailed Breakdown by Skill

### Document Skills

#### docx

**Category:** No assumptions needed

All verification via ZIP inspection, XML parsing, and schema validation.

| Constraint | Predicate | Tier |
|------------|-----------|------|
| Valid ZIP structure | `is_zip_archive(file) == true` | T1 |
| Required files present | `contains_file(file, 'word/document.xml') == true` | T1 |
| XML well-formed | `xml_wellformed(file, 'word/document.xml') == true` | T1 |
| Schema valid | `xml_schema_valid(file, 'wml.xsd') == true` | T1 |
| Content preserved on edit | `text_content_preserved(input, output) == true` | T2 |
| Tracked changes have metadata | `insertions_have_rsid(file) == true` | T2 |

#### pdf

**Category:** No assumptions needed

All verification via file header parsing, structure analysis, and form inspection.

| Constraint | Predicate | Tier |
|------------|-----------|------|
| Valid PDF header | `starts_with_pdf_header(file) == true` | T1 |
| Valid XRef table | `has_valid_xref(file) == true` | T1 |
| Parser succeeds | `pdf_parser_succeeds(file) == true` | T1 |
| Form fields typed correctly | `form_field_type_errors(file) == 0` | T2 |
| Merge page count correct | `page_count(merged) == sum(sources)` | T2 |

#### pptx

**Category:** No assumptions needed

All verification via ZIP inspection, XML parsing, and reference validation.

| Constraint | Predicate | Tier |
|------------|-----------|------|
| Valid ZIP structure | `is_zip_archive(file) == true` | T1 |
| Required files present | `contains_file(file, 'ppt/presentation.xml') == true` | T1 |
| Schema valid | `xml_schema_valid(file, 'pml.xsd') == true` | T1 |
| Slides structurally complete | `malformed_slide_count(file) == 0` | T1 |
| Media references resolve | `missing_media_count(file) == 0` | T2 |
| Layouts valid | `slides_with_invalid_layout_count(file) == 0` | T2 |

#### xlsx

**Category:** No assumptions needed

All verification via ZIP inspection, XML parsing, and formula/type analysis.

| Constraint | Predicate | Tier |
|------------|-----------|------|
| Valid ZIP structure | `is_zip_archive(file) == true` | T1 |
| Schema valid | `xml_schema_valid(file, 'sml.xsd') == true` | T1 |
| Has worksheets | `sheet_count(file) > 0` | T1 |
| Formulas parse | `formula_syntax_error_count(file) == 0` | T2 |
| Data types correct | `type_mismatch_count(file) == 0` | T2 |
| Named ranges valid | `invalid_named_range_count(file) == 0` | T2 |

---

### Technical Skills

#### webapp-testing

**Category:** No assumptions needed

CAPE verifies the model produced correct **test code**. Whether tests pass when executed is application correctness, not model capability.

| Constraint | Predicate | Tier |
|------------|-----------|------|
| Valid syntax | `syntax_valid(code) == true` | T1 |
| Tests defined | `test_count(code) > 0` | T1 |
| Assertions present | `tests_without_assertions_count(code) == 0` | T1 |
| Valid Playwright API | `invalid_playwright_method_count(code) == 0` | T1 |
| Proper async/await | `unawaited_async_count(code) == 0` | T1 |
| No hardcoded waits | `hardcoded_wait_count(code) == 0` | T3 |
| Descriptive names | `generic_test_name_count(code) == 0` | T3 |

#### slack-gif-creator

**Category:** No assumptions needed

All verification via GIF file header parsing and structure analysis.

| Constraint | Predicate | Tier | Source |
|------------|-----------|------|--------|
| Valid GIF89a format | `gif_format(file) == 'GIF89a'` | T1 | GIF spec |
| File size ≤ 64KB | `file_size_bytes(file) <= 65536` | T1 | Slack spec |
| Dimensions 128×128 | `width(file) == 128 && height(file) == 128` | T1 | Slack spec |
| Is animated | `frame_count(file) > 1` | T1 | Task requirement |
| Frame timing valid | `min_frame_delay_ms(file) >= 20` | T1 | Platform behavior |
| Color table valid | `color_table_size(file) <= 256` | T1 | GIF spec |
| No duplicate frames | `duplicate_frame_count(file) == 0` | T3 | Optimization |

#### artifacts-builder

**Category:** No assumptions needed

All verification via JSX parsing and AST analysis.

| Constraint | Predicate | Tier |
|------------|-----------|------|
| Valid JSX syntax | `valid_jsx_syntax(code) == true` | T1 |
| Imports resolve | `unresolved_import_count(code) == 0` | T1 |
| Valid Tailwind classes | `invalid_tailwind_class_count(code) == 0` | T1 |
| Hooks rules followed | `hooks_rules_violations(code) == 0` | T1 |
| Has default export | `has_default_export(code) == true` | T1 |

> **Note:** We intentionally do **not** verify complexity. Complexity is request-dependent—a simple button is correct if that's what the user asked for.

#### mcp-builder

**Category:** Fixed assumptions (minimal)

All verification via JSON schema validation and AST analysis.

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "valid MCP server" | Schema validates | `manifest_schema_valid(server) == true` | T1 |
| "valid MCP server" | Required handlers present | `has_endpoint_handler(server, 'list_tools') == true` | T1 |
| "valid MCP server" | Tools have implementations | `tools_without_handlers_count(server) == 0` | T1 |
| "high-quality" | Type definitions complete | `typescript_errors(code) == 0` | T1 |
| "high-quality" | Documentation present | `undocumented_tool_count(server) == 0` | T1 |

---

### Creative Skills

#### algorithmic-art

**Category:** Fixed assumptions

Code structure verified via AST; image metrics verified via static file analysis of the PNG output.

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "p5.js sketches" | Valid syntax | `syntax_valid(code) == true` | T1 |
| "p5.js sketches" | Has setup() | `has_function(code, 'setup') == true` | T1 |
| "p5.js sketches" | Has draw() | `has_function(code, 'draw') == true` | T1 |
| "seeded randomness" | Uses randomSeed | `calls_function(code, 'randomSeed') == true` | T1 |
| "gallery-quality" | High entropy | `shannon_entropy(image) >= config.min_entropy` | T3 |
| "gallery-quality" | Color diversity | `unique_color_count(image) >= config.min_colors` | T3 |

**Default thresholds:** `min_entropy: 4.5`, `min_colors: 4`

> **Note:** T3 image metrics use static file analysis (pixel histogram, entropy calculation). No rendering required—the model produces the PNG.

#### canvas-design

**Category:** Fixed assumptions

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "visual art" | Valid output format | `format(file) in ['png', 'svg', 'pdf']` | T1 |
| "design philosophies" | Dimensions match spec | `width(file) == spec.width` | T1 |
| "coherent" | Colors within palette | `off_palette_color_count(file, spec.palette) == 0` | T2 |

#### theme-factory

**Category:** Fixed assumptions

All verification via CSS parsing and color math.

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "professional themes" | Valid CSS syntax | `css_syntax_valid(theme) == true` | T1 |
| "professional themes" | Color variables defined | `missing_color_variable_count(theme) == 0` | T1 |
| "professional themes" | WCAG AA contrast | `min_contrast_ratio(theme) >= 4.5` | T2 |
| "professional themes" | Dark mode support | `has_dark_mode_query(theme) == true` | T2 |
| "consistent" | Type scale ratio | `type_scale_consistency(theme) >= config.min_consistency` | T3 |

#### frontend-design

**Category:** Fixed assumptions

All verification via HTML/CSS parsing and static analysis.

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "valid HTML" | W3C valid | `html_parse_error_count(html) == 0` | T1 |
| "valid CSS" | CSS parses | `css_parse_error_count(css) == 0` | T1 |
| "accessible" | Contrast ratios | `wcag_contrast_violations(css) == 0` | T2 |
| "accessible" | ARIA attributes | `missing_aria_count(html) == 0` | T2 |
| "avoid AI slop" | Border-radius variety | `unique_border_radius_count(css) >= 3` | T3 |
| "avoid AI slop" | Font-size variety | `unique_font_size_count(css) >= 3` | T3 |
| "avoid AI slop" | Controlled fonts | `font_family_count(css) <= 3` | T3 |

**Default thresholds:** `min_border_radius_variety: 3`, `min_font_size_variety: 3`, `max_font_families: 3`

See [frontend-design/ASSUMPTIONS.md](../fixed-assumptions/frontend-design/ASSUMPTIONS.md) for rationale.

---

### Enterprise Skills

#### brand-guidelines

**Category:** Fixed assumptions

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "official brand colors" | Exact hex match | `off_brand_color_count(output, config.colors) == 0` | T2 |
| "typography" | Specified fonts only | `off_brand_font_count(output, config.fonts) == 0` | T2 |
| "consistent spacing" | Spacing uses brand scale | `off_scale_spacing_count(output, config.spacing) == 0` | T2 |

> **Note:** Brand guidelines are T2 (governance) because brand violations are compliance failures, not mere quality issues.

#### internal-comms

**Category:** Fixed assumptions

All verification via text analysis (deterministic algorithms, not LLM judgment).

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "professional" | No slang | `slang_match_count(text, config.slang_list) == 0` | T3 |
| "professional" | Neutral+ sentiment | `sentiment_score(text) >= config.min_sentiment` | T3 |
| "clear" | Reading level | `flesch_kincaid_grade(text) <= config.max_grade` | T3 |
| "structured" | Has required sections | `has_required_sections(text, config.sections) == true` | T2 |
| "attribution" | Has author | `has_author(text) == true` | T2 |

**Default thresholds:** `min_sentiment: 0.0`, `max_grade: 10`

---

### Meta Skills

#### skill-creator

**Category:** Fixed assumptions

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "effective skills" | Valid YAML frontmatter | `yaml_frontmatter_valid(skill) == true` | T1 |
| "effective skills" | Required fields present | `missing_required_field_count(skill) == 0` | T1 |
| "effective skills" | Name matches directory | `name_matches_directory(skill) == true` | T1 |
| "effective skills" | Description sufficient | `description_length(skill) >= config.min_length` | T3 |

**Default thresholds:** `min_description_length: 50`

#### doc-coauthoring

**Category:** Fixed assumptions

| Original Guidance | Assumption | Predicate | Tier |
|-------------------|------------|-----------|------|
| "structured workflow" | Has required sections | `has_required_sections(doc) == true` | T1 |
| "effective collaboration" | Questions present | `question_count(doc) >= config.min_questions` | T2 |
| "produces document" | Output complete | `word_count(doc) >= config.min_words` | T1 |
| "produces document" | No orphan headings | `orphan_heading_count(doc) == 0` | T3 |

**Default thresholds:** `min_questions: 3`, `min_words: 100`

---

## Limitations

This analysis captures what's verifiable through static analysis. The following remain outside policy scope:

| Limitation | Example | Why |
|------------|---------|-----|
| Aesthetic quality | "Is this beautiful?" | No structural proxy correlates reliably |
| Runtime behavior | "Does this code work?" | Requires execution harness |
| Creative novelty | "Is this original?" | Requires corpus comparison |
| Semantic correctness | "Is this factually accurate?" | Requires domain knowledge |
| Contextual fit | "Is this right for the audience?" | Requires context specification |

These require either human judgment, execution environments, or additional context not present in the source skills.

---

## Extending This Analysis

To add T2 security constraints to document skills (recommended for enterprise):

```json
{
  "id": "policy.docx.security",
  "tier": "T2",
  "assert": [
    { "expr": "macro_count(file) == 0", "msg": "Contains macros" },
    { "expr": "external_link_count(file) == 0", "msg": "Contains external links" },
    { "expr": "embedded_object_count(file) == 0", "msg": "Contains embedded objects" }
  ]
}
```

Similar extensions apply to PDF (no JavaScript), XLSX (no macros), and PPTX (no external media).
