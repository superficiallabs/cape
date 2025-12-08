# Extraction Specification

**Version**: 1.0.0
**Status**: Stable

## Overview

Extraction is the process of converting unstructured AI model output into a structured PredicateGraph. This specification defines the extraction task, quality metrics, and guidance for each node type.

## Extraction Pipeline

```
┌──────────────┐     ┌─────────────┐     ┌─────────────────┐
│ Model Output │────>│  Extractor  │────>│ PredicateGraph  │
│    (text)    │     │             │     │   (structured)  │
└──────────────┘     └─────────────┘     └─────────────────┘
```

## Task Definition

Given:
- Raw text output from an AI model
- Optional context (user query, system prompt, available tools)

Produce:
- A valid PredicateGraph with all relevant nodes extracted

## Quality Metrics

### Completeness

All relevant information from the output should be captured:

| Metric | Definition |
|--------|------------|
| Entity Recall | % of entities correctly identified |
| Claim Recall | % of claims correctly identified |
| Relation Recall | % of relationships correctly linked |

### Accuracy

Extracted information should match the source:

| Metric | Definition |
|--------|------------|
| Span Accuracy | Character offsets match source text |
| Type Accuracy | Node types correctly assigned |
| Attribute Accuracy | Properties correctly extracted |

### Consistency

The graph should be internally coherent:

| Metric | Definition |
|--------|------------|
| Reference Validity | All refs point to existing nodes |
| Span Coverage | Spans don't overlap incorrectly |
| ID Uniqueness | All IDs are unique within type |

## Error Types

### Extraction Errors

| Error | Description | Severity |
|-------|-------------|----------|
| Missing Entity | Entity not extracted | Major |
| Missing Claim | Claim not extracted | Major |
| Wrong Type | Incorrect type assigned | Minor |
| Wrong Span | Incorrect character offsets | Minor |
| Dangling Reference | Reference to non-existent node | Major |
| Duplicate ID | Same ID used twice | Critical |

### Structural Errors

| Error | Description | Severity |
|-------|-------------|----------|
| Invalid JSON | Output not valid JSON | Critical |
| Schema Violation | Doesn't match schema | Critical |
| Missing Required | Required field absent | Critical |

## Node-Type Specific Guidance

### Entities

**When to extract:**
- Named objects, people, places, organizations
- Technical concepts (languages, frameworks, algorithms)
- Quantities with units
- References to external resources

**Type assignment:**
- Use domain-appropriate types
- Be consistent within a graph
- Prefer specific over generic types

**Example types:**
- `PERSON`, `ORGANIZATION`, `LOCATION`
- `PROGRAMMING_LANGUAGE`, `FRAMEWORK`, `LIBRARY`
- `QUANTITY`, `DATE`, `CURRENCY`

### Claims

**When to extract:**
- Assertions of fact
- Opinions and judgments
- Instructions and recommendations
- Conditional statements

**Modality assignment:**
- `factual`: "Python is a programming language"
- `opinion`: "Python is the best language"
- `conditional`: "If you need speed, use Rust"
- `instruction`: "Install the package using pip"

**Granularity:**
- Extract atomic claims
- Break compound statements into separate claims
- Link related claims via entity references

### Operations

**When to extract:**
- Explicit calculations
- Logical deductions
- Data transformations

**Capture:**
- All operands (values used)
- The operator (what operation)
- The result (what was computed)
- The span (where in text)

### Tool Calls

**When to extract:**
- Function invocations
- API calls
- System commands

**Capture:**
- Function name exactly as written
- All arguments with their values
- Argument types

### Citations

**When to extract:**
- URLs referenced
- Documents cited
- Sources mentioned

**Link:**
- Each citation to its claim
- Multiple citations can support one claim
- One citation can support multiple claims

### Code Blocks

**When to extract:**
- Fenced code blocks
- Inline code snippets
- Shell commands

**Capture:**
- Language if specified
- Complete code content
- Exact span boundaries

### Discourse Acts

**When to extract:**
- Major structural segments
- Functional units of communication

**Hierarchy:**
- Top-level acts for main sections
- Child acts for sub-sections
- Link to relevant claims

## Extraction Strategies

### Rule-Based

Pattern matching for structured elements:

```
Code blocks: /```(\w+)?\n([\s\S]*?)```/
Citations: /\[(\d+)\]|https?:\/\/[^\s]+/
Tool calls: /function_name\(.*\)/
```

### Model-Based

Neural extraction for semantic elements:

- Named Entity Recognition for entities
- Claim detection models for claims
- Discourse parsing for structure

### Hybrid

Combine approaches:

1. Rule-based for syntactic elements (code, citations)
2. Model-based for semantic elements (claims, entities)
3. Post-processing for consistency

## Validation

After extraction:

1. Validate against PredicateGraph schema
2. Check all references resolve
3. Verify span consistency
4. Ensure ID uniqueness

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




