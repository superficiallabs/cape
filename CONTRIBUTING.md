# Contributing to CAPE

Thank you for your interest in contributing to CAPE! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Types of Contributions](#types-of-contributions)
- [Development Setup](#development-setup)
- [Submission Guidelines](#submission-guidelines)
- [Style Guide](#style-guide)
- [Review Process](#review-process)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use issue templates when available
- Provide clear reproduction steps for bugs
- Include relevant version information

### Suggesting Enhancements

- Open an issue with the `enhancement` label
- Describe the use case and expected behavior
- Consider backward compatibility implications

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Run validation (`python validator/validate.py --all`)
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

## Types of Contributions

### Specification Changes

Changes to files in `specs/` require:
- Clear rationale in the PR description
- Consideration of backward compatibility
- Updates to relevant schemas
- Updates to the compatibility matrix

### Schema Changes

Changes to files in `schemas/` require:
- Corresponding specification updates
- Version bump consideration
- Migration path documentation
- Updated examples

### Policy Pack Contributions

New or modified policy packs require:
- Complete policy definitions
- Example PredicateGraphs
- Expected outcomes documentation
- Passing validation

### Example Contributions

New examples require:
- Valid PredicateGraph JSON
- Corresponding expectations file
- Clear documentation of the scenario

## Development Setup

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cape.git
cd cape

# Install dependencies
pip install -r validator/requirements.txt

# Verify setup
python validator/validate.py --all
```

## Submission Guidelines

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `spec`: Specification change
- `schema`: Schema change
- `example`: Example addition/modification
- `chore`: Maintenance

### Pull Request Checklist

- [ ] All validation passes
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Backward compatibility considered
- [ ] Tests added (if applicable)

## Style Guide

### Markdown

- Use ATX-style headers (`#`)
- One sentence per line for easier diffs
- Use fenced code blocks with language hints

### JSON

- 2-space indentation
- No trailing commas
- Sorted keys where logical
- Descriptive key names

### Naming Conventions

- Policy packs: `<scope>.<capability>.v<version>.json`
- Schemas: `<type>-v<version>.json`
- Examples: `<descriptive-name>.json`

## Review Process

1. **Automated Checks**: All PRs run validation automatically
2. **Maintainer Review**: At least one maintainer must approve
3. **Specification Review**: Spec changes require additional review
4. **Merge**: Squash and merge for clean history

### Review Timeline

- Initial response: Within 3 business days
- Full review: Within 1 week
- Complex changes may require longer discussion

## Questions?

- Open a discussion in GitHub Discussions
- Email: research@superficiallabs.com

Thank you for contributing to CAPE!




