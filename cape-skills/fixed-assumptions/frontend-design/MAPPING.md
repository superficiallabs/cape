# Mapping: frontend-design

> **Source:** [anthropics/skills/frontend-design](https://github.com/anthropics/skills/tree/main/frontend-design)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "real working code" | T1 | `html_syntax_valid(output) == true` | Direct |
| 2 | "real working code" | T1 | `jsx_syntax_valid(output) == true` | Direct |
| 3 | "real working code" | T1 | `css_syntax_valid(output) == true` | Direct |
| 4 | "real working code" | T1 | `has_default_export(output) == true` | Direct |
| 5 | "real working code" | T1 | `hooks_rules_valid(output) == true` | Direct |
| 6 | "exceptional attention" | T2 | `images_missing_alt_count(output) == 0` | Direct |
| 7 | "exceptional attention" | T2 | `buttons_missing_text_count(output) == 0` | Direct |
| 8 | "exceptional attention" | T2 | `inputs_missing_label_count(output) == 0` | Direct |
| 9 | "exceptional attention" | T2 | `min_color_contrast(output) >= 4.5` | Direct |
| 10 | "avoid AI slop" | T3 | `unique_border_radius_count(output) >= 3` | Proxy |
| 11 | "avoid AI slop" | T3 | `unique_color_count(output) in [4, 12]` | Proxy |
| 12 | "avoid AI slop" | T3 | `font_family_count(output) <= 3` | Proxy |
| 13 | "avoid AI slop" | T3 | `unique_font_size_count(output) >= 3` | Proxy |
| 14 | "BOLD aesthetic" | T3 | `spacing_on_scale(output, 4) == true` | Proxy |
| 15 | "BOLD aesthetic" | T3 | `typography_level_count(output) >= 3` | Proxy |
| 16 | "production-grade" | T3 | `breakpoint_count(output) >= 2` | Direct |
| 17 | "production-grade" | T3 | `hardcoded_color_count(output) == 0` | Direct |
| 18 | "production-grade" | T3 | `inline_style_count(output) == 0` | Direct |

---

## Verification Approach

All predicates are verified through **static code analysis**. No execution or rendering required.

| Analysis Type | Predicates |
|---------------|------------|
| Syntax parsing | HTML, JSX, CSS validity |
| AST analysis | Default export, hooks rules, tag presence |
| CSS parsing | Colors, fonts, spacing, border-radius, breakpoints |
| Pattern matching | Alt text, labels, aria attributes, inline styles |
| Color math | Contrast ratio calculation from declared values |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Syntax validity, structure | Invalid code = broken artifact |
| **T2** | Accessibility (alt, labels, contrast) | Inaccessible interfaces exclude users |
| **T3** | Design variety, intentionality, maintainability | Quality preferences |

---

## Anti-Slop Predicates (T3)

The "avoid generic AI slop aesthetics" guidance is converted to structural proxies:

| Proxy | What it detects | Why it indicates "slop" |
|-------|-----------------|-------------------------|
| **Border-radius variety** | Uniform radius everywhere | Generic AI uses one radius for all elements |
| **Color count** | Too few (<4) or too many (>12) | Slop is either monotone or rainbow noise |
| **Font family restraint** | More than 3 families | Slop often mixes fonts arbitrarily |
| **Font size variety** | Fewer than 3 sizes | Slop has flat typography hierarchy |

---

## Accessibility Predicates (T2)

Static accessibility checks that don't require rendering:

| Check | What it verifies | How |
|-------|------------------|-----|
| `images_missing_alt_count` | All `<img>` have alt attribute | HTML/JSX parsing |
| `buttons_missing_text_count` | Buttons have text or aria-label | HTML/JSX parsing |
| `inputs_missing_label_count` | Inputs have associated labels | HTML/JSX parsing |
| `min_color_contrast` | Text/background contrast ratio | Parse CSS color values, calculate ratio |

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Pick an extreme aesthetic" | Which aesthetic is subjective | Verify intentionality instead |
| "True to the aesthetic direction" | Requires understanding intent | Retained as guidance |
| "Renders correctly" | Requires execution | Syntax validity as proxy |
| "Performance score" | Requires Lighthouse | Retained as guidance |
| "Beautiful" | Aesthetic judgment | Retained as guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 5 | Static syntax analysis |
| T2 (Governance) | 4 | Static accessibility checks |
| T3 (Quality) | 9 | Static code analysis |
| Non-verifiable | 5 | Documented |
| **Total** | **23** | — |
