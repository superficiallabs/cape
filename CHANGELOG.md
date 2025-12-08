# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-01

### Added

- **PredicateGraph Specification v1.0.0**
  - Entity extraction and representation
  - Claim modeling with modality and domain
  - Tool call representation
  - Citation linking
  - Code block extraction
  - Discourse act annotation

- **CPL Specification v1.0.0**
  - Policy definition language
  - Quantifiers (forall, exists)
  - Predicates and conditions
  - Logical operators
  - Scope and binding rules

- **Policy Pack Specification v1.0.0**
  - Pack metadata and versioning
  - Policy collection format
  - Dependency declarations
  - Compatibility requirements

- **Learned Verifier Specification v1.0.0**
  - Rubric schema for semantic verification
  - Meta-verification specification
  - Integration with symbolic policies

- **Extraction Specification v1.0.0**
  - Extraction task definition
  - Quality metrics and error types
  - Node-type specific guidance

- **Correction Specification v1.0.0**
  - Three correction strategies: patch, insert, rewrite
  - Multi-violation handling
  - Re-verification requirements

- **Core Policy Packs**
  - `core.tool-use.v1` - Tool argument validation
  - `core.citation-grounding.v1` - Citation requirements
  - `core.safe-code.v1` - Code safety checks

- **Example Policy Pack**
  - `example.customer-support.v1` - Customer support quality

- **Example Rubrics**
  - `verifier.reasoning.argument_soundness`
  - `verifier.mathematics.proof_validity`
  - `verifier.agents.plan_feasibility`

- **Example PredicateGraphs**
  - Tool use violation example
  - Citation grounding violation example
  - Safe code violation example
  - Customer support violation example
  - Reasoning violation example

- **JSON Schemas**
  - PredicateGraph schema v1.0.0
  - CPL Policy schema v1.0.0
  - Policy Pack schema v1.0.0
  - Verifier Rubric schema v1.0.0

- **Validator**
  - Python-based schema validation
  - Support for all artifact types
  - Batch validation mode

- **Documentation**
  - Glossary of terms
  - Governance model
  - Compatibility matrix
  - Contributing guidelines
  - Code of conduct

## [Unreleased]

### Planned

- Additional core policy packs
- Extended verifier rubrics
- Multi-language validator support




