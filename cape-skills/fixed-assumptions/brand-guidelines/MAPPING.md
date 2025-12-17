# Mapping: brand-guidelines

> **Source:** [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/brand-guidelines)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | Valid CSS output | T1 | `valid_css(output) == true` | Direct |
| 2 | "official brand colors" | T2 | `unauthorized_color_count(output, ...) == 0` | Config check |
| 3 | "typography" | T2 | `unauthorized_font_count(output, ...) == 0` | Config check |
| 4 | "WCAG compliance" | T2 | `min_contrast_ratio(output) >= config.contrast_threshold` | Direct |
| 5 | "consistent spacing" | T3 | `off_grid_spacing_count(output, ...) == 0` | Proxy |
| 6 | "typography hierarchy" | T3 | `heading_sizes_descending(output) == true` | Direct |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | CSS validity | Broken CSS = unusable artifact |
| **T2** | Colors, fonts, contrast | Brand/accessibility violations are compliance failures |
| **T3** | Spacing grid, heading hierarchy | Quality preferences, not compliance requirements |

**Note on spacing:** Some brand guidelines treat spacing as T2 (strict compliance). The default here is T3 (quality preference). Override by moving the policy to T2 in your configuration if spacing is a hard requirement.

---

## Configuration Reference

This policy is **fully configurable**. Default values are examples (Anthropic brand); replace with your organization's brand constants.

| Config Key | Default | Description |
|------------|---------|-------------|
| `brand_colors` | `{primary: "#D97757", ...}` | Allowed color palette (hex codes) |
| `color_shade_tolerance` | `0.15` | Allowed lightness variation for shades/tints |
| `brand_fonts` | `["Styrene A", ...]` | Allowed font family names |
| `spacing_base` | `8` | Grid base unit in pixels |
| `spacing_exceptions` | `[1, 2, 4]` | Sub-base values allowed for fine adjustments |
| `contrast_threshold` | `4.5` | WCAG AA minimum contrast ratio |
| `heading_scale_ratio` | `1.25` | Expected ratio between heading levels |

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Brand voice" | Semantic/tone | Retained as skill guidance |
| "Visual harmony" | Aesthetic judgment | Retained as skill guidance |
| "Appropriate imagery" | Context-dependent | Retained as skill guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 1 | Fully verified |
| T2 (Governance) | 3 | Fully verified |
| T3 (Quality) | 2 | Verified via proxies |
| Non-verifiable | 3 | Documented |
| **Total** | **9** | — |
