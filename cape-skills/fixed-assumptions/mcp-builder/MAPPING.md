# Mapping: mcp-builder

> **Source:** [anthropics/skills/mcp-builder](https://github.com/anthropics/skills/tree/main/mcp-builder)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Assumptions:** [ASSUMPTIONS.md](./ASSUMPTIONS.md)
>
> **Reference:** [MCP Specification](https://modelcontextprotocol.io/)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | "MCP servers" | T1 | `manifest_exists(server) == true` | Direct |
| 2 | "MCP servers" | T1 | `manifest_schema_valid(server) == true` | Direct |
| 3 | "MCP servers" | T1 | `has_endpoint_handler(server, 'list_tools') == true` | Direct |
| 4 | "MCP servers" | T1 | `has_endpoint_handler(server, 'call_tool') == true` | Direct |
| 5 | "MCP servers" | T1 | `tools_without_handlers_count(server) == 0` | Direct |
| 6 | "MCP servers" | T1 | `invalid_tool_schema_count(server) == 0` | Direct |
| 7 | "production-ready" | T2 | `hardcoded_secret_count(server, ...) == 0` | Direct |
| 8 | "production-ready" | T2 | `tools_without_input_validation_count(server) == 0` | Direct |
| 9 | "production-ready" | T2 | `sql_injection_risk_count(server) == 0` | Direct |
| 10 | "production-ready" | T2 | `command_injection_risk_count(server) == 0` | Direct |
| 11 | "high-quality" | T3 | `lint_error_count(server) == 0` | Proxy |
| 12 | "high-quality" | T3 | `type_annotation_coverage(server) >= 0.9` | Proxy |
| 13 | "well-documented" | T3 | `readme_exists(server) == true` | Direct |
| 14 | "well-documented" | T3 | `tool_description_coverage(server) >= config.min_doc_coverage` | Proxy |
| 15 | "production-ready" | T3 | `tools_without_error_handling_count(server) == 0` | Proxy |

---

## Verification Approach

All predicates use **static analysis**. No server execution required.

| Analysis Type | Predicates |
|---------------|------------|
| File presence | Manifest exists, README exists |
| JSON Schema validation | Manifest schema, tool schemas |
| AST analysis | Endpoint handlers, tool handlers, error handling, type coverage |
| Pattern matching | Hardcoded secrets, SQL injection, command injection |
| Static linting | Lint errors |
| Manifest parsing | Tool descriptions |

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Manifest, endpoints, tool handlers, schemas | Protocol violations = broken server |
| **T2** | No secrets, input validation, no injection vectors | Security issues = unsafe to deploy |
| **T3** | Lint, types, README, tool descriptions, error handling | Quality/maintainability preferences |

**Note on "production-ready":** This guidance spans two tiers:
- **T2 (Security):** No hardcoded secrets, input validation, no injection vectors
- **T3 (Robustness):** Error handling present

Security issues are compliance failures; robustness issues are quality concerns.

---

## MCP Protocol Requirements (Static Verification)

| Requirement | Static Check | What it verifies |
|-------------|--------------|------------------|
| Valid manifest | `manifest_schema_valid()` | JSON conforms to MCP schema |
| `list_tools` endpoint | `has_endpoint_handler()` | Handler function exists in code |
| `call_tool` endpoint | `has_endpoint_handler()` | Handler function exists in code |
| Tools implemented | `tools_without_handlers_count()` | Each manifest tool has code handler |
| Valid tool schemas | `invalid_tool_schema_count()` | Input/output schemas are valid JSON Schema |

**Note:** These checks verify the code structure, not runtime behavior. A server can pass all checks and still fail at runtime due to logic errors.

---

## Security Checks (Static Analysis)

| Check | What it detects | How |
|-------|-----------------|-----|
| **Hardcoded secrets** | API keys, passwords in source | Pattern match variable names + literal values |
| **Input validation** | Missing schema validation | AST check for validation calls |
| **SQL injection** | String concatenation in queries | Pattern match unsafe SQL patterns |
| **Command injection** | User input in shell commands | Pattern match unsafe exec patterns |

---

## Non-Verifiable Guidance

| Guidance | Reason | Handling |
|----------|--------|----------|
| "Endpoints respond correctly" | Requires execution | Verify handler exists as proxy |
| "Tools return valid responses" | Requires execution | Verify schemas as proxy |
| "Useful tools" | Semantic utility | Retained as guidance |
| "Well-designed API" | Subjective design quality | Retained as guidance |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 6 | Static analysis |
| T2 (Security) | 4 | Static analysis |
| T3 (Quality) | 5 | Static analysis |
| Non-verifiable | 4 | Documented |
| **Total** | **19** | — |
