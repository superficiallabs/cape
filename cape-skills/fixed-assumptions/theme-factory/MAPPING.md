# Mapping: theme-factory

> **Source:** [anthropics/skills/theme-factory](https://github.com/anthropics/skills/tree/main/theme-factory)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)
>
> **Reference:** [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | Valid CSS output | T1 | `css_syntax_valid(output) == true` | Direct |
| 2 | Valid CSS output | T1 | `css_parse_error_count(output) == 0` | Direct |
| 3 | Valid CSS output | T1 | `invalid_property_count(output) == 0` | Direct |
| 4 | "10 pre-set themes" | T1 | `has_color_definitions(output) == true` | Direct |
| 5 | "10 pre-set themes" | T1 | `has_typography_definitions(output) == true` | Direct |
| 6 | "10 pre-set themes" | T1 | `has_spacing_definitions(output) == true` | Direct |
| 7 | "professional" | T2 | `min_text_contrast_ratio(output) >= 4.5` | Direct |
| 8 | "professional" | T2 | `min_ui_contrast_ratio(output) >= 3.0` | Direct |
| 9 | "professional" | T2 | `has_dark_mode_variant(output) == true` | Direct |
| 10 | "professional" | T2 | `dark_mode_contrast_valid(output) == true` | Direct |
| 11 | "professional" | T3 | `base_font_size_px(output) >= 14` | Proxy |
| 12 | "professional" | T3 | `base_line_height(output) >= 1.4` | Proxy |
| 13 | "professional" | T3 | `font_family_count(output) <= 3` | Proxy |
| 14 | "consistent" | T3 | `has_type_scale(output) == true` | Proxy |
| 15 | "consistent" | T3 | `type_scale_ratio_consistent(output) == true` | Proxy |
| 16 | "consistent" | T3 | `spacing_scale_adherence(output) >= 0.8` | Proxy |
| 17 | "consistent" | T3 | `primary_color_count(output) <= 5` | Proxy |
| 18 | "consistent" | T3 | `has_color_relationships(output) == true` | Proxy |
| 19 | Maintainability | T3 | `css_variable_count(output) >= 3` | Proxy |

---

## Verification Approach

All predicates use **static CSS analysis**. No rendering or execution required.

| Analysis Type | Predicates |
|---------------|------------|
| CSS parsing | Syntax, properties, values, variable count |
| Value extraction | Font sizes, line heights, colors, spacing |
| Color math | Contrast ratios, color relationships |
| Scale detection | Type scale, spacing scale adherence |
| Pattern matching | Dark mode media query presence |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | CSS validity, theme completeness | Invalid/incomplete theme = broken |
| **T2** | WCAG contrast, dark mode | Accessibility = compliance requirement |
| **T3** | Typography, spacing, palette, variables | Quality/maintainability preferences |

**Note on dark mode as T2:** Dark mode is increasingly a compliance expectation. Users with light sensitivity or in low-light environments need it for accessibility reasons.

---

## WCAG Requirements

| Requirement | Standard | Threshold | Tier |
|-------------|----------|-----------|------|
| Text contrast (normal) | WCAG AA | 4.5:1 | T2 |
| Text contrast (large) | WCAG AA | 3:1 | T2 |
| UI component contrast | WCAG AA | 3:1 | T2 |

---

## Theme Completeness

A complete theme must define:

| Component | What to include |
|-----------|-----------------|
| **Colors** | Primary, secondary, accent, background, text, semantic (error, success, warning) |
| **Typography** | Font families, size scale, line heights, weights |
| **Spacing** | Spacing scale, margin/padding values |

Missing any component = T1 failure.

---

## Quality Metrics

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Base font size | ≥14px | Readability minimum |
| Line height | ≥1.4 | Text readability |
| Font families | ≤3 | Restraint and consistency |
| Spacing adherence | ≥80% | Most values on scale |
| Primary colors | ≤5 | Palette coherence |
| CSS variables | ≥3 | Minimum maintainability |

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Professional" | Aesthetic judgment | Accessibility + readability proxies |
| "Beautiful" | Subjective | Retained as guidance |
| "Appropriate for use case" | Context-dependent | Retained as guidance |
| "Harmonious colors" | Partially verifiable | Color relationships as proxy |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 6 | Fully verified |
| T2 (Accessibility) | 4 | Fully verified |
| T3 (Quality) | 9 | Verified via proxies |
| Non-verifiable | 4 | Documented |
| **Total** | **23** | — |
