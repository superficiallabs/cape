# Learned Verifiers Specification

**Version**: 1.0.0
**Status**: Stable

## Overview

Learned Verifiers complement symbolic CPL policies by handling semantic verification tasks that require understanding beyond structural checks. They use trained models to evaluate properties like argument soundness, proof validity, and plan feasibility.

## Schema Version

This specification corresponds to schema version `1.0.0`.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  PredicateGraph │────>│   CPL Policies  │──> Structural Results
└─────────────────┘     └─────────────────┘
         │
         │              ┌─────────────────┐
         └─────────────>│ Learned Verifier│──> Semantic Results
                        └─────────────────┘
```

## Rubric Structure

A Verifier Rubric defines how a learned verifier should evaluate outputs.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `verifier_id` | string | Yes | Unique verifier identifier |
| `name` | string | Yes | Human-readable name |
| `description` | string | Yes | What this verifier evaluates |
| `version` | string | Yes | Rubric version (semver) |
| `input_schema` | object | Yes | Expected PredicateGraph structure |
| `output_schema` | object | Yes | Evaluation output structure |
| `training_objective` | string | Yes | Training description |
| `meta_verification` | boolean | No | Whether to verify the verifier |
| `metadata` | object | No | Additional metadata |

## Verifier Categories

### Reasoning Verifiers

Evaluate logical reasoning quality:

- **Argument Soundness**: Are premises true and conclusions valid?
- **Deductive Validity**: Does the conclusion follow from premises?
- **Inductive Strength**: Is the evidence sufficient?

### Mathematics Verifiers

Evaluate mathematical correctness:

- **Proof Validity**: Is the proof correct and complete?
- **Calculation Accuracy**: Are computations correct?
- **Step Justification**: Are all steps justified?

### Agent Verifiers

Evaluate agent behavior:

- **Plan Feasibility**: Can the plan achieve its goal?
- **Action Safety**: Are proposed actions safe?
- **Goal Alignment**: Does behavior align with objectives?

## Output Schema

Verifier outputs follow a standard structure:

```json
{
  "verifier_id": "verifier.reasoning.argument_soundness",
  "evaluation": {
    "premises_true": true,
    "logic_valid": true,
    "conclusion_supported": true
  },
  "issues": [
    {
      "location": "premise_2",
      "description": "Premise is not supported by evidence",
      "severity": "major"
    }
  ],
  "score": 0.75,
  "reasoning": "The argument is logically valid but one premise lacks support."
}
```

### Standard Output Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `verifier_id` | string | Yes | Verifier that produced this |
| `evaluation` | object | Yes | Domain-specific evaluation |
| `issues` | array | Yes | Identified problems |
| `score` | number | Yes | Overall score (0-1) |
| `reasoning` | string | Yes | Explanation of evaluation |

### Issue Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `location` | string | Yes | Where the issue occurs |
| `description` | string | Yes | What the issue is |
| `severity` | string | Yes | fatal, major, minor |
| `issue_type` | string | No | Categorization |

## Training

### Training Objective

Each rubric specifies a training objective:

```json
{
  "training_objective": "Evaluate argument soundness by checking premise truth and logical validity; identify specific fallacies and unsupported claims"
}
```

### Training Data Format

Training examples pair PredicateGraphs with expected outputs:

```json
{
  "input": { "...PredicateGraph..." },
  "expected_output": { "...Verifier Output..." },
  "notes": "Example of unsound argument due to false premise"
}
```

## Meta-Verification

When `meta_verification` is true, the verifier's output is itself verified:

1. Check output conforms to schema
2. Validate reasoning is coherent
3. Ensure score matches issues
4. Verify all issues are actionable

## Integration with CPL

Learned verifiers can be referenced in CPL policies:

```json
{
  "rule_id": "reasoning-sound",
  "description": "Reasoning must be sound",
  "expression": {
    "verifier": {
      "id": "verifier.reasoning.argument_soundness",
      "threshold": 0.8
    }
  }
}
```

## Example Rubric

```json
{
  "verifier_id": "verifier.reasoning.argument_soundness",
  "name": "Argument Soundness Verifier",
  "description": "Evaluates whether arguments are logically sound",
  "version": "1.0.0",
  "input_schema": {
    "type": "object",
    "required": ["claims", "discourse_acts"],
    "properties": {
      "claims": {
        "type": "array",
        "description": "Claims forming the argument"
      },
      "discourse_acts": {
        "type": "array",
        "description": "Must include REASONING acts"
      }
    }
  },
  "output_schema": {
    "type": "object",
    "required": ["evaluation", "issues", "score", "reasoning"],
    "properties": {
      "evaluation": {
        "type": "object",
        "properties": {
          "premises_true": { "type": "boolean" },
          "logic_valid": { "type": "boolean" },
          "conclusion_supported": { "type": "boolean" }
        }
      },
      "issues": { "type": "array" },
      "score": { "type": "number", "minimum": 0, "maximum": 1 },
      "reasoning": { "type": "string" }
    }
  },
  "training_objective": "Evaluate argument soundness by checking premise truth and logical validity",
  "meta_verification": true,
  "metadata": {
    "author": "Superficial Labs",
    "created": "2025-12-01",
    "category": "reasoning"
  }
}
```

## Validation

Verifier Rubrics must validate against `schemas/verifier-rubric-v1.0.0.json`.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




