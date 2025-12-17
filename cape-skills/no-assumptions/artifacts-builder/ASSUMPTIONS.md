# Assumptions: artifacts-builder

> **Source:** [anthropics/skills/artifacts-builder](https://github.com/anthropics/skills/tree/main/artifacts-builder)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)

---

## No Assumptions Required

This skill requires **no fixed assumptions**. All constraints are objectively verifiable (T1) through static code analysis:

| Constraint | Verification |
|------------|--------------|
| Valid React/JSX | Syntax parsing |
| Imports resolve | AST analysis against allowed list |
| Valid Tailwind classes | Pattern matching against class list |
| Hooks rules followed | Static analysis (eslint-plugin-react-hooks style) |
| Has default export | AST check |
| Source size limit | Byte count |

---

## Verification Approach

All predicates use **static code analysis**. No execution or rendering required.

This means we verify the code is *structurally correct*, not that it *runs correctly*. A component can pass all static checks and still fail at runtime due to logic errors. However, static checks catch the majority of issues:

- Syntax errors → caught by parser
- Missing imports → caught by import resolution
- Invalid Tailwind → caught by class validation
- Hooks violations → caught by static analysis
- Missing export → caught by AST check

---

## Why Not Verify "Complexity"?

The source skill mentions "complex" and "elaborate" artifacts. We intentionally do **not** create T3 proxies for these because:

**1. Complexity is request-dependent**

A simple button component is correct if that's what the user asked for. Requiring minimum component counts or line counts would fail valid requests.

**2. Proxies would encourage bad code**

- `line_count >= 50` → Encourages verbose, padded code
- `component_count >= 2` → Encourages artificial splitting
- `has_state_management` → Not all artifacts need state

A well-crafted 30-line stateless component is better than a bloated 100-line component with unnecessary complexity.

**3. No objective threshold exists**

Per CAPE's contextual objectivity principle: we verify properties where there's a fact of the matter. "Is it valid JSX?" is objective. "Is it complex enough?" depends entirely on context not present in the skill.

---

## Why Not Verify Runtime Behavior?

The original policy included execution-dependent predicates:

| Removed Predicate | Why removed |
|-------------------|-------------|
| `renders_successfully(artifact)` | Requires running React |
| `console_error_count(artifact)` | Requires runtime environment |
| `bundle_size(artifact)` | Requires bundling step |

CAPE verifies **outputs**, not **behaviors**. An artifact is code—we verify the code structure. Whether that code behaves correctly when rendered is downstream of CAPE's scope.

The static checks we keep (valid syntax, correct hooks, resolved imports) catch the issues that *prevent* successful rendering. Code that passes these checks is likely to render correctly.

---

## Extending This Policy

If your use case requires complexity verification (e.g., teaching/evaluation contexts), you could add T3 policies:

```json
{
  "id": "policy.artifacts_builder.complexity",
  "tier": "T3",
  "description": "Artifact meets minimum complexity threshold",
  "assert": [
    { "expr": "component_count(code) >= config.min_components OR line_count(code) >= config.min_lines", "msg": "Artifact below complexity threshold" }
  ]
}
```

With configuration:
```json
{
  "min_components": 2,
  "min_lines": 50
}
```

This is **not included by default** because it would cause false failures for legitimate simple artifacts.
