# CAPE Validator

A Python-based validation tool for CAPE artifacts.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Validate All Artifacts

```bash
python validate.py --all
```

This validates:
- All PredicateGraphs in `examples/`
- All Policy Packs in `packs/`
- All Verifier Rubrics in `rubrics/`

### Validate Single File

```bash
python validate.py --file <path> --kind <type>
```

Types:
- `predicategraph` - PredicateGraph JSON files
- `policy_pack` - Policy Pack JSON files
- `cpl_policy` - Standalone CPL Policy files
- `verifier_rubric` - Verifier Rubric JSON files

### Examples

All commands assume you're running from the repository root directory.

```bash
# Validate a PredicateGraph
python validator/validate.py --file examples/tool-use/tip-calc-violation.json --kind predicategraph

# Validate a Policy Pack
python validator/validate.py --file packs/core.tool-use.v1.json --kind policy_pack

# Validate a Verifier Rubric
python validator/validate.py --file rubrics/reasoning.argument-soundness.v1.json --kind verifier_rubric
```

Alternatively, if running from the `validator/` directory:

```bash
cd validator
python validate.py --file ../examples/tool-use/tip-calc-violation.json --kind predicategraph
```

## Exit Codes

- `0` - All validations passed
- `1` - One or more validations failed

## Output

The validator outputs:
- ✓ for passed validations
- ✗ for failed validations with error details

### Example Output

```
[PredicateGraphs]
  ✓ examples/tool-use/tip-calc-violation.json
  ✓ examples/citation-grounding/factual-no-citation.json
  ✓ examples/safe-code/python-unsafe.json

[Policy Packs]
  ✓ packs/core.tool-use.v1.json
  ✓ packs/core.citation-grounding.v1.json
  ✓ packs/core.safe-code.v1.json

[Verifier Rubrics]
  ✓ rubrics/reasoning.argument-soundness.v1.json
  ✓ rubrics/mathematics.proof-validity.v1.json
  ✓ rubrics/agents.plan-feasibility.v1.json

Summary: 9 passed, 0 failed
```

## Development

### Adding New Schema Versions

1. Add schema file to `schemas/`
2. Update `schema_map` in `validate.py`

### Extending Validation

The validator uses JSON Schema validation via `jsonschema`. To add custom validation logic, extend the `validate_file()` function.




