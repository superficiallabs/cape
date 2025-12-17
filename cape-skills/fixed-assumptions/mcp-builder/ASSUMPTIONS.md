# Assumptions: mcp-builder

> **Source:** [anthropics/skills/mcp-builder](https://github.com/anthropics/skills/tree/main/mcp-builder)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Reference:** [MCP Specification](https://modelcontextprotocol.io/)

---

## Overview

The mcp-builder skill asks for "high-quality," "well-documented," and "production-ready" MCP servers. These are interpreted as specific, verifiable properties via static code analysis:

- **T1 (Correctness):** Protocol compliance—manifest valid, handlers exist, schemas valid
- **T2 (Security):** No secrets, input validation, no injection vectors
- **T3 (Quality):** Lint clean, typed, documented, error handling present

**Philosophy:** MCP servers are infrastructure. "Production-ready" means they won't break, leak secrets, or be unmaintainable. We verify these properties through code analysis.

**Verification approach:** All predicates use static analysis—file inspection, JSON Schema validation, AST analysis, and pattern matching. No server execution required.

---

## Assumption 1: Code Quality (Lint + Types)

**Original guidance:**
> "high-quality MCP server"

**Interpretation:**
"High-quality" code passes standard quality checks: no linter errors and complete type annotations.

**Predicates:**
```
lint_error_count(server) == 0
type_annotation_coverage(server) >= 0.9
```

**Tier:** T3 (Preference)

**Default configuration:**
```json
{
  "require_type_hints": true
}
```

**Static verification:**
- Lint: Run ESLint (JS/TS) or Ruff/Pylint (Python) in check mode
- Types: AST analysis to count typed vs untyped function signatures

**Threshold rationale:**

| Lint errors | Interpretation |
|-------------|----------------|
| 0 | Clean code (required) |
| 1–5 | Minor issues—should fix |
| 5+ | Quality problems |

| Type coverage | Interpretation |
|---------------|----------------|
| < 50% | Mostly untyped |
| 50–80% | Partially typed |
| 80–90% | Well typed |
| 90%+ | Fully typed (default threshold) |

**Customization:**
- Prototype: set `require_type_hints: false`
- Strict typing: raise coverage to `1.0` (100%)

---

## Assumption 2: Documentation Coverage

**Original guidance:**
> "well-documented"

**Interpretation:**
"Well-documented" means: README exists AND all tools have descriptions.

**Predicates:**
```
readme_exists(server) == true
tool_description_coverage(server) >= config.min_doc_coverage
```

**Tier:** T3 (Preference)

**Default configuration:**
```json
{
  "min_doc_coverage": 1.0
}
```

**Static verification:**
- README: File existence check
- Tool descriptions: Parse manifest, check `description` field on each tool

**Customization:**
- Internal tools: lower to `0.8` (80%)
- Public API: keep at `1.0` (100%)

---

## Assumption 3: Security (No Secrets)

**Original guidance:**
> "production-ready"

**Interpretation:**
Production servers must not contain hardcoded secrets.

**Predicate:**
```
hardcoded_secret_count(server, config.secret_patterns) == 0
```

**Tier:** T2 (Governance)—Security issues are compliance failures

**Default configuration:**
```json
{
  "secret_patterns": ["api_key", "password", "secret", "token", "credential"]
}
```

**Static verification:** Pattern match variable names containing secret-related terms that are assigned literal string values.

**What this detects:**
- `API_KEY = "sk-..."`
- `password = "hunter2"`
- `const token = "abc123"`

**What this doesn't detect:**
- Secrets in external config files
- Obfuscated secrets
- Non-standard naming

**Customization:**
- Add domain-specific patterns: `"aws_secret"`, `"stripe_key"`, etc.

---

## Assumption 4: Security (Input Validation)

**Original guidance:**
> "production-ready"

**Interpretation:**
Production servers must validate all tool inputs.

**Predicate:**
```
tools_without_input_validation_count(server) == 0
```

**Tier:** T2 (Governance)

**Static verification:** AST analysis to check for validation patterns:
- JSON Schema definitions for tool arguments
- Runtime type checking calls (Zod, Pydantic, etc.)
- Explicit validation code

**Customization:**
- Allow some tools without validation: use threshold instead of zero

---

## Assumption 5: Security (No Injection Vectors)

**Original guidance:**
> "production-ready"

**Interpretation:**
Production servers must not have obvious injection vulnerabilities.

**Predicates:**
```
sql_injection_risk_count(server) == 0
command_injection_risk_count(server) == 0
```

**Tier:** T2 (Governance)

**Static verification:** Pattern matching for dangerous patterns:
- String concatenation in SQL: `"SELECT * FROM users WHERE id = " + userId`
- User input in shell: `exec("ls " + userPath)`

**What this detects:**
- Obvious string concatenation patterns
- Direct user input in dangerous contexts

**What this doesn't detect:**
- Sophisticated injection patterns
- Logic flaws

**Note:** This is static analysis, not penetration testing.

---

## Assumption 6: Error Handling (Robustness)

**Original guidance:**
> "production-ready"

**Interpretation:**
Production servers should handle errors gracefully.

**Predicate:**
```
tools_without_error_handling_count(server) == 0
```

**Tier:** T3 (Preference)—Robustness is quality, not security

**Static verification:** AST analysis to check for:
- Try/catch blocks around tool logic
- Error response patterns

**Customization:**
- Allow some tools without handling: use threshold

---

## Not Verified (Would Require Execution)

| Guidance | Why not mapped |
|----------|----------------|
| "Endpoints respond" | Requires running server |
| "Tools callable" | Requires invoking tools |
| "Valid responses" | Requires runtime checks |
| "Response time" | Requires execution measurement |

These are verified via structural proxies (handler exists, schema valid) rather than runtime behavior.

---

## Not Verified (Genuinely Subjective)

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Useful tools" | Semantic utility | Retained as guidance |
| "Well-designed API" | Subjective design | Retained as guidance |
| "Appropriate for use case" | Context-dependent | Retained as guidance |

---

## Configuration Reference

```json
{
  "configuration": {
    "require_type_hints": true,
    "min_doc_coverage": 1.0,
    "required_endpoints": ["list_tools", "call_tool"],
    "secret_patterns": ["api_key", "password", "secret", "token", "credential"]
  }
}
```

Override any threshold at evaluation time to match your deployment requirements.
