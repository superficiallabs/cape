# Mapping: algorithmic-art

> **Source:** [anthropics/skills/algorithmic-art](https://github.com/anthropics/skills/tree/main/algorithmic-art)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "p5.js sketches" | T1 | `valid_p5_syntax(code) == true` | Direct |
| 2 | "p5.js sketches" | T1 | `has_setup_function(code) == true` | Direct |
| 3 | "p5.js sketches" | T1 | `has_draw_function(code) == true` | Direct |
| 4 | "seeded randomness" | T1 | `calls_random_seed(code) == true` | Direct |
| 5 | (implicit safety) | T1 | `no_fetch_calls(code) == true` | Direct |
| 6 | (implicit safety) | T1 | `no_eval_calls(code) == true` | Direct |
| 7 | "gallery-quality" | T3 | `color_function_count(code) >= config.min_color_calls` | Proxy |
| 8 | "gallery-quality" | T3 | `unique_shape_functions(code) >= config.min_shape_variety` | Proxy |
| 9 | "gallery-quality" | T3 | `uses_noise_or_nested_loops(code) == true` | Proxy |
| 10 | "gallery-quality" | T3 | `transform_function_count(code) >= config.min_transform_calls` | Proxy |

---

## Predicate Details

### T1: Objective Correctness

| Predicate | What it verifies | Failure mode |
|-----------|------------------|--------------|
| `valid_p5_syntax(code)` | Code parses as valid p5.js/JavaScript | Syntax errors prevent execution |
| `has_setup_function(code)` | Required p5.js entry point exists | Sketch won't initialize |
| `has_draw_function(code)` | Required p5.js render loop exists | Sketch won't animate/render |
| `calls_random_seed(code)` | Randomness is seeded for reproducibility | Non-deterministic output |
| `no_fetch_calls(code)` | No external data dependencies | Breaks reproducibility, potential failures |
| `no_eval_calls(code)` | No dynamic code execution | Security risk, code smell |

### T3: Quality Proxies (Static Code Analysis)

| Predicate | What it proxies | Why this proxy |
|-----------|-----------------|----------------|
| `color_function_count(code)` | Intentional color work | Multiple fill/stroke/background calls suggest deliberate palette |
| `unique_shape_functions(code)` | Visual variety | Multiple shape types suggest compositional thought |
| `uses_noise_or_nested_loops(code)` | Algorithmic complexity | Noise functions and nested iteration produce non-trivial output |
| `transform_function_count(code)` | Compositional depth | Transformations suggest spatial reasoning |

See [ASSUMPTIONS.md](./ASSUMPTIONS.md) for threshold rationale and customization guidance.

All predicates are verifiable through static code analysis (AST parsing, pattern matching). No execution required.

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Algorithmic philosophy" | Semantic/conceptual | Retained as skill guidance |
| "Emotional impact" | Purely subjective | Retained as skill guidance |
| "Aesthetic merit" | No structural proxy | Retained as skill guidance |

These remain in the source skill as human-readable context. No predicates are written for them.

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 6 | Verified via static analysis |
| T3 (Quality) | 4 | Verified via static code proxies |
| Non-verifiable | 3 | Documented, not enforced |
| **Total** | **13** | — |
