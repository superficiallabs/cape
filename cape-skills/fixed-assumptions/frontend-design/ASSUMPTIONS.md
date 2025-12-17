# Assumptions: frontend-design

> **Source:** [anthropics/skills/frontend-design](https://github.com/anthropics/skills/tree/main/frontend-design)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

The frontend-design skill contains Anthropic's most explicit anti-slop guidance: *"avoid generic AI slop aesthetics."* This is subjective guidance that we convert to structural proxies via static code analysis.

**Philosophy:** "AI slop" is structurally characterized by **uniformity** and **lack of intentionality**. Good design exhibits **variety within constraint** and **systematic intent**. Our proxies detect the absence of these qualities by analyzing the code itself.

**Verification approach:** All predicates use static analysis—parsing HTML/JSX/CSS and analyzing patterns. No rendering or execution required.

---

## Assumption 1: Border-Radius Variety (Anti-Slop)

**Original guidance:**
> "avoid generic AI slop aesthetics"

**Interpretation:**
Generic AI outputs apply uniform border-radius everywhere—typically `8px` or `rounded-lg` on every element. Intentional design uses different radii for different purposes.

**Predicate:**
```
unique_border_radius_count(output) >= config.min_border_radius_variety
```

**Tier:** T3 (Preference)

**Default threshold:** `min_border_radius_variety: 3`

**Threshold rationale:**

| Unique radii | Interpretation |
|--------------|----------------|
| 1 | Uniform—strong slop indicator |
| 2 | Minimal variety—likely generic |
| 3 | Reasonable variety—intentional choices (default) |
| 4–5 | Good variety—deliberate design system |

**Static verification:** Parse CSS, extract all `border-radius` values, count unique values.

**Customization:**
- Brutalist design: lower to `1` (sharp corners is intentional)
- Complex UI: raise to `4`

---

## Assumption 2: Color Palette (Anti-Slop)

**Original guidance:**
> "avoid generic AI slop aesthetics"

**Interpretation:**
Intentional design uses a curated palette. Too few colors suggests incomplete theming. Too many suggests noise.

**Predicates:**
```
unique_color_count(output) >= config.min_color_count
unique_color_count(output) <= config.max_color_count
```

**Tier:** T3 (Preference)

**Default thresholds:** `min_color_count: 4`, `max_color_count: 12`

**Threshold rationale:**

| Color count | Interpretation |
|-------------|----------------|
| 1–3 | Minimal—possibly incomplete |
| 4–8 | Intentional palette—primary, secondary, accent, neutrals (default) |
| 9–12 | Rich palette—extended system |
| 13+ | Noisy—likely uncontrolled |

**Static verification:** Parse CSS, extract all color values, deduplicate (normalize formats), count.

**Customization:**
- Monochrome: set `min_color_count: 2`
- Rich dashboard: raise `max_color_count: 16`

---

## Assumption 3: Font Family Restraint (Anti-Slop)

**Original guidance:**
> "avoid generic AI slop aesthetics"

**Interpretation:**
Intentional design uses 2–3 font families with clear purposes. Generic outputs mix fonts arbitrarily.

**Predicate:**
```
font_family_count(output) <= config.max_font_families
```

**Tier:** T3 (Preference)

**Default threshold:** `max_font_families: 3`

**Threshold rationale:**

| Font families | Typical usage |
|---------------|---------------|
| 1 | Single typeface—minimal |
| 2 | Heading + body—standard |
| 3 | Heading + body + mono—complete (default max) |
| 4+ | Lack of restraint |

**Static verification:** Parse CSS `font-family` declarations, extract primary font from each stack, count unique.

---

## Assumption 4: Font Size Variety (Anti-Slop)

**Original guidance:**
> "avoid generic AI slop aesthetics"

**Interpretation:**
Good typography uses a scale with distinct sizes. Generic outputs have flat hierarchy.

**Predicate:**
```
unique_font_size_count(output) >= config.min_font_size_variety
```

**Tier:** T3 (Preference)

**Default threshold:** `min_font_size_variety: 3`

**Threshold rationale:**

| Unique sizes | Interpretation |
|--------------|----------------|
| 1 | Completely flat—slop indicator |
| 2 | Minimal hierarchy |
| 3 | Basic scale—heading, body, small (default) |
| 4–6 | Good scale |

**Static verification:** Parse CSS `font-size` declarations, count unique values.

---

## Assumption 5: Spacing System (Intentionality)

**Original guidance:**
> "BOLD aesthetic direction"

**Interpretation:**
Intentional design uses consistent spacing multiples. Arbitrary design uses random pixel values.

**Predicate:**
```
spacing_on_scale(output, config.spacing_base) == true
```

**Tier:** T3 (Preference)

**Default threshold:** `spacing_base: 4` (multiples of 4px)

**Static verification:** Parse CSS margin/padding/gap values, verify they're multiples of base (with exceptions for 1px, 2px borders).

---

## Assumption 6: Typography Hierarchy (Intentionality)

**Original guidance:**
> "BOLD aesthetic direction"

**Interpretation:**
Intentional design has clear visual hierarchy—at least 3 distinct typography levels.

**Predicate:**
```
typography_level_count(output) >= config.min_typography_levels
```

**Tier:** T3 (Preference)

**Default threshold:** `min_typography_levels: 3`

**Static verification:** Parse CSS, identify distinct combinations of font-size + font-weight.

---

## Assumption 7: Responsive Breakpoints (Production-Readiness)

**Original guidance:**
> "production-grade"

**Interpretation:**
Production code must work on multiple devices.

**Predicate:**
```
breakpoint_count(output) >= config.min_breakpoints
```

**Tier:** T3 (Preference)

**Default threshold:** `min_breakpoints: 2`

**Static verification:** Count `@media` queries with width-based conditions.

---

## Assumption 8: No Hardcoded Colors (Production-Readiness)

**Original guidance:**
> "production-grade"

**Interpretation:**
Production code uses CSS variables for colors, enabling theming.

**Predicate:**
```
hardcoded_color_count(output) == 0
```

**Tier:** T3 (Preference)

**Static verification:** Parse CSS, identify color values not using `var()`. Exclude variable definitions themselves.

---

## Assumption 9: No Inline Styles (Production-Readiness)

**Original guidance:**
> "production-grade"

**Interpretation:**
Production code separates concerns. Inline styles don't scale.

**Predicate:**
```
inline_style_count(output) == 0
```

**Tier:** T3 (Preference)

**Static verification:** Parse HTML/JSX, count `style` attributes.

---

## Accessibility (T2) — Not Assumptions

These are direct requirements, not interpretive assumptions:

| Predicate | What it checks | Why T2 |
|-----------|----------------|--------|
| `images_missing_alt_count == 0` | All images have alt text | Accessibility requirement |
| `buttons_missing_text_count == 0` | Buttons have accessible names | Accessibility requirement |
| `inputs_missing_label_count == 0` | Form inputs have labels | Accessibility requirement |
| `min_color_contrast >= 4.5` | WCAG AA contrast ratio | Accessibility requirement |

All verified via static analysis of HTML/JSX/CSS.

---

## Not Verified

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Renders correctly" | Requires execution | Syntax validity as proxy |
| "Performance score" | Requires Lighthouse | Retained as guidance |
| "Pick an extreme aesthetic" | Subjective choice | Verify intentionality instead |
| "Beautiful" | Aesthetic judgment | Retained as guidance |

---

## Configuration Reference

```json
{
  "configuration": {
    "min_border_radius_variety": 3,
    "min_color_count": 4,
    "max_color_count": 12,
    "max_font_families": 3,
    "min_font_size_variety": 3,
    "spacing_base": 4,
    "min_typography_levels": 3,
    "min_breakpoints": 2,
    "min_contrast_ratio": 4.5
  }
}
```
