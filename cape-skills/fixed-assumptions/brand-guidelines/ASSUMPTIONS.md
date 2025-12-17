# Assumptions: brand-guidelines

> **Source:** [anthropics/skills/brand-guidelines](https://github.com/anthropics/skills/tree/main/brand-guidelines)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

Brand guidelines policies enforce organizational visual identity. Unlike creative skills where we use proxies for quality, brand compliance has clear requirements: either you're using the approved colors/fonts or you're not.

**Key distinction:** Most predicates here are **configuration checks**, not assumptions. The assumption is that "on brand" means "matches configured values exactly." The values themselves are injected, not assumed.

---

## Assumption 1: Color Compliance (with Shade Tolerance)

**Original guidance:**
> "Use official brand colors"

**Interpretation:**
Colors must match the configured brand palette. However, we allow shades and tints within a tolerance range to accommodate hover states, disabled states, and intentional variations.

**Predicate:**
```
unauthorized_color_count(output, config.brand_colors, config.color_shade_tolerance) == 0
```

**Tier:** T2 (Governance) — Brand violations are compliance failures

**Configuration:**
```json
{
  "brand_colors": {
    "primary": "#D97757",
    "secondary": "#1A1A1A",
    "background": "#FFFFFF",
    "text": "#1A1A1A"
  },
  "color_shade_tolerance": 0.15
}
```

**Shade tolerance rationale:**

| Tolerance | Effect |
|-----------|--------|
| `0.0` | Exact hex match only (strictest) |
| `0.10` | Minor variations (subtle hover states) |
| `0.15` | Moderate variations (default—accommodates most UI states) |
| `0.25` | Permissive (allows significant tints/shades) |

**Customization:**
- Strict brand enforcement: set `color_shade_tolerance: 0`
- Extended palette: add more colors to `brand_colors`
- Semantic colors (error, success): add to palette or create separate policy

---

## Assumption 2: Typography Compliance

**Original guidance:**
> "Use brand typography"

**Interpretation:**
Font families must match the configured list exactly. No assumptions about which fonts—entirely driven by configuration.

**Predicate:**
```
unauthorized_font_count(output, config.brand_fonts) == 0
```

**Tier:** T2 (Governance)

**Configuration:**
```json
{
  "brand_fonts": ["Styrene A", "Styrene B", "system-ui", "sans-serif"]
}
```

**Rationale for fallbacks:**
Including `system-ui` and `sans-serif` in the allowed list ensures graceful degradation when brand fonts aren't available. Remove these for strict enforcement.

**Customization:**
- Strict enforcement: remove system fallbacks from list
- Multiple weights: fonts are matched by family name; weights are not validated (add separate policy if needed)

---

## Assumption 3: Contrast Compliance (WCAG)

**Original guidance:**
> Implicit accessibility requirement

**Interpretation:**
All foreground/background color pairs must meet WCAG AA contrast ratio. This is a T2 (governance) requirement because accessibility violations can be legal compliance failures.

**Predicate:**
```
min_contrast_ratio(output) >= config.contrast_threshold
```

**Tier:** T2 (Governance)

**Default threshold:** `4.5` (WCAG AA for normal text)

**Threshold reference:**

| Threshold | Standard | Use case |
|-----------|----------|----------|
| `3.0` | WCAG AA Large Text | Headings ≥18pt or ≥14pt bold |
| `4.5` | WCAG AA Normal Text | Body text (default) |
| `7.0` | WCAG AAA | Enhanced accessibility |

**Customization:**
- Large text only: lower to `3.0`
- AAA compliance: raise to `7.0`
- Separate thresholds: create multiple policies for different text sizes

---

## Assumption 4: Spacing Grid

**Original guidance:**
> "Consistent application"

**Interpretation:**
"Consistent" means following a spacing scale. All margin/padding values should be multiples of a base unit, with exceptions for fine-grained adjustments (1px borders, 2px outlines, etc.).

**Predicate:**
```
off_grid_spacing_count(output, config.spacing_base, config.spacing_exceptions) == 0
```

**Tier:** T3 (Preference) — This is a quality guideline, not a hard compliance requirement

**Configuration:**
```json
{
  "spacing_base": 8,
  "spacing_exceptions": [1, 2, 4]
}
```

**Rationale for 8px base:**

| Base | Common usage |
|------|--------------|
| `4px` | Dense UIs, data-heavy applications |
| `8px` | Standard (most design systems) |
| `10px` | Decimal-friendly calculations |
| `16px` | Spacious, editorial layouts |

**Rationale for exceptions:**
Sub-base values (1px, 2px, 4px) are needed for:
- Border widths
- Focus outlines
- Fine-tuned alignments
- Icon padding

**Customization:**
- Strict grid: set `spacing_exceptions: []`
- Different base: common alternatives are 4px or 16px
- Promote to T2: if spacing is a hard brand requirement

---

## Assumption 5: Typography Hierarchy

**Original guidance:**
> Implicit in "typography" guidance

**Interpretation:**
Heading sizes should follow a descending scale (h1 > h2 > h3 > h4 > h5 > h6). This ensures visual hierarchy is maintained.

**Predicate:**
```
heading_sizes_descending(output) == true
```

**Tier:** T3 (Preference)

**Rationale:**
Inverted heading sizes (e.g., h3 larger than h2) break visual hierarchy and indicate likely errors. This is a quality check, not a brand compliance requirement.

**Customization:**
- Specific scale ratio: add `heading_scale_ratio` check (e.g., each level should be 1.25× smaller)
- Skip validation: remove this policy if headings are used non-hierarchically (rare)

---

## Not Verified

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Brand voice" | Semantic analysis required | Retained as skill guidance |
| "Visual harmony" | Aesthetic judgment | Retained as skill guidance |
| "Appropriate imagery" | Context-dependent | Retained as skill guidance |
| "Logo usage rules" | Complex spatial requirements | Could be added as separate policy |

---

## Configuration Template

Replace defaults with your organization's brand:

```json
{
  "configuration": {
    "brand_colors": {
      "primary": "#YOUR_PRIMARY",
      "secondary": "#YOUR_SECONDARY",
      "accent": "#YOUR_ACCENT",
      "background": "#YOUR_BG",
      "text": "#YOUR_TEXT"
    },
    "color_shade_tolerance": 0.15,
    "brand_fonts": ["Your Brand Font", "Your Fallback", "system-ui"],
    "spacing_base": 8,
    "spacing_exceptions": [1, 2, 4],
    "contrast_threshold": 4.5
  }
}
```
