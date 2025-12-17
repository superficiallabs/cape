# Assumptions: webapp-testing

> **Source:** [anthropics/skills/webapp-testing](https://github.com/anthropics/skills/tree/main/webapp-testing)
>
> **Policy:** [policy.cpl](./policy.cpl) | **Mapping:** [MAPPING.md](./MAPPING.md)
>
> **Category:** No assumptions needed
>
> **Framework:** [Playwright](https://playwright.dev/)

---

## No Assumptions Required

This skill falls into the **"No Assumptions Needed"** category. All requirements are derived from:
- TypeScript/JavaScript syntax rules
- Playwright API specification
- Testing best practices with objective definitions

### What This Policy Verifies

The **capability** being trained is: "Write good Playwright tests."

| Model output | Policy verifies |
|--------------|-----------------|
| Test code (.spec.ts) | Code is well-formed and follows best practices |

We verify the **test code quality**, not whether tests pass. Whether tests pass depends on the application under test—that's outside the model's control.

---

## Verification Approach

All predicates use **static code analysis**. No test execution required.

| Analysis Type | Predicates |
|---------------|------------|
| Parsing | Syntax validity |
| AST analysis | Test definitions, assertions, async/await |
| API validation | Playwright method names |
| Pattern matching | Test names, hardcoded waits |

---

## Why No Assumptions?

**1. Syntax is Binary**

TypeScript/JavaScript either parses or it doesn't. There's no "partially valid" syntax.

**2. Playwright API is Documented**

The Playwright API has a fixed set of methods. `page.clickk()` is wrong; `page.click()` is right. No subjective judgment.

**3. Assertions are Required**

A test without assertions always passes—it verifies nothing. This is objectively a bug, not a style preference.

**4. Async/Await is Required**

Playwright methods are async. Missing `await` causes race conditions. This is a correctness issue.

---

## What This Policy Verifies

### T1: Objective Correctness

| Check | What it catches |
|-------|-----------------|
| Valid syntax | Parse errors, typos |
| Tests exist | Empty files |
| Assertions present | Tests that verify nothing |
| Valid Playwright API | Wrong method names |
| Proper async/await | Race conditions |

### T3: Best Practices

| Check | What it catches |
|-------|-----------------|
| Descriptive names | `test('test1', ...)` |
| Reasonable length | 200-line tests |
| No hardcoded waits | `page.waitForTimeout(5000)` |

---

## Why T3 for Best Practices?

Best practices are T3 (quality), not T1 (correctness), because:

**Descriptive names:** A test named `test1` still runs. Bad names hurt maintainability, not functionality.

**Test length:** Long tests work. They're just harder to understand.

**Hardcoded waits:** `waitForTimeout(5000)` works. It's just slow and flaky compared to proper conditions.

These are quality issues, not correctness issues.

---

## Common Patterns

### Good Test
```typescript
test('should display error message when login fails', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#username', 'invalid');
  await page.fill('#password', 'wrong');
  await page.click('button[type="submit"]');
  await expect(page.locator('.error')).toBeVisible();
});
```

### Bad Test (Caught by Policy)
```typescript
test('test1', async ({ page }) => {  // T3: generic name
  page.goto('/login');  // T1: missing await
  page.fill('#username', 'invalid');  // T1: missing await
  await page.waitForTimeout(5000);  // T3: hardcoded wait
  // T1: no assertions!
});
```

---

## Configuration Reference

```json
{
  "configuration": {
    "min_assertions_per_test": 1,
    "require_descriptive_names": true,
    "max_test_length_lines": 50
  }
}
```

---

## Summary Table

| Constraint | Source | Predicate | Tier |
|------------|--------|-----------|------|
| Valid syntax | TypeScript | `syntax_valid()` | **T1** |
| Tests exist | Testing basics | `test_count() > 0` | **T1** |
| Has assertions | Testing basics | `tests_without_assertions_count() == 0` | **T1** |
| Valid API | Playwright docs | `invalid_playwright_method_count() == 0` | **T1** |
| Proper await | Async/await | `unawaited_async_count() == 0` | **T1** |
| Descriptive names | Best practice | `generic_test_name_count() == 0` | **T3** |
| Reasonable length | Best practice | `tests_exceeding_length_count() == 0` | **T3** |
| No hardcoded waits | Best practice | `hardcoded_wait_count() == 0` | **T3** |
