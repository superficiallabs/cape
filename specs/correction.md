# Correction Specification

**Version**: 1.0.0
**Status**: Stable

## Overview

The Correction Engine transforms AI outputs that violate policies into compliant versions. This specification defines correction strategies, multi-violation handling, and re-verification requirements.

## Correction Pipeline

```
┌─────────────────┐     ┌─────────────┐     ┌─────────────────┐
│ PredicateGraph  │────>│  Evaluator  │────>│   Violations    │
└─────────────────┘     └─────────────┘     └─────────────────┘
                                                    │
┌─────────────────┐     ┌─────────────┐             │
│ Corrected Graph │<────│  Corrector  │<────────────┘
└─────────────────┘     └─────────────┘
```

## Correction Strategies

### 1. Patch

Minimal, targeted fixes to specific violations.

**When to use:**
- Single, isolated violations
- Clear fix location
- Minimal collateral impact

**Process:**
1. Identify violation location
2. Generate minimal fix
3. Apply to original text
4. Re-extract affected nodes

**Example:**

Violation: Tool argument has wrong type
```json
// Original
{ "amount": "100" }

// Patched
{ "amount": 100 }
```

### 2. Insert

Add missing elements without modifying existing content.

**When to use:**
- Missing required elements
- Incomplete outputs
- Missing citations or context

**Process:**
1. Identify what's missing
2. Generate addition
3. Determine insertion point
4. Insert without disrupting existing

**Example:**

Violation: Factual claim missing citation
```
// Original
"Python was created in 1991."

// With insertion
"Python was created in 1991 [1].

[1] https://python.org/history"
```

### 3. Rewrite

Complete regeneration of a section.

**When to use:**
- Multiple interrelated violations
- Structural problems
- Semantic issues requiring rethinking

**Process:**
1. Identify problematic section
2. Extract constraints and requirements
3. Regenerate section
4. Integrate with unchanged parts

**Example:**

Violation: Reasoning is unsound
```
// Original (unsound)
"All birds can fly. Penguins are birds. Therefore, penguins can fly."

// Rewritten
"Most birds can fly, but there are exceptions. Penguins are birds that 
have evolved for swimming rather than flying. Their wings have adapted 
into flippers, making them excellent swimmers but unable to fly."
```

## Strategy Selection

```
┌─────────────────────────────────────────────────────┐
│                  Violation Analysis                  │
├──────────────────┬──────────────────────────────────┤
│   Violation      │           Strategy               │
│   Count          │                                  │
├──────────────────┼──────────────────────────────────┤
│   1, isolated    │   Patch                          │
│   1, missing     │   Insert                         │
│   1, semantic    │   Rewrite (local)                │
│   Multiple,      │   Sequential Patch/Insert        │
│   independent    │                                  │
│   Multiple,      │   Rewrite (section)              │
│   related        │                                  │
│   Many,          │   Rewrite (full)                 │
│   systemic       │                                  │
└──────────────────┴──────────────────────────────────┘
```

## Multi-Violation Handling

### Independent Violations

Apply fixes in order of severity, then location:

1. Sort by severity (fatal > major > minor)
2. Within severity, sort by location (start to end)
3. Apply fixes sequentially
4. Adjust spans after each fix

### Dependent Violations

When fixing one affects another:

1. Identify dependency graph
2. Find root causes
3. Fix root causes first
4. Re-evaluate dependent violations

### Conflicting Violations

When fixes would contradict:

1. Identify conflict
2. Prioritize by policy precedence
3. Apply higher-priority fix
4. Document trade-off

## Correction Output

```json
{
  "original_text": "...",
  "corrected_text": "...",
  "corrections": [
    {
      "violation_id": "v1",
      "strategy": "patch",
      "location": { "start": 50, "end": 55 },
      "original": "\"100\"",
      "replacement": "100",
      "explanation": "Changed string to number"
    }
  ],
  "residual_violations": [],
  "verification_status": "passed"
}
```

### Correction Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `violation_id` | string | Yes | Which violation this fixes |
| `strategy` | string | Yes | patch, insert, or rewrite |
| `location` | object | Yes | Where the change occurs |
| `original` | string | Yes | Original content |
| `replacement` | string | Yes | New content |
| `explanation` | string | Yes | Why this fix |

## Re-Verification

After correction:

1. **Re-extract**: Generate new PredicateGraph
2. **Re-evaluate**: Run all policies
3. **Iterate**: If new violations, correct again
4. **Limit**: Max iterations to prevent loops

### Iteration Limits

| Scenario | Max Iterations |
|----------|----------------|
| Patch corrections | 3 |
| Insert corrections | 3 |
| Rewrite corrections | 2 |
| Mixed | 5 |

### Termination Conditions

- All policies pass
- Max iterations reached
- No progress (same violations)
- Conflict detected

## Quality Criteria

### Minimal Change Principle

Corrections should:
- Preserve original meaning where possible
- Change only what's necessary
- Maintain style and tone
- Not introduce new issues

### Coherence

Corrected output should:
- Read naturally
- Be internally consistent
- Flow logically
- Not have obvious patches

### Completeness

All violations should be:
- Addressed
- Or documented as unresolvable
- With clear reasoning

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-01 | Initial release |




