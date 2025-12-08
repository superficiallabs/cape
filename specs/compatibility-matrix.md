# Compatibility Matrix

**Version**: 1.0.0

## Overview

This document tracks compatibility between CAPE specification versions and provides guidance for upgrades.

## Current Versions

| Component | Version | Status |
|-----------|---------|--------|
| PredicateGraph Schema | 1.0.0 | Stable |
| CPL Policy Schema | 1.0.0 | Stable |
| Policy Pack Schema | 1.0.0 | Stable |
| Verifier Rubric Schema | 1.0.0 | Stable |

## Schema Compatibility

### PredicateGraph

| Schema Version | Compatible Extractors | Notes |
|----------------|----------------------|-------|
| 1.0.0 | ≥1.0.0 | Initial release |

### CPL Policy

| Schema Version | Compatible Runtimes | Notes |
|----------------|---------------------|-------|
| 1.0.0 | ≥1.0.0 | Initial release |

### Policy Pack

| Schema Version | Compatible Loaders | Notes |
|----------------|-------------------|-------|
| 1.0.0 | ≥1.0.0 | Initial release |

### Verifier Rubric

| Schema Version | Compatible Verifiers | Notes |
|----------------|---------------------|-------|
| 1.0.0 | ≥1.0.0 | Initial release |

## Cross-Component Compatibility

| PredicateGraph | CPL Policy | Policy Pack | Rubric | Compatible |
|----------------|------------|-------------|--------|------------|
| 1.0.0 | 1.0.0 | 1.0.0 | 1.0.0 | ✓ |

## Migration Guides

### Future Migrations

Migration guides will be added here when new versions are released.

## Deprecation Schedule

No deprecations in v1.0.0.

### Planned Deprecations

| Component | Feature | Deprecated In | Removed In | Migration |
|-----------|---------|---------------|------------|-----------|
| - | - | - | - | - |

## Backward Compatibility

### Guarantees

Within a major version:
- New optional fields may be added
- New node types may be added
- New predicates may be added
- Existing fields will not change type
- Existing required fields will not be removed

### Non-Guarantees

Between major versions:
- Fields may be removed
- Types may change
- Semantics may change

## Version Detection

### Schema Version Field

All CAPE artifacts include a `schema_version` field:

```json
{
  "schema_version": "1.0.0",
  ...
}
```

Consumers should:
1. Check `schema_version` before processing
2. Reject unknown major versions
3. Warn on unknown minor versions
4. Ignore unknown patch versions

### Version Parsing

Version strings follow semver:
- Format: `MAJOR.MINOR.PATCH`
- Compare: Major → Minor → Patch
- Pre-release: Not used in stable releases

## Upgrade Recommendations

### From Pre-1.0 (if applicable)

Not applicable - v1.0.0 is the initial release.

### Future Upgrades

Upgrade guides will be provided with each release.

## Testing Compatibility

### Validator Support

The validator supports checking compatibility:

```bash
# Check if file is compatible with version
python validator/validate.py --file graph.json --version 1.0.0
```

### Test Suites

Compatibility test suites are provided for each version in `examples/`.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




