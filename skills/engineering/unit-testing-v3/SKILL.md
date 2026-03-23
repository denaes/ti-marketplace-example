---
name: unit-testing-v3
description: Write and run unit tests for the V3 NestJS codebase (Jest, Sinon, patterns)
metadata:
  type: skill
  department: engineering
  source: ti-rd-playbook
  version: "1.0"
---
# Unit Testing (V3) Skill

## 1. Purpose

Define how to **write and run unit tests** for the TI V3 NestJS application so that new and changed code is covered consistently and tests remain maintainable.

## 2. When This Skill Is Used

- Implementing a [BE], [FE] (if unit-tested), or other story that requires unit tests.
- Adding tests for a new controller, service, or adapter in `ti/v3/`.
- Reviewing or refactoring existing tests under `ti/v3/test/`.

## 3. Test Stack (V3)

- **Runner / framework:** Jest (NestJS default).
- **Location:** `ti/v3/test/` — structure mirrors `ti/v3/src/` (e.g. `src/modules/chat/chat.service.ts` → `test/modules/chat/chat.service.spec.ts`).
- **Mocking:** Sinon (stubs, mocks, createStubInstance) is used widely in V3 tests (see examples below).
- **Assertions:** Node `assert` or Jest `expect`; prefer one style per file.

## 4. File and Naming Conventions

- **Spec files:** `*.spec.ts` next to or under `test/` with the same relative path as source.
- **Describe block:** Use the class or module name (e.g. `describe('ChatService', function () { ... })`).
- **Imports:** Prefer relative paths from the spec file to the source (e.g. `../../src/modules/chat/chat.service`).

## 5. Patterns (from ti/v3)

- **Service with dependencies:** Stub dependencies with Sinon; inject stubs into the service under test.
  - Example: `chat.service.spec.ts` — stubs for `IAIAdapter`, `VectorSearchService`, `ContentAccessResolver`; `beforeEach` creates stubs and instantiates `ChatService`.
- **Controllers:** Test HTTP layer with mocked service (e.g. `createStubInstance(SomeService)`); assert status codes, response shape, and that service methods were called with expected args.
- **Guards and decorators:** Unit test the guard logic in isolation with fake request/context; use Sinon for dependencies.
- **Async:** Use `async/await` in tests; ensure `beforeEach`/`afterEach` clean up (e.g. `sinon.restore()`).

## 6. What to Test

- **Happy path:** Expected inputs → expected outputs and side effects.
- **Error paths:** Invalid input, missing auth, adapter throwing → correct exception or status (e.g. 403, 500).
- **Boundaries:** Empty lists, null/undefined where the contract allows.
- **Integration with ports:** When testing a service that uses an adapter (hexagonal), stub the adapter; do not hit real DB or external APIs in unit tests.

## 7. Running Tests

- From repo root: `cd ti/v3 && npm test` (or `npx jest`).
- Single file: `npx jest ti/v3/test/modules/chat/chat.service.spec.ts`.
- Watch mode: `npm test -- --watch` when iterating.

## 8. Do Not

- Do not use real external services or DB in unit tests; use stubs/mocks.
- Do not skip tests without a tracked reason (e.g. ticket to fix flake).
- Do not commit `@ts-ignore` or disabled tests unless there is a follow-up ticket; prefer fixing the test or the code.
- Do not duplicate large blocks of production code in tests; use factories or small helpers where it improves readability.

## 9. Relation to Other Skills

- **Cursor prompt:** The story's Cursor prompt often has a "TESTING" section; align test cases with that and with the story's acceptance criteria.
- **E2E:** For full flows use E2E (Playwright) per `skills/engineering/e2e-playwright/SKILL.md`; unit tests focus on a single class or module in isolation.
