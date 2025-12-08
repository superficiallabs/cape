# PredicateGraph Specification

**Version**: 1.0.0
**Status**: Stable

## Overview

A PredicateGraph is a structured representation of an AI model's output that enables deterministic policy evaluation. It decomposes natural language responses into typed, queryable nodes.

## Schema Version

This specification corresponds to schema version `1.0.0`.

## Structure

A PredicateGraph contains the following top-level fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | Yes | Schema version (semver) |
| `output_id` | string | Yes | Unique identifier for this output |
| `text` | string | Yes | Original model output text |
| `entities` | array | Yes | Extracted entities |
| `claims` | array | Yes | Extracted claims |
| `operations` | array | Yes | Mathematical/logical operations |
| `tool_calls` | array | Yes | Tool/function calls |
| `citations` | array | Yes | Source citations |
| `code_blocks` | array | Yes | Code snippets |
| `discourse_acts` | array | Yes | Discourse structure |
| `context` | object | No | Request context |

## Node Types

### Entities

Entities represent named objects, concepts, or references in the output.

```json
{
  "id": "e1",
  "text": "Python",
  "type": "PROGRAMMING_LANGUAGE",
  "span": { "start": 0, "end": 6 },
  "attributes": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique entity identifier |
| `text` | string | Yes | Entity surface form |
| `type` | string | Yes | Entity type |
| `span` | object | Yes | Character offsets |
| `attributes` | object | No | Additional properties |

### Claims

Claims represent assertions or statements made in the output.

```json
{
  "id": "c1",
  "text": "The function returns a list",
  "modality": "factual",
  "domain": "programming",
  "span": { "start": 10, "end": 37 },
  "entity_refs": ["e1"],
  "evidence": []
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique claim identifier |
| `text` | string | Yes | Claim text |
| `modality` | string | Yes | Claim type (factual, opinion, conditional, etc.) |
| `domain` | string | No | Subject domain |
| `span` | object | Yes | Character offsets |
| `entity_refs` | array | No | Referenced entity IDs |
| `evidence` | array | No | Supporting evidence |

#### Modality Types

- `factual`: Assertion of fact
- `opinion`: Subjective statement
- `conditional`: Dependent on conditions
- `hypothetical`: Speculative statement
- `instruction`: Directive or command

### Operations

Operations represent calculations or logical operations.

```json
{
  "id": "op1",
  "type": "arithmetic",
  "operator": "multiply",
  "operands": [100, 0.15],
  "result": 15,
  "span": { "start": 50, "end": 70 }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique operation identifier |
| `type` | string | Yes | Operation type |
| `operator` | string | Yes | Specific operator |
| `operands` | array | Yes | Input values |
| `result` | any | Yes | Computed result |
| `span` | object | Yes | Character offsets |

### Tool Calls

Tool calls represent function invocations.

```json
{
  "id": "tc1",
  "name": "calculate_tip",
  "arguments": {
    "bill_amount": 100,
    "tip_percentage": 15
  },
  "span": { "start": 0, "end": 50 }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique tool call identifier |
| `name` | string | Yes | Function name |
| `arguments` | object | Yes | Function arguments |
| `span` | object | Yes | Character offsets |

### Citations

Citations link claims to sources.

```json
{
  "id": "cit1",
  "claim_id": "c1",
  "source": {
    "type": "url",
    "value": "https://example.com/doc"
  },
  "span": { "start": 100, "end": 130 }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique citation identifier |
| `claim_id` | string | Yes | Referenced claim ID |
| `source` | object | Yes | Source information |
| `span` | object | No | Character offsets |

### Code Blocks

Code blocks represent code snippets.

```json
{
  "id": "cb1",
  "language": "python",
  "code": "def hello():\n    print('Hello')",
  "span": { "start": 200, "end": 250 }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique code block identifier |
| `language` | string | Yes | Programming language |
| `code` | string | Yes | Code content |
| `span` | object | Yes | Character offsets |

### Discourse Acts

Discourse acts represent the communicative structure.

```json
{
  "id": "da1",
  "type": "EXPLANATION",
  "span": { "start": 0, "end": 100 },
  "claim_refs": ["c1", "c2"],
  "children": ["da2"]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique discourse act identifier |
| `type` | string | Yes | Act type |
| `span` | object | Yes | Character offsets |
| `claim_refs` | array | No | Referenced claim IDs |
| `children` | array | No | Child discourse act IDs |

#### Discourse Act Types

- `GREETING`: Opening salutation
- `ACKNOWLEDGMENT`: Recognition of user input
- `CLARIFICATION`: Request for more information
- `EXPLANATION`: Detailed description
- `REASONING`: Logical argumentation
- `ASSERTION`: Direct statement
- `INSTRUCTION`: Step-by-step guidance
- `WARNING`: Caution or alert
- `SUMMARY`: Condensed overview
- `CLOSING`: Final remarks

## Context

The optional context object provides request information.

```json
{
  "context": {
    "user_query": "Calculate a 15% tip on $100",
    "system_prompt": "You are a helpful assistant",
    "tools_available": ["calculate_tip"]
  }
}
```

## Span Objects

All span objects have the same structure:

```json
{
  "start": 0,
  "end": 10
}
```

- `start`: Inclusive start character offset (0-indexed)
- `end`: Exclusive end character offset

## Example

See `examples/tool-use/tip-calc-violation.json` for a complete example.

## Validation

PredicateGraphs must validate against `schemas/predicate-graph-v1.0.0.json`.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




