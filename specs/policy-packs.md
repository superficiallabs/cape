# Policy Packs Specification

**Version**: 1.0.0
**Status**: Stable

## Overview

Policy Packs are versioned collections of related CPL policies. They provide a way to distribute, share, and apply coherent sets of capability requirements.

## Schema Version

This specification corresponds to schema version `1.0.0`.

## Structure

A Policy Pack contains:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `pack_id` | string | Yes | Unique pack identifier |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | Pack description |
| `version` | string | Yes | Pack version (semver) |
| `policies` | array | Yes | Included policies |
| `dependencies` | array | No | Required packs |
| `metadata` | object | No | Additional metadata |

## Naming Convention

Pack IDs follow the pattern: `<scope>.<capability>.v<major>`

- **scope**: `core` for official packs, organization name for others
- **capability**: The capability being evaluated
- **version**: Major version number

Examples:
- `core.tool-use.v1`
- `core.citation-grounding.v1`
- `acme.customer-support.v1`

## Policies Array

Each policy in the pack follows the CPL specification:

```json
{
  "policies": [
    {
      "policy_id": "tool-args-valid",
      "name": "Tool Arguments Valid",
      "description": "Tool call arguments match expected schema",
      "version": "1.0.0",
      "rules": [...]
    }
  ]
}
```

## Dependencies

Packs can depend on other packs:

```json
{
  "dependencies": [
    {
      "pack_id": "core.tool-use.v1",
      "version": ">=1.0.0"
    }
  ]
}
```

### Version Constraints

- `1.0.0`: Exact version
- `>=1.0.0`: Minimum version
- `>=1.0.0 <2.0.0`: Version range
- `^1.0.0`: Compatible with 1.x.x
- `~1.0.0`: Compatible with 1.0.x

## Metadata

Optional metadata fields:

```json
{
  "metadata": {
    "author": "Superficial Labs",
    "license": "Apache-2.0",
    "homepage": "https://github.com/superficiallabs/cape",
    "tags": ["tool-use", "function-calling"],
    "created": "2025-12-01",
    "updated": "2025-12-01"
  }
}
```

## Core Packs

### core.tool-use.v1

Validates tool/function call correctness:

- Argument types match schema
- Required arguments present
- No extra arguments
- Values within constraints

### core.citation-grounding.v1

Validates citation requirements:

- Factual claims have citations
- Citations reference valid sources
- Citation format is correct

### core.safe-code.v1

Validates code safety:

- No dangerous patterns
- No secrets/credentials
- Safe library usage
- Input validation present

## Custom Packs

Organizations can create custom packs for domain-specific requirements.

### Example: Customer Support Pack

```json
{
  "pack_id": "example.customer-support.v1",
  "name": "Customer Support Quality",
  "description": "Policies for customer support interactions",
  "version": "1.0.0",
  "policies": [
    {
      "policy_id": "greeting-required",
      "name": "Greeting Required",
      "description": "Response must include a greeting",
      "version": "1.0.0",
      "rules": [
        {
          "rule_id": "has-greeting",
          "description": "Must have GREETING discourse act",
          "expression": {
            "exists": {
              "var": "da",
              "in": "discourse_acts",
              "condition": {
                "predicate": "has_discourse_type",
                "args": ["da", "GREETING"]
              }
            }
          }
        }
      ]
    }
  ]
}
```

## Evaluation

When evaluating a pack:

1. Load all dependencies
2. Evaluate each policy in order
3. Aggregate results across all policies
4. Report overall pass/fail

### Result Format

```json
{
  "pack_id": "core.tool-use.v1",
  "passed": false,
  "policy_results": [
    {
      "policy_id": "tool-args-valid",
      "passed": false,
      "violations": [
        {
          "rule_id": "args-match-schema",
          "node_id": "tc1",
          "message": "Argument 'amount' has wrong type",
          "severity": "error"
        }
      ]
    }
  ]
}
```

## Validation

Policy Packs must validate against `schemas/policy-pack-v1.0.0.json`.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




