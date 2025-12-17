# Assumptions: canvas-design

> **Source:** [anthropics/skills/canvas-design](https://github.com/anthropics/skills/tree/main/canvas-design)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

The canvas-design skill asks for "beautiful visual art" following "design philosophies." These are subjective goals that cannot be verified directly. We use structural proxies that detect common composition problems without claiming to measure beauty itself.

**Philosophy:** These proxies catch obvious failures (blank canvas, visual chaos, no focal point) rather than guaranteeing good design. Passing all predicates means the design isn't obviously broken—not that it's beautiful.

**Verification approach:** This policy assumes the model outputs actual image files (PNG, PDF, SVG). All predicates are verified via standard image processing (PIL, OpenCV, etc.)—no execution harness required.

---

## Configuration Profiles

These thresholds define what "quality" means for your context:

**Print production:**
- `min_unique_colors: 4`
- `max_unique_colors: 15`
- `min_visual_balance: 0.35`
- `max_visual_balance: 0.65`
- `min_dominant_color_ratio: 0.15`
- `min_dpi: 300`

**Social media graphics:**
- `min_unique_colors: 3`
- `max_unique_colors: 20`
- `min_visual_balance: 0.3`
- `max_visual_balance: 0.7`
- `min_dominant_color_ratio: 0.1`
- `min_dpi: 72`

**Sketch exploration:**
- `min_unique_colors: 2`
- `max_unique_colors: 30`
- `min_visual_balance: 0.2`
- `max_visual_balance: 0.8`
- `min_dominant_color_ratio: 0.05`
- `min_dpi: 72`

The policy doesn't define quality—you do. These predicates verify your definition objectively.

---

## Assumption 1: Intentional Color Palette (Variety)

**Original guidance:**
> "design philosophies"

**Interpretation:**
Good design uses color intentionally. Too few colors suggests incomplete work or lack of effort. Too many colors suggests noise or lack of control.

**Predicate:**
```
unique_color_count(output) >= config.min_unique_colors
unique_color_count(output) <= config.max_unique_colors
```

**Tier:** T3 (Preference)

**Default thresholds:** `min_unique_colors: 2`, `max_unique_colors: 20`

**Threshold rationale:**

| Color count | Typical interpretation |
|-------------|------------------------|
| 1 | Monochrome—may be intentional but often indicates incomplete render |
| 2–5 | Minimal palette—intentional, cohesive |
| 6–12 | Standard palette—typical for most designs |
| 13–20 | Rich palette—complex but controlled |
| > 20 | Noisy—often indicates gradients, photos, or lack of curation |

**Customization:**
- Monochrome designs: set `min_unique_colors: 1`
- Photographic content: raise `max_unique_colors: 100` or disable
- Strict palette: lower `max_unique_colors: 8`

---

## Assumption 2: Color Hierarchy

**Original guidance:**
> "design philosophies"

**Interpretation:**
Intentional designs have dominant colors that establish hierarchy. If no single color exceeds a minimum coverage threshold, the palette may be chaotic.

**Predicate:**
```
dominant_color_ratio(output) >= config.min_dominant_color_ratio
```

**Tier:** T3 (Preference)

**Default threshold:** `min_dominant_color_ratio: 0.1` (10%)

**Threshold rationale:**

| Dominant color ratio | Typical interpretation |
|----------------------|------------------------|
| < 5% | No clear hierarchy—visual noise |
| 5–10% | Weak hierarchy—many competing colors |
| 10–30% | Clear hierarchy—intentional design (default) |
| > 30% | Strong dominance—bold, simple design |

**Customization:**
- Complex illustrations: lower to `0.05`
- Bold branding: raise to `0.25`
- Pattern designs: may legitimately have no dominant color—disable check

---

## Assumption 3: Visual Balance

**Original guidance:**
> "beautiful visual art"

**Interpretation:**
"Beautiful" often implies balanced composition. We measure visual weight distribution across the canvas. Content shouldn't be entirely in one corner or entirely centered.

**Predicate:**
```
visual_weight_distribution(output) >= config.min_visual_balance
visual_weight_distribution(output) <= config.max_visual_balance
```

**Tier:** T3 (Preference)

**Default thresholds:** `min_visual_balance: 0.3`, `max_visual_balance: 0.7`

**How visual_weight_distribution works:**
- Divides canvas into regions (e.g., quadrants or grid)
- Measures pixel density / visual weight in each region
- Returns a normalized score: 0.0 = all weight in edges, 1.0 = all weight in center, 0.5 = perfectly distributed

**Threshold rationale:**

| Distribution score | Typical interpretation |
|--------------------|------------------------|
| < 0.3 | Edge-heavy—content in corners, empty center |
| 0.3–0.5 | Balanced toward edges—dynamic, asymmetric |
| 0.5 | Perfectly centered—may be intentional or boring |
| 0.5–0.7 | Balanced toward center—focused, traditional |
| > 0.7 | Center-heavy—content clustered in middle only |

**Customization:**
- Centered compositions (logos, portraits): raise `min_visual_balance: 0.5`
- Edge-focused designs (borders, frames): lower `max_visual_balance: 0.4`
- Asymmetric layouts: widen range to `[0.2, 0.8]`

---

## Assumption 4: Focal Point

**Original guidance:**
> "beautiful visual art"

**Interpretation:**
Good designs have at least one focal point—an area that draws the viewer's eye. We detect this via high-contrast regions.

**Predicate:**
```
contrast_region_count(output) >= 1
```

**Tier:** T3 (Preference)

**Threshold rationale:**
A design with zero high-contrast regions may be:
- Entirely low-contrast (washed out)
- Uniformly busy (no hierarchy)
- Blank or near-blank

At least one contrast region indicates intentional focus.

**Customization:**
- Soft/muted aesthetics: this check may produce false positives—consider disabling
- Multi-focal designs: could require `>= 2` for more complex compositions
- Background patterns: may legitimately have no focal point—disable check

---

## Not Verified (T1/T2 Only)

The following constraints are objectively verifiable without assumptions:

| Constraint | Tier | Why no assumption needed |
|------------|------|--------------------------|
| Valid format (PNG/PDF/SVG) | T1 | Binary check—file is or isn't valid |
| File not corrupted | T1 | Header validation—deterministic |
| Dimensions match spec | T1 | Numeric comparison |
| Not empty (>5% content) | T1 | Pixel count—deterministic |
| Sufficient resolution | T1 | DPI check—deterministic |
| Colors within palette | T2 | Subset check against spec (if provided) |

---

## Not Verified (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Beautiful" | No structural proxy captures beauty | Retained as guidance |
| "Artistic merit" | Subjective judgment | Retained as guidance |
| "Appropriate style" | Context-dependent | Retained as guidance |
| "Professional quality" | Vague, multidimensional | Retained as guidance |

---

## Configuration Reference

```json
{
  "configuration": {
    "allowed_formats": ["png", "pdf", "svg"],
    "min_content_coverage": 0.05,
    "min_dpi": 72,
    "min_unique_colors": 2,
    "max_unique_colors": 20,
    "min_visual_balance": 0.3,
    "max_visual_balance": 0.7,
    "min_dominant_color_ratio": 0.1
  }
}
```

Override any threshold at evaluation time to match your design context.
