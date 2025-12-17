# Mapping: artifacts-builder

> **Source:** [anthropics/skills/artifacts-builder](https://github.com/anthropics/skills/tree/main/artifacts-builder)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed (T1 only)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "React" artifacts | T1 | `valid_jsx_syntax(code) == true` | Direct |
| 2 | "React" artifacts | T1 | `jsx_parse_error_count(code) == 0` | Direct |
| 3 | Use available libraries | T1 | `unresolved_import_count(code) == 0` | Direct |
| 4 | "Tailwind CSS" | T1 | `invalid_tailwind_class_count(code) == 0` | Direct |
| 5 | React best practices | T1 | `hooks_rules_violations(code) == 0` | Direct |
| 6 | Renderable component | T1 | `has_default_export(code) == true` | Direct |
| 7 | Environment constraints | T1 | `source_size_bytes(code) <= config.max_source_size_bytes` | Direct |

---

## Verification Approach

All predicates use **static code analysis**. No execution required.

| Analysis Type | Predicates |
|---------------|------------|
| JSX parsing | Syntax validity, parse errors |
| AST analysis | Import resolution, hooks rules, default export |
| Pattern matching | Tailwind class validation |
| Byte counting | Source size |

---

## Why No T3 Proxies?

The original skill mentions "complex" and "elaborate" artifacts. We do **not** verify complexity because:

1. **Complexity is request-dependent.** A user asking for a simple button shouldn't fail because it's "not complex enough."

2. **Complexity proxies are easily gamed.** Line count and component count encourage bloat, not quality.

3. **The skill enables complexity, it doesn't require it.** The skill teaches Claude *how* to build artifacts. What to build is determined by the user.

4. **No fact of the matter.** Per CAPE's contextual objectivity principle, we only verify properties where there's an objective answer. "Is it valid JSX?" has a fact of the matter. "Is it complex enough?" does not.

**What we verify:** Is the code structurally correct?
**What we don't verify:** Is the artifact impressive?

---

## Predicate Details

| Predicate | What it catches | Why it's T1 |
|-----------|-----------------|-------------|
| `valid_jsx_syntax` | Syntax errors, unclosed tags | Won't compile |
| `jsx_parse_error_count` | Parse failures | Won't compile |
| `unresolved_import_count` | Missing dependencies | Won't run |
| `invalid_tailwind_class_count` | Typos in class names | Styling won't apply |
| `hooks_rules_violations` | Conditional hooks, nested hooks | React will crash or behave incorrectly |
| `has_default_export` | No entry point | Can't render |
| `source_size_bytes` | Oversized source | Environment limit |

---

## Not Mapped (Would Require Execution)

| Guidance | Why not mapped |
|----------|----------------|
| "Renders successfully" | Requires running React |
| "No console errors" | Requires runtime |
| "Bundle size" | Requires bundling step |

These are verified via structural proxies (valid syntax, correct hooks, resolved imports) rather than runtime behavior.

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "complex artifacts" | Request-dependent, no objective threshold | Retained as skill guidance |
| "elaborate" | Subjective quality judgment | Retained as skill guidance |
| "beautiful" | Aesthetic preference | Retained as skill guidance |
| "modern frontend" | Vague; valid React is already verified | Retained as skill guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 7 | Static analysis |
| T2 (Governance) | 0 | None in source skill |
| T3 (Quality) | 0 | Intentionally omitted (see above) |
| Non-verifiable | 4 | Documented |
| **Total** | **11** | — |
