# Assumptions: algorithmic-art

> **Source:** [anthropics/skills/algorithmic-art](https://github.com/anthropics/skills/tree/main/algorithmic-art)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## Overview

The algorithmic-art skill asks for "gallery-quality computational art." This is subjective guidance that we convert to objective predicates via static code analysis.

**Philosophy:** We define "gallery-quality" in terms of code patterns that correlate with quality output. Code that uses noise functions, multiple colors, varied shapes, and transformations tends to produce more interesting art than code that doesn't. These are verifiable proxies, not aesthetic judgments.

**All verification is static**—we analyze code structure, not rendered output. No execution harness required.

---

## Configuration Profiles

These thresholds define what "quality" means for your context:

**Gallery submission:**
- `min_color_calls: 5`
- `min_shape_variety: 4`
- `min_transform_calls: 3`

**Educational demo:**
- `min_color_calls: 2`
- `min_shape_variety: 2`
- `min_transform_calls: 1`

**Minimalist study:**
- `min_color_calls: 1`
- `min_shape_variety: 1`
- `min_transform_calls: 0`

The policy doesn't define quality—you do. These predicates verify your definition objectively.

---

## Assumption 1: Intentional Color Work

**Original guidance:**
> "gallery-quality art"

**Interpretation:**
Quality generative art typically involves deliberate color choices. Code with multiple color function calls (fill, stroke, background with different values) suggests intentional palette work.

**Predicate:**
```
color_function_count(code) >= config.min_color_calls
```

**Default threshold:** `min_color_calls: 3`

**Rationale:**
| Color calls | Typical code pattern |
|-------------|---------------------|
| 0–1 | Default colors only, likely accidental |
| 2 | Background + one fill, minimal intentionality |
| 3+ | Multiple deliberate color choices |

**Customization:**
- Monochrome intentional style: lower to `1`
- Rich color work requirement: raise to `5`

---

## Assumption 2: Shape Variety

**Original guidance:**
> "gallery-quality art"

**Interpretation:**
Quality generative art typically uses multiple shape types rather than repeating a single primitive. Variety in shape functions suggests compositional thought.

**Predicate:**
```
unique_shape_functions(code) >= config.min_shape_variety
```

**Default threshold:** `min_shape_variety: 2`

**Rationale:**
| Shape types | Typical output |
|-------------|---------------|
| 1 | Repetitive single-primitive pattern |
| 2 | Basic variety (e.g., circles + lines) |
| 3+ | Rich compositional vocabulary |

**Shape functions counted:** `ellipse`, `rect`, `line`, `arc`, `bezier`, `vertex`, `triangle`, `quad`, `point`

**Customization:**
- Minimalist single-shape study: lower to `1`
- Complex compositions: raise to `4`

---

## Assumption 3: Algorithmic Complexity

**Original guidance:**
> "gallery-quality art", "computational art"

**Interpretation:**
Computational art should exhibit algorithmic sophistication. Code using noise functions or nested iteration produces more complex output than flat sequential code.

**Predicate:**
```
uses_noise_or_nested_loops(code) == true
```

**What triggers true:**
- Calls to `noise()`, `noiseSeed()`, or Perlin noise functions
- Nested `for` or `while` loops (loop inside loop)
- Recursive function calls

**Rationale:**
Noise functions and nested iteration are the building blocks of non-trivial generative art. Their absence usually indicates trivially simple output.

**Customization:**
This is a binary check. If you need to allow simple sketches, remove this predicate from the policy.

---

## Assumption 4: Compositional Transformations

**Original guidance:**
> "gallery-quality art"

**Interpretation:**
Quality generative art often uses spatial transformations for compositional depth. Code using translate, rotate, scale suggests spatial reasoning beyond flat coordinates.

**Predicate:**
```
transform_function_count(code) >= config.min_transform_calls
```

**Default threshold:** `min_transform_calls: 1`

**Transform functions counted:** `translate`, `rotate`, `scale`, `push`, `pop`, `shearX`, `shearY`

**Rationale:**
| Transform calls | Typical composition |
|-----------------|---------------------|
| 0 | Flat, absolute positioning |
| 1+ | Spatial reasoning, relative positioning |
| 3+ | Complex nested transformations |

**Customization:**
- Allow flat compositions: set to `0`
- Require complex spatial work: raise to `3`

---

## T1 Predicates (Not Assumptions)

The following are direct requirements, not interpretive assumptions:

| Predicate | Why it's T1 |
|-----------|-------------|
| `valid_p5_syntax(code)` | Invalid syntax = broken code |
| `has_setup_function(code)` | Missing setup = sketch won't run |
| `has_draw_function(code)` | Missing draw = no render loop |
| `calls_random_seed(code)` | Explicit requirement for reproducibility |
| `no_fetch_calls(code)` | External deps break reproducibility |
| `no_eval_calls(code)` | Security requirement |

---

## Not Verified

The following cannot be converted to static predicates:

| Guidance | Why not verifiable |
|----------|-------------------|
| "Algorithmic philosophy" | Semantic concept requiring interpretation |
| "Emotional impact" | Purely subjective viewer response |
| "Aesthetic merit" | No code pattern correlates with beauty |
| Runtime errors | Requires execution |
| Actual determinism | Requires executing twice |
| Visual output quality | Requires rendering |

These remain as guidance for human judgment.

---

## Configuration Reference

```json
{
  "configuration": {
    "min_color_calls": 3,
    "min_shape_variety": 2,
    "min_transform_calls": 1
  }
}
```

Override any threshold by passing a custom configuration at evaluation time.
