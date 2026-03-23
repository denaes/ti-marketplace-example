---
name: qa-test-planner
description: Generate comprehensive Playwright test plans for an epic, covering all stories and their acceptance criteria
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# QA Test Planner Skill

## 1. Objective

Act as an expert web test planner with extensive experience in quality assurance, user experience testing, and test scenario design. Your expertise includes functional testing, edge case identification, and comprehensive test coverage planning.

## 2. When This Skill Is Used

This skill is invoked when generating a **[QA] story** during epic decomposition. The [QA] story is the **centralized test plan for the entire epic** — it must reference and cover all other stories in the epic, not just its own scope.

## 3. Input Requirements

Before generating the test plan, you must have:

1. **All story files in the epic** — read every story to extract:
   - Acceptance criteria (these become test assertions)
   - Technical implementation details (these inform test setup)
   - Dependencies between stories (these determine test ordering)
   - Edge cases mentioned in any story
   - Error states and failure modes

2. **The PRD** — for additional context on user journeys, personas, and system behavior

3. **Codebase patterns** — existing test framework, test utilities, E2E tools

## 4. Test Plan Structure

The [QA] story must produce a test plan with the following structure:

### 4.1 Test Suite Organization

Organize test scenarios by **functional area** (not by story number), so the test plan reads as a coherent verification of the feature, not a checklist of story ACs:

```markdown
## Test Suite: [Epic Name]

### Area 1: [Functional Area] (covers Stories X, Y, Z)
### Area 2: [Functional Area] (covers Stories A, B)
...
```

### 4.2 Test Scenario Format

Each scenario must include:

| Field | Description |
|-------|-------------|
| **ID** | `TS-{area}-{number}` (e.g., `TS-AUTH-001`) |
| **Title** | Clear, descriptive title |
| **Covers** | Which story/stories and AC(s) this scenario verifies |
| **Type** | `Happy Path` / `Negative` / `Edge Case` / `Security` / `Performance` |
| **Preconditions** | Starting state assumptions (always assume blank/fresh state unless stated) |
| **Steps** | Numbered step-by-step instructions, specific enough for any tester |
| **Expected Result** | What should happen (assertions) |
| **Failure Criteria** | What constitutes a failure |

### 4.3 Required Test Categories

Every test plan must include scenarios from these categories:

1. **Happy Path** — Primary user flows work as specified
2. **Negative Testing** — Invalid inputs, unauthorized access, missing data
3. **Edge Cases** — Boundary conditions, concurrent operations, empty states
4. **Security** — Permission boundaries, data leaks, injection vectors
5. **Integration** — Cross-story interactions, dependency chains
6. **Regression** — Existing functionality that must not break

### 4.4 Coverage Matrix

The test plan must include a coverage matrix showing which stories and ACs are verified by which test scenarios:

```markdown
| Story | AC | Test Scenario(s) | Coverage |
|-------|----|--------------------|----------|
| Story 3 | Feature flag ON → UI visible | TS-FF-001, TS-FF-002 | ✅ |
| Story 5 | Private content never in results | TS-SEC-001, TS-SEC-003 | ✅ |
| Story 5 | Eligible content indexed <5min | TS-PERF-001 | ✅ |
```

## 5. Quality Standards

- **Independence:** Scenarios must be independent and runnable in any order
- **Specificity:** Steps must be specific enough for any tester to follow without asking questions
- **Completeness:** Every acceptance criterion across ALL stories must have at least one test scenario
- **Negative coverage:** For every "must do X" AC, include a "must NOT do Y" test
- **Traceability:** Every scenario must link back to the story/AC it verifies
- **Cross-references:** See `standards/conventions.md` for cross-referencing rules. Use Jira ticket IDs when they exist, story titles when they don't. Never use local file names or story numbers.

## 6. Cursor Prompt Generation for [QA] Stories

When generating the Cursor Prompt for a [QA] story, use this template:

```
Role: Senior QA Engineer / Playwright Test Author

Task: Implement the E2E test suite for the [Epic Name] epic.

YOU ARE TESTING THE FOLLOWING STORIES:
[For each story in the epic, list:]
- Story N: [Title] — Key ACs: [list acceptance criteria]
  - Files: [list implementation files from the story's Cursor Prompt]

TEST PLAN REFERENCE:
[Include the full test plan from the story's "Test Scenarios" section]

CODEBASE CONTEXT:
1. Test framework: [e.g., Playwright, Jest, Vitest]
2. Test utilities: [existing test helpers, factories, fixtures]
3. Test configuration: [playwright.config.ts location, base URLs, auth setup]

WHAT TO IMPLEMENT:
[List each test scenario from the plan as a Part]

Part 1 — [Functional Area]: [scenarios TS-XXX-001 through TS-XXX-00N]
Part 2 — [Functional Area]: [scenarios TS-YYY-001 through TS-YYY-00N]
...

PLAYWRIGHT PATTERNS:
- Use Page Object Model for reusable page interactions
- Use test fixtures for authentication and data setup
- Use expect() assertions with descriptive messages
- Group related tests in describe() blocks by functional area
- Use test.beforeEach() for fresh state setup

DO NOT:
- Skip negative test scenarios
- Hard-code test data (use factories/fixtures)
- Write tests that depend on execution order
- Skip the coverage matrix verification

TESTING:
- All scenarios pass on a fresh database
- Coverage matrix shows 100% AC coverage
- No test depends on another test's side effects
```
