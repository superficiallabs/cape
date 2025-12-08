# Examples

This directory contains example PredicateGraphs and their expected policy evaluation outcomes.

## Structure

Each subdirectory contains:
- A PredicateGraph JSON file (e.g., `tip-calc-violation.json`)
- An expectations file (e.g., `tip-calc-violation.expectations.json`)

## Examples

### tool-use/

Examples of tool/function call scenarios.

| File | Description |
|------|-------------|
| `tip-calc-violation.json` | Tool call with incorrect argument type |
| `tip-calc-violation.expectations.json` | Expected policy violations |

### citation-grounding/

Examples of citation and factual grounding scenarios.

| File | Description |
|------|-------------|
| `factual-no-citation.json` | Factual claim without citation |
| `factual-no-citation.expectations.json` | Expected policy violations |

### safe-code/

Examples of code safety scenarios.

| File | Description |
|------|-------------|
| `python-unsafe.json` | Python code with unsafe patterns |
| `python-unsafe.expectations.json` | Expected policy violations |

### customer-support/

Examples of customer support interaction quality.

| File | Description |
|------|-------------|
| `no-acknowledgment.json` | Response missing customer acknowledgment |
| `no-acknowledgment.expectations.json` | Expected policy violations |

### reasoning/

Examples of reasoning and argument quality.

| File | Description |
|------|-------------|
| `argument-unsound.json` | Argument with false premise |
| `argument-unsound.expectations.json` | Expected verifier output |

## Using Examples

### Validation

```bash
# Validate all examples
python validator/validate.py --all

# Validate a specific example
python validator/validate.py --file examples/tool-use/tip-calc-violation.json --kind predicategraph
```

### Testing Policies

Use examples to test policy implementations:

1. Load the PredicateGraph
2. Run your policy implementation
3. Compare results with expectations file

## Creating New Examples

1. Create a PredicateGraph that demonstrates the scenario
2. Validate against the schema
3. Create an expectations file with expected outcomes
4. Add to appropriate subdirectory
5. Update this README

### Expectations File Format

```json
{
  "description": "Brief description of what this example tests",
  "packs": ["pack-ids-to-test"],
  "expected_violations": [
    {
      "policy_id": "policy-id",
      "rule_id": "rule-id",
      "node_id": "violating-node-id",
      "message": "Expected violation message"
    }
  ],
  "notes": "Additional context or explanation"
}
```

For learned verifier examples:

```json
{
  "description": "Brief description",
  "packs": [],
  "verifiers": ["verifier.category.name"],
  "expected_verifier_output": {
    "verifier_id": "verifier.category.name",
    "issues": [...],
    "score": 0.0,
    "reasoning": "Expected reasoning"
  },
  "notes": "Additional context"
}
```




