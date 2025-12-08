# CPL Specification

**Capability Policy Language**

**Version**: 1.0.0
**Status**: Stable

## Overview

CPL (Capability Policy Language) is a declarative language for specifying executable policies over PredicateGraphs. Policies define requirements that AI outputs must satisfy.

## Schema Version

This specification corresponds to schema version `1.0.0`.

## Policy Structure

A CPL policy contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policy_id` | string | Yes | Unique policy identifier |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | Policy description |
| `version` | string | Yes | Policy version (semver) |
| `rules` | array | Yes | Policy rules |
| `metadata` | object | No | Additional metadata |

## Rules

Each rule is a logical expression over the PredicateGraph.

```json
{
  "rule_id": "r1",
  "description": "All tool calls must have correct argument types",
  "expression": {
    "forall": {
      "var": "tc",
      "in": "tool_calls",
      "condition": {
        "predicate": "arguments_match_schema",
        "args": ["tc"]
      }
    }
  }
}
```

### Rule Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `rule_id` | string | Yes | Unique rule identifier |
| `description` | string | Yes | Human-readable description |
| `expression` | object | Yes | Logical expression |
| `severity` | string | No | Violation severity (error, warning, info) |

## Expressions

### Quantifiers

#### Universal Quantifier (forall)

```json
{
  "forall": {
    "var": "x",
    "in": "claims",
    "condition": { ... }
  }
}
```

Evaluates to true if the condition holds for all elements.

#### Existential Quantifier (exists)

```json
{
  "exists": {
    "var": "x",
    "in": "citations",
    "condition": { ... }
  }
}
```

Evaluates to true if the condition holds for at least one element.

### Logical Operators

#### Conjunction (and)

```json
{
  "and": [
    { "predicate": "p1", "args": ["x"] },
    { "predicate": "p2", "args": ["x"] }
  ]
}
```

#### Disjunction (or)

```json
{
  "or": [
    { "predicate": "p1", "args": ["x"] },
    { "predicate": "p2", "args": ["x"] }
  ]
}
```

#### Negation (not)

```json
{
  "not": {
    "predicate": "p1",
    "args": ["x"]
  }
}
```

#### Implication (implies)

```json
{
  "implies": {
    "if": { "predicate": "p1", "args": ["x"] },
    "then": { "predicate": "p2", "args": ["x"] }
  }
}
```

### Predicates

Predicates are atomic boolean functions.

```json
{
  "predicate": "has_citation",
  "args": ["claim"]
}
```

#### Built-in Predicates

| Predicate | Arguments | Description |
|-----------|-----------|-------------|
| `has_citation` | claim | Claim has a citation |
| `is_factual` | claim | Claim modality is factual |
| `has_type` | entity, type | Entity has specified type |
| `arguments_match_schema` | tool_call | Tool arguments match schema |
| `result_correct` | operation | Operation result is correct |
| `is_safe` | code_block | Code passes safety checks |
| `has_discourse_type` | discourse_act, type | Act has specified type |

#### Custom Predicates

Policies may define custom predicates:

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

### Comparisons

```json
{
  "compare": {
    "left": { "field": "x.confidence" },
    "op": ">=",
    "right": 0.8
  }
}
```

Operators: `==`, `!=`, `<`, `<=`, `>`, `>=`

### Field Access

Access node fields using dot notation:

```json
{
  "field": "tool_call.arguments.amount"
}
```

## Evaluation

### Algorithm

1. Parse the policy JSON
2. For each rule:
   a. Evaluate the expression against the PredicateGraph
   b. Record pass/fail and any violations
3. Aggregate results

### Violation Reporting

When a rule fails, report:

- `rule_id`: Failed rule
- `node_id`: Violating node (if applicable)
- `message`: Human-readable description
- `severity`: Error level

## Example Policy

```json
{
  "policy_id": "citation-required",
  "name": "Citation Required for Factual Claims",
  "description": "All factual claims must have citations",
  "version": "1.0.0",
  "rules": [
    {
      "rule_id": "factual-claims-cited",
      "description": "Every factual claim must have a citation",
      "expression": {
        "forall": {
          "var": "c",
          "in": "claims",
          "condition": {
            "implies": {
              "if": { "predicate": "is_factual", "args": ["c"] },
              "then": { "predicate": "has_citation", "args": ["c"] }
            }
          }
        }
      },
      "severity": "error"
    }
  ]
}
```

## Validation

CPL policies must validate against `schemas/cpl-policy-v1.0.0.json`.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




