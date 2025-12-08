#!/usr/bin/env python3
"""
CAPE Validator

Validates CAPE artifacts against their JSON schemas.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Tuple, Optional

try:
    from jsonschema import validate, ValidationError, SchemaError
except ImportError:
    print("Error: jsonschema is required. Install with: pip install jsonschema")
    sys.exit(1)


# Base directory (repository root)
BASE = Path(__file__).parent.parent

# Schema mapping
SCHEMA_MAP = {
    "predicategraph": "predicate-graph-v1.0.0.json",
    "policy_pack": "policy-pack-v1.0.0.json",
    "cpl_policy": "cpl-policy-v1.0.0.json",
    "verifier_rubric": "verifier-rubric-v1.0.0.json",
}


def load_json(path: Path) -> dict:
    """Load a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_schema(kind: str) -> dict:
    """Load a schema by kind."""
    schema_file = SCHEMA_MAP.get(kind)
    if not schema_file:
        raise ValueError(f"Unknown kind: {kind}. Valid: {list(SCHEMA_MAP.keys())}")
    
    schema_path = BASE / "schemas" / schema_file
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema not found: {schema_path}")
    
    return load_json(schema_path)


def validate_file(path: Path, kind: str) -> Tuple[bool, str]:
    """
    Validate a file against its schema.
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Load the file
        data = load_json(path)
        
        # Load the schema
        schema = load_schema(kind)
        
        # Validate
        validate(instance=data, schema=schema)
        
        return True, "Valid"
        
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except ValidationError as e:
        # Get a cleaner error message
        path_str = " -> ".join(str(p) for p in e.absolute_path) if e.absolute_path else "root"
        return False, f"Validation error at {path_str}: {e.message}"
    except SchemaError as e:
        return False, f"Schema error: {e.message}"
    except FileNotFoundError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Error: {e}"


def validate_all() -> Tuple[int, int]:
    """
    Validate all artifacts in the repository.
    
    Returns:
        Tuple of (passed, failed) counts
    """
    passed = 0
    failed = 0
    
    # PredicateGraphs in examples
    print("\n[PredicateGraphs]")
    for example_dir in sorted(BASE.glob("examples/*/")):
        if not example_dir.is_dir():
            continue
        for path in sorted(example_dir.glob("*.json")):
            # Skip expectations files
            if path.name.endswith(".expectations.json"):
                continue
            
            rel = path.relative_to(BASE)
            success, msg = validate_file(path, "predicategraph")
            if success:
                print(f"  ✓ {rel}")
                passed += 1
            else:
                print(f"  ✗ {rel}")
                print(f"    {msg}")
                failed += 1
    
    # Policy Packs
    print("\n[Policy Packs]")
    for path in sorted(BASE.glob("packs/*.json")):
        rel = path.relative_to(BASE)
        success, msg = validate_file(path, "policy_pack")
        if success:
            print(f"  ✓ {rel}")
            passed += 1
        else:
            print(f"  ✗ {rel}")
            print(f"    {msg}")
            failed += 1
    
    # Verifier Rubrics
    print("\n[Verifier Rubrics]")
    for path in sorted(BASE.glob("rubrics/*.json")):
        rel = path.relative_to(BASE)
        success, msg = validate_file(path, "verifier_rubric")
        if success:
            print(f"  ✓ {rel}")
            passed += 1
        else:
            print(f"  ✗ {rel}")
            print(f"    {msg}")
            failed += 1
    
    return passed, failed


def main():
    parser = argparse.ArgumentParser(
        description="Validate CAPE artifacts against JSON schemas"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all artifacts in the repository"
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Path to a single file to validate"
    )
    parser.add_argument(
        "--kind",
        choices=list(SCHEMA_MAP.keys()),
        help="Kind of artifact (required with --file)"
    )
    parser.add_argument(
        "--version",
        help="Schema version to validate against (optional, uses default if not specified)"
    )
    
    args = parser.parse_args()
    
    if args.all:
        passed, failed = validate_all()
        print(f"\nSummary: {passed} passed, {failed} failed")
        sys.exit(0 if failed == 0 else 1)
    
    elif args.file:
        if not args.kind:
            print("Error: --kind is required when using --file")
            sys.exit(1)
        
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        
        success, msg = validate_file(args.file, args.kind)
        if success:
            print(f"✓ {args.file}: {msg}")
            sys.exit(0)
        else:
            print(f"✗ {args.file}: {msg}")
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()




