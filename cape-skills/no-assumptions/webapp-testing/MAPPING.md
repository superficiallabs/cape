# Mapping: webapp-testing

> **Source:** [anthropics/skills/webapp-testing](https://github.com/anthropics/skills/tree/main/webapp-testing)
>
> **Policy:** [policy.cpl](./policy.cpl)
>
> **Category:** No assumptions needed
>
> **Framework:** [Playwright](https://playwright.dev/)

---

## Constraint Mapping

| # | SKILL.md Guidance | Tier | Predicate | Type |
|---|-------------------|------|-----------|------|
| 1 | Valid test code | T1 | `syntax_valid(code) == true` | Direct |
| 2 | Valid test code | T1 | `parse_error_count(code) == 0` | Direct |
| 3 | "run Playwright tests" | T1 | `test_count(code) > 0` | Direct |
| 4 | "verify functionality" | T1 | `tests_without_assertions_count(code) == 0` | Direct |
| 5 | Playwright API | T1 | `invalid_playwright_method_count(code) == 0` | Direct |
| 6 | Playwright API | T1 | `deprecated_playwright_method_count(code) == 0` | Direct |
| 7 | Async correctness | T1 | `unawaited_async_count(code) == 0` | Direct |
| 8 | Best practices | T3 | `generic_test_name_count(code) == 0` | Proxy |
| 9 | Best practices | T3 | `tests_exceeding_length_count(code) == 0` | Proxy |
| 10 | Best practices | T3 | `hardcoded_wait_count(code) == 0` | Direct |

---

## Verification Approach

All predicates use **static code analysis**. No test execution required.

| Analysis Type | Predicates |
|---------------|------------|
| Parsing | Syntax validity, parse errors |
| AST analysis | Test count, assertions, async/await |
| API validation | Playwright methods |
| Pattern matching | Test names, hardcoded waits |
| Metrics | Test length |

**What this verifies:** The model produces well-formed, correct Playwright test code.

**What this doesn't verify:** Whether tests pass when run. That depends on the application under test, not the model's capability.

---

## Tier Rationale

| Tier | Predicates | Why this tier |
|------|------------|---------------|
| **T1** | Syntax, tests exist, assertions, API, async | Invalid code won't run |
| **T3** | Names, length, hardcoded waits | Best practices / maintainability |

---

## Playwright Test Structure

A valid Playwright test file includes:

```typescript
import { test, expect } from '@playwright/test';

test('descriptive name', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle('Example');
});
```

| Requirement | What it catches |
|-------------|-----------------|
| Valid syntax | Parse errors |
| Has test() | Empty file |
| Has expect() | Tests without verification |
| Proper await | Race conditions |
| Valid API | Typos, deprecated methods |

---

## Common Anti-Patterns Detected

| Anti-pattern | Predicate | Why it's bad |
|--------------|-----------|--------------|
| No assertions | `tests_without_assertions_count` | Test always passes |
| Missing await | `unawaited_async_count` | Race conditions, flaky tests |
| Hardcoded waits | `hardcoded_wait_count` | Slow, flaky tests |
| Generic names | `generic_test_name_count` | Hard to understand failures |
| Long tests | `tests_exceeding_length_count` | Hard to maintain |

---

## Coverage Summary

| Category | Count | Status |
|----------|------:|--------|
| T1 (Correctness) | 7 | Static analysis |
| T2 (Governance) | 0 | Not applicable |
| T3 (Quality) | 3 | Static analysis |
| **Total** | **10** | — |
