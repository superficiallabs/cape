# Predicate Reference

**Version**: 1.0.0
**Status**: Stable

## Overview

This document defines the semantics of built-in predicates used in CPL policies. Predicates are atomic boolean functions that evaluate properties of PredicateGraph nodes.

## Predicate Categories

Predicates are organized by the node types they operate on:

- **Tool Call Predicates**: Evaluate `tool_calls` nodes
- **Claim Predicates**: Evaluate `claims` nodes
- **Citation Predicates**: Evaluate `citations` nodes
- **Code Block Predicates**: Evaluate `code_blocks` nodes
- **Discourse Act Predicates**: Evaluate `discourse_acts` nodes

---

## Tool Call Predicates

### `arguments_match_schema`

**Arguments**: `tool_call`

**Description**: Checks whether all arguments in a tool call match their expected types as defined in the tool's schema.

**Semantics**:
- Returns `true` if every argument in `tool_call.arguments` has the correct type according to the tool's parameter schema
- Returns `false` if any argument has an incorrect type (e.g., string where number expected)
- Type checking is strict: `"100"` (string) does not match `number` type

**Example Violation**:
```json
{
  "tool_name": "calculate_tip",
  "arguments": {
    "bill_amount": "100",  // Should be number, not string
    "tip_percentage": 15
  }
}
```

---

### `has_required_arguments`

**Arguments**: `tool_call`

**Description**: Checks whether all required arguments are present in the tool call.

**Semantics**:
- Returns `true` if all parameters marked as `required` in the tool schema are present in `tool_call.arguments`
- Returns `false` if any required argument is missing
- Optional arguments do not affect the result

**Example Violation**:
```json
{
  "tool_name": "send_email",
  "arguments": {
    "subject": "Hello"
    // Missing required "to" argument
  }
}
```

---

### `no_extra_arguments`

**Arguments**: `tool_call`

**Description**: Checks that no unexpected arguments are provided beyond those defined in the tool schema.

**Semantics**:
- Returns `true` if all keys in `tool_call.arguments` are defined in the tool schema
- Returns `false` if any argument key is not in the schema
- Useful for catching typos or hallucinated parameters

**Example Violation**:
```json
{
  "tool_name": "get_weather",
  "arguments": {
    "location": "NYC",
    "tempurature_unit": "celsius"  // Typo: "temperature_unit" is the correct name
  }
}
```

---

### `tool_is_available`

**Arguments**: `tool_call`

**Description**: Checks whether the tool being called exists in the available tools list.

**Semantics**:
- Returns `true` if `tool_call.tool_name` matches a tool in the context's available tools
- Returns `false` if the tool name is not found
- Comparison is case-sensitive and exact

**Example Violation**:
```json
{
  "tool_name": "send_sms",  // Tool not in available tools list
  "arguments": { "to": "+1234567890", "message": "Hello" }
}
```

---

## Claim Predicates

### `is_factual`

**Arguments**: `claim`

**Description**: Checks whether a claim asserts a factual statement about the world.

**Semantics**:
- Returns `true` if `claim.modality` equals `"factual"`
- Returns `false` for other modalities: `"hedged"`, `"conditional"`, `"opinion"`, etc.
- Factual claims assert something as objectively true

**Examples**:
- Factual: "The Earth orbits the Sun" → `is_factual` returns `true`
- Hedged: "The project might be delayed" → `is_factual` returns `false`
- Opinion: "Python is the best language" → `is_factual` returns `false`

---

### `has_citation`

**Arguments**: `claim`

**Description**: Checks whether a claim has at least one supporting citation.

**Semantics**:
- Returns `true` if there exists a citation node where `citation.claim_id` equals `claim.node_id`
- Returns `false` if no citation references this claim
- Does not validate citation quality or accuracy

**Example**:
```json
// Claim
{ "node_id": "claim_1", "text": "GDP grew 3% in Q4", "modality": "factual" }

// Citation (if present, has_citation returns true)
{ "node_id": "cit_1", "claim_id": "claim_1", "source": "Bureau of Economic Analysis" }
```

---

## Citation Predicates

### `has_valid_source`

**Arguments**: `citation`

**Description**: Checks whether a citation has a properly specified source.

**Semantics**:
- Returns `true` if `citation.source` is a non-empty string
- Returns `false` if source is empty, null, or missing
- Does not validate that the source actually exists or is accessible

---

### `refs_existing_claim`

**Arguments**: `citation`

**Description**: Checks whether a citation references an existing claim in the PredicateGraph.

**Semantics**:
- Returns `true` if `citation.claim_id` matches the `node_id` of a claim in `claims`
- Returns `false` if the referenced claim does not exist
- Catches orphaned citations that reference non-existent claims

---

## Code Block Predicates

### `contains_eval`

**Arguments**: `code_block`

**Description**: Checks whether code contains dangerous dynamic execution functions.

**Semantics**:
- Returns `true` if the code contains patterns like:
  - Python: `eval()`, `exec()`, `compile()`
  - JavaScript: `eval()`, `Function()`, `setTimeout(string)`
  - Similar constructs in other languages
- Returns `false` if no such patterns are found
- Detection is syntax-aware, not just string matching (avoids false positives in comments/strings)

**Example Violation**:
```python
user_input = input("Enter expression: ")
result = eval(user_input)  # Dangerous: arbitrary code execution
```

---

### `vulnerable_to_injection`

**Arguments**: `code_block`

**Description**: Checks whether code is vulnerable to shell injection attacks.

**Semantics**:
- Returns `true` if the code constructs shell commands from untrusted input without sanitization
- Patterns detected include:
  - `os.system(f"cmd {user_input}")`
  - `subprocess.call(cmd, shell=True)` with string interpolation
  - Similar patterns in other languages
- Returns `false` if shell commands use safe patterns (e.g., argument arrays)

**Example Violation**:
```python
import os
filename = input("Enter filename: ")
os.system(f"cat {filename}")  # Vulnerable: user could input "; rm -rf /"
```

**Safe Alternative**:
```python
import subprocess
filename = input("Enter filename: ")
subprocess.run(["cat", filename])  # Safe: arguments are not shell-interpreted
```

---

### `contains_secrets`

**Arguments**: `code_block`

**Description**: Checks whether code contains hardcoded credentials or secrets.

**Semantics**:
- Returns `true` if the code contains patterns indicating hardcoded secrets:
  - API keys: `api_key = "sk-..."`, `AWS_SECRET_KEY = "..."`
  - Passwords: `password = "..."`, `pwd = "admin123"`
  - Tokens: `token = "ghp_..."`, `bearer_token = "..."`
- Returns `false` if credentials are loaded from environment or secure storage
- Uses heuristics including variable names, value patterns, and entropy analysis

**Example Violation**:
```python
API_KEY = "sk-1234567890abcdef"  # Hardcoded secret
```

**Safe Alternative**:
```python
import os
API_KEY = os.environ.get("API_KEY")  # Loaded from environment
```

---

### `uses_safe_libraries`

**Arguments**: `code_block`

**Description**: Checks whether code uses known-safe libraries and avoids deprecated/unsafe ones.

**Semantics**:
- Returns `true` if all imported libraries are considered safe
- Returns `false` if code imports known-unsafe or deprecated libraries:
  - Python: `pickle` (insecure deserialization), `md5` (weak hash)
  - JavaScript: deprecated crypto methods
- Severity is typically `warning` rather than `error`

---

## Discourse Act Predicates

### `has_discourse_type`

**Arguments**: `discourse_act`, `type`

**Description**: Checks whether a discourse act has a specific type.

**Semantics**:
- Returns `true` if `discourse_act.act_type` equals the specified `type`
- Returns `false` otherwise
- Common discourse types include:
  - `GREETING` - Salutation or hello
  - `ACKNOWLEDGMENT` - Recognition of user's issue
  - `QUESTION` - Interrogative act
  - `ANSWER` - Response to question
  - `INSTRUCTION` - Directive or command
  - `CLOSING` - Sign-off or goodbye
  - `REASONING` - Logical argumentation

**Example**:
```json
{
  "exists": {
    "var": "da",
    "in": "discourse_acts",
    "condition": {
      "predicate": "has_discourse_type",
      "args": ["da", "ACKNOWLEDGMENT"]
    }
  }
}
```

---

### `is_professional_tone`

**Arguments**: `claim` or `discourse_act`

**Description**: Checks whether text maintains a professional tone appropriate for business communication.

**Semantics**:
- Returns `true` if the text avoids:
  - Excessive informality (slang, casual abbreviations)
  - Inappropriate humor
  - Overly emotional language
  - Unprofessional expressions
- Returns `false` if unprofessional patterns are detected
- Implementation may use rule-based or ML-based detection

---

## Implementing Custom Predicates

CPL policies can define custom predicates that compose built-in predicates:

```json
{
  "custom_predicates": {
    "is_grounded": {
      "params": ["claim"],
      "expression": {
        "or": [
          { "predicate": "has_citation", "args": ["claim"] },
          { "not": { "predicate": "is_factual", "args": ["claim"] } }
        ]
      }
    }
  }
}
```

Custom predicates:
- Must have unique names that don't conflict with built-in predicates
- Can reference other custom predicates (no circular dependencies)
- Are scoped to the policy or pack where they are defined

---

## Predicate Evaluation

### Evaluation Context

Predicates are evaluated with access to:
- The current node being examined
- The full PredicateGraph for cross-references
- Tool schemas (for tool validation predicates)
- Configuration parameters (thresholds, allow-lists, etc.)

### Error Handling

When predicate evaluation fails:
- Missing required fields: Returns `false` with diagnostic
- Invalid node references: Returns `false` with diagnostic
- Runtime errors: Propagated as evaluation failures

### Performance Considerations

- Predicates should be stateless and side-effect free
- Complex predicates (e.g., `vulnerable_to_injection`) may use caching
- Cross-reference predicates (e.g., `refs_existing_claim`) should use indexed lookups

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |






