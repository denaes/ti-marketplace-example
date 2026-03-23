---
name: e2e-playwright
description: Plan and implement E2E tests with Playwright (Page Object Model, fixtures, coverage)
metadata:
  type: skill
  department: engineering
  source: ti-rd-playbook
  version: "1.0"
---
# E2E Playwright Skill

## 1. Purpose

Guide engineers to **plan and implement end-to-end tests** using Playwright (or the project's chosen E2E framework) so that critical user flows are automated and aligned with epic test plans and acceptance criteria.

## 2. When This Skill Is Used

- Implementing a [QA] story or an epic's E2E test suite.
- Adding or updating E2E tests for a feature that has UI or API flows.
- When the story's Cursor prompt or test plan references Playwright, E2E, or "test scenarios".

## 3. Relationship to QA Test Planner

The **tech lead** skill `skills/engineering-management/qa_test_planner/SKILL.md` defines how [QA] stories and test plans are structured (test scenarios by functional area, coverage matrix, TS-XXX IDs). When implementing the **tests**, follow that plan and use this skill for structure and patterns.

## 4. Test Structure and Organization

- **By functional area:** Group tests by feature/area (e.g. "Conversational Search", "Feature flag gating"), not only by story number. This keeps suites readable and stable when stories are split or merged.
- **Scenario format:** Each scenario should have clear preconditions, steps, and expected results; map back to story ACs for traceability (e.g. "TS-AUTH-001 covers TI-3516 AC: 403 when flag off").
- **Independence:** Tests must be runnable in any order; use fresh state (e.g. clean DB or fixtures) in `beforeEach` or test fixtures so one test does not depend on another.

## 5. Playwright Patterns

- **Page Object Model (POM):** Encapsulate page or flow interactions in page objects (e.g. `ConversationalSearchPage`, `LoginPage`) so tests stay short and changes to the UI are localized.
- **Fixtures:** Use Playwright fixtures (or project-specific) for auth, base URL, and test data so tests do not repeat setup.
- **Assertions:** Use `expect()` with descriptive messages; assert visible state, not implementation details.
- **Selectors:** Prefer stable selectors (data-testid, role, label); avoid fragile CSS that breaks when styling changes.
- **Config:** Respect `playwright.config.ts` (or equivalent) for base URL, timeouts, and browsers; document any env vars (e.g. auth credentials) in a README or `.env.sample`, not in code.

## 6. What to Cover

- **Happy path:** Main user flows that match the epic's acceptance criteria.
- **Negative:** Invalid input, unauthorized access, feature off (e.g. 403 when flag disabled).
- **Edge cases:** Empty state, timeouts, concurrent actions if relevant.
- **Regression:** Existing critical flows that must not break (smoke tests).

Ensure the **coverage matrix** from the [QA] story is satisfied: every AC has at least one E2E (or unit) scenario that verifies it.

## 7. Test Data and Environment

- **No hard-coded secrets:** Use environment variables or fixture files that are gitignored or in a secure store.
- **Data setup:** Prefer factories or API calls to create test data; avoid depending on production or shared DB state.
- **Cleanup:** Where possible, clean up created data after the test or in `afterEach` to avoid polluting the next run.

## 8. Running E2E Tests

- **Local:** `npx playwright test` (or project script, e.g. `npm run e2e`) from the app or test root.
- **CI:** E2E typically runs in pipeline with a dedicated env (staging or test); document in `skills/engineering/automation-ci/SKILL.md` if different.
- **Debug:** Use `npx playwright test --debug` or headed mode when diagnosing failures; avoid committing long timeouts or debug-only code.

## 9. Do Not

- Do not skip negative or security scenarios that are in the test plan.
- Do not hard-code user credentials or API keys; use config or env.
- Do not write tests that depend on execution order or shared mutable state.
- Do not ignore flaky tests; fix or quarantine with a ticket to fix.

## 10. Cross-References

- Use Jira ticket IDs (e.g. TI-3516) in test descriptions or coverage comments; see `standards/conventions.md`.
- Map test scenarios back to the [QA] story's test plan IDs (e.g. TS-XXX-001) when the plan uses them.
