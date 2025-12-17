# Mapping: canvas-design

> **Source:** [anthropics/skills/canvas-design](https://github.com/anthropics/skills/tree/main/canvas-design)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "PNG and PDF formats" | T1 | `format(output) in config.allowed_formats` | Direct |
| 2 | Valid file output | T1 | `file_header_valid(output) == true` | Direct |
| 3 | "dimensions" | T1 | `width(output) == spec.width`, `height(output) == spec.height` | Direct |
| 4 | Non-empty output | T1 | `content_coverage(output) >= config.min_content_coverage` | Direct |
| 5 | Sufficient resolution | T1 | `dpi(output) >= config.min_dpi` | Direct |
| 6 | "coherent" palette | T2 | `colors_subset_of(output, spec.palette) == true` | Config check |
| 7 | "design philosophies" | T3 | `unique_color_count(output) >= min AND <= max` | Proxy |
| 8 | "design philosophies" | T3 | `dominant_color_ratio(output) >= config.min_dominant_color_ratio` | Proxy |
| 9 | "beautiful visual art" | T3 | `visual_weight_distribution(output) in [min, max]` | Proxy |
| 10 | "beautiful visual art" | T3 | `contrast_region_count(output) >= 1` | Proxy |

---

## Verification Approach

This policy assumes the model outputs actual image files (PNG, PDF, SVG). All predicates are verified via standard image processing — no execution harness required.

| Predicate Type | Verification Method |
|----------------|---------------------|
| Format, validity | File header parsing |
| Dimensions, DPI | Image metadata extraction |
| Color analysis | Pixel value extraction, histogram |
| Visual balance | Quadrant pixel density analysis |
| Focal point | Edge detection, contrast analysis |

Libraries like PIL/Pillow, OpenCV, or ImageMagick handle all operations.

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Format, file validity, dimensions, content, resolution | Broken/empty/wrong-size = unusable |
| **T2** | Palette compliance | Using off-palette colors is a spec violation |
| **T3** | Color variety, hierarchy, balance, focal point | Quality indicators, not correctness requirements |

---

## Predicate Details

### T1: Objective Correctness

| Predicate | What it catches | Failure mode |
|-----------|-----------------|--------------|
| `format(output) in [...]` | Wrong file type | Can't be used as specified |
| `file_header_valid(output)` | Corrupted exports | File won't open |
| `width/height == spec` | Wrong dimensions | Won't fit intended use |
| `content_coverage >= 5%` | Blank canvas | Nothing to show |
| `dpi >= 72` | Low resolution | Pixelated/unusable output |

### T2: Governance

| Predicate | What it catches | Failure mode |
|-----------|-----------------|--------------|
| `colors_subset_of(output, palette)` | Off-palette colors | Spec violation (only checked if palette specified) |

### T3: Quality Proxies

| Predicate | What it proxies | Threshold rationale |
|-----------|-----------------|---------------------|
| `unique_color_count` in [2, 20] | Intentional palette | < 2 = incomplete; > 20 = noisy |
| `dominant_color_ratio >= 10%` | Color hierarchy | No dominant color = visual chaos |
| `visual_weight_distribution` in [0.3, 0.7] | Visual balance | Content shouldn't be all edges or all center |
| `contrast_region_count >= 1` | Focal point | Design needs something to draw the eye |

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Beautiful" | Aesthetic judgment beyond proxies | Retained as skill guidance |
| "Design philosophy" | Conceptual/stylistic intent | Retained as skill guidance |
| "Artistic merit" | Subjective quality | Retained as skill guidance |
| "Appropriate for use case" | Context-dependent | Retained as skill guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 5 | Fully verified |
| T2 (Governance) | 1 | Verified (conditional on spec.palette) |
| T3 (Quality) | 4 | Verified via proxies |
| Non-verifiable | 4 | Documented |
| **Total** | **14** | — |
