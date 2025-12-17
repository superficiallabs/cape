# Assumptions: theme-factory

> **Source:** [anthropics/skills/theme-factory](https://github.com/anthropics/skills/tree/main/theme-factory)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Reference:** [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)

---

## Overview

The theme-factory skill asks for "professional" and "consistent" themes. We interpret "professional" primarily through accessibility and readability standards, and "consistent" through mathematical scale relationships.

**Philosophy:** A professional theme is accessible by default. Accessibility isn't a feature—it's baseline quality. We verify WCAG compliance as T2 (governance), and readability/consistency as T3 (quality).

**Verification approach:** All predicates use static CSS analysis—parsing, value extraction, and color math. No rendering or execution required.

---

## Configuration Profiles

These thresholds define what "professional" means for your context:

**Design system:**
- `min_contrast_text: 4.5`
- `min_contrast_ui: 3.0`
- `min_base_font_size: 16`
- `min_line_height: 1.5`
- `max_font_families: 2`
- `min_spacing_adherence: 0.9`
- `max_primary_colors: 4`

**Marketing site:**
- `min_contrast_text: 4.5`
- `min_contrast_ui: 3.0`
- `min_base_font_size: 16`
- `min_line_height: 1.6`
- `max_font_families: 3`
- `min_spacing_adherence: 0.8`
- `max_primary_colors: 5`

**MVP product:**
- `min_contrast_text: 4.5`
- `min_contrast_ui: 3.0`
- `min_base_font_size: 14`
- `min_line_height: 1.4`
- `max_font_families: 3`
- `min_spacing_adherence: 0.7`
- `max_primary_colors: 6`

The policy doesn't define quality—you do. These predicates verify your definition objectively.

---

## Assumption 1: Text Contrast (Accessibility)

**Original guidance:**
> "professional themes"

**Interpretation:**
Professional themes must be accessible. WCAG AA requires 4.5:1 contrast ratio for normal text.

**Predicate:**
```
min_text_contrast_ratio(output) >= config.min_contrast_text
```

**Tier:** T2 (Governance)—Accessibility is a compliance requirement

**Default threshold:** `min_contrast_text: 4.5`

**WCAG reference:**

| Text type | Required ratio | Standard |
|-----------|----------------|----------|
| Normal text | 4.5:1 | WCAG AA |
| Large text (18pt+) | 3:1 | WCAG AA |
| Normal text | 7:1 | WCAG AAA |

**Static verification:** Parse CSS color values, calculate contrast ratio using relative luminance formula.

**Customization:**
- AAA compliance: raise to `7.0`
- Large text only: lower to `3.0` (if all text is large)

---

## Assumption 2: UI Contrast (Accessibility)

**Original guidance:**
> "professional themes"

**Interpretation:**
UI elements (buttons, inputs, icons) need sufficient contrast to be perceivable.

**Predicate:**
```
min_ui_contrast_ratio(output) >= config.min_contrast_ui
```

**Tier:** T2 (Governance)

**Default threshold:** `min_contrast_ui: 3.0`

**Static verification:** Identify UI-related color pairs (border/background, icon/background), calculate contrast.

---

## Assumption 3: Dark Mode Support (Accessibility)

**Original guidance:**
> "professional themes"

**Interpretation:**
Professional themes must support dark mode. Users with light sensitivity, migraine conditions, or in low-light environments need dark alternatives.

**Predicate:**
```
has_dark_mode_variant(output) == true
dark_mode_contrast_valid(output) == true
```

**Tier:** T2 (Governance)—Dark mode is increasingly an accessibility expectation

**Static verification:**
- Check for `@media (prefers-color-scheme: dark)` or equivalent
- Parse dark mode color values, verify contrast requirements

**Customization:**
- Light-only applications: could be disabled (not recommended)

---

## Assumption 4: Base Font Size (Readability)

**Original guidance:**
> "professional themes"

**Interpretation:**
Professional themes should be readable. Base font sizes below 14px strain most readers.

**Predicate:**
```
base_font_size_px(output) >= config.min_base_font_size
```

**Tier:** T3 (Preference)

**Default threshold:** `min_base_font_size: 14` (pixels)

**Threshold rationale:**

| Size | Interpretation |
|------|----------------|
| <12px | Very small—accessibility issue |
| 12–14px | Small—readable but tight |
| 14–16px | Standard—comfortable reading (default minimum) |
| 16–18px | Large—optimal for body text |
| >18px | Very large—heading territory |

**Customization:**
- Data-dense UIs: may need smaller text—lower to `12`
- Reading-focused apps: raise to `16`

---

## Assumption 5: Line Height (Readability)

**Original guidance:**
> "professional themes"

**Interpretation:**
Adequate line height improves readability. Tight leading makes text harder to scan.

**Predicate:**
```
base_line_height(output) >= config.min_line_height
```

**Tier:** T3 (Preference)

**Default threshold:** `min_line_height: 1.4` (unitless ratio)

**Threshold rationale:**

| Line height | Interpretation |
|-------------|----------------|
| 1.0–1.2 | Very tight—hard to read |
| 1.2–1.4 | Tight—acceptable for headings |
| 1.4–1.6 | Standard—comfortable body text (default) |
| 1.6–2.0 | Loose—generous spacing |
| >2.0 | Very loose—may waste space |

**Customization:**
- Headings: may use tighter line height
- Long-form content: raise to `1.5` or `1.6`

---

## Assumption 6: Font Family Restraint (Consistency)

**Original guidance:**
> "consistent"

**Interpretation:**
Consistent themes use limited font families. Too many fonts creates visual chaos.

**Predicate:**
```
font_family_count(output) <= config.max_font_families
```

**Tier:** T3 (Preference)

**Default threshold:** `max_font_families: 3`

**Typical usage:**
- 1 font: Heading + body (same family, different weights)
- 2 fonts: Heading + body (different families)
- 3 fonts: Heading + body + mono (complete set)

**Customization:**
- Minimal design: lower to `2`
- Complex editorial: raise to `4`

---

## Assumption 7: Type Scale Consistency (Consistency)

**Original guidance:**
> "consistent"

**Interpretation:**
Professional typography follows a mathematical scale. Heading sizes should relate by consistent ratios.

**Predicates:**
```
has_type_scale(output) == true
type_scale_ratio_consistent(output) == true
```

**Tier:** T3 (Preference)

**Common type scales:**

| Ratio | Name | Scale example (16px base) |
|-------|------|---------------------------|
| 1.125 | Major second | 16, 18, 20, 23, 26... |
| 1.200 | Minor third | 16, 19, 23, 28, 33... |
| 1.250 | Major third | 16, 20, 25, 31, 39... |
| 1.333 | Perfect fourth | 16, 21, 28, 37, 50... |
| 1.500 | Perfect fifth | 16, 24, 36, 54, 81... |

**Static verification:** Extract font-size values, compute ratios between adjacent sizes, check for consistency.

---

## Assumption 8: Spacing Scale Consistency (Consistency)

**Original guidance:**
> "consistent"

**Interpretation:**
Professional themes use systematic spacing. At least 80% of spacing values should adhere to a scale.

**Predicate:**
```
spacing_scale_adherence(output) >= config.min_spacing_adherence
```

**Tier:** T3 (Preference)

**Default threshold:** `min_spacing_adherence: 0.8` (80%)

**Threshold rationale:**

| Adherence | Interpretation |
|-----------|----------------|
| <50% | No system—arbitrary values |
| 50–70% | Weak system—many exceptions |
| 70–80% | Moderate—mostly systematic |
| 80–90% | Good—consistent with exceptions (default) |
| 90%+ | Strict—highly systematic |

**Common spacing scales:**
- 4px base: 4, 8, 12, 16, 24, 32, 48, 64...
- 8px base: 8, 16, 24, 32, 48, 64, 96...

---

## Assumption 9: Palette Coherence (Consistency)

**Original guidance:**
> "consistent"

**Interpretation:**
Professional themes have coherent color palettes—not random colors. We verify limited primary colors and harmonic relationships.

**Predicates:**
```
primary_color_count(output) <= config.max_primary_colors
has_color_relationships(output) == true
```

**Tier:** T3 (Preference)

**Default threshold:** `max_primary_colors: 5`

**Color relationships (verified via color wheel math):**
- Complementary (opposite on wheel)
- Analogous (adjacent on wheel)
- Triadic (evenly spaced)
- Monochromatic (same hue, different lightness)

---

## Assumption 10: CSS Variables (Maintainability)

**Original guidance:**
> Implicit in "professional"

**Interpretation:**
Professional themes use CSS custom properties for maintainability. Hardcoded values scattered through CSS are unmaintainable.

**Predicate:**
```
css_variable_count(output) >= config.min_css_variables
```

**Tier:** T3 (Preference)

**Default threshold:** `min_css_variables: 3`

**What should be variables:**
- Color palette values
- Font families
- Spacing scale base
- Border radii
- Shadows

---

## Not Verified (T1 Only)

These constraints are objectively verifiable without assumptions:

| Constraint | Tier | Why no assumption needed |
|------------|------|--------------------------|
| Valid CSS syntax | T1 | Parser check |
| Valid properties | T1 | Property validation |
| Theme has colors | T1 | Definition presence check |
| Theme has typography | T1 | Definition presence check |
| Theme has spacing | T1 | Definition presence check |

---

## Not Verified (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Professional" | Aesthetic judgment | Accessibility + readability proxies |
| "Beautiful" | Subjective | Retained as guidance |
| "Appropriate for use case" | Context-dependent | Retained as guidance |

---

## Configuration Reference

```json
{
  "configuration": {
    "min_contrast_text": 4.5,
    "min_contrast_ui": 3.0,
    "min_base_font_size": 14,
    "min_line_height": 1.4,
    "max_font_families": 3,
    "min_spacing_adherence": 0.8,
    "min_css_variables": 3,
    "max_primary_colors": 5
  }
}
```

Override any threshold at evaluation time to match your design standards.
