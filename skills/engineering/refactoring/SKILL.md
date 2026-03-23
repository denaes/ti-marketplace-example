---
name: refactoring
description: Refactor code safely (scope, tests, small steps, rollback)
metadata:
  type: skill
  department: engineering
  source: claude-skills
  version: "1.0"
---
# Refactoring Skill

## 1. Purpose

Guide **safe refactoring** of existing code so behavior is preserved, tests protect against regressions, and changes stay reviewable and easy to roll back.

## 2. When This Skill Is Used

- The user asks to "refactor X", "clean up this module", or "extract this into a separate function/class".
- Reducing duplication, improving readability, or aligning code with current architecture (e.g. hexagonal patterns in V3) without changing behavior.
- Preparing code for a new feature (e.g. extract interface, then add new implementation).

## 3. Principles

- **Behavior first:** Refactoring does not change observable behavior. No new features and no bug "fixes" in the same commit unless the ticket explicitly includes both; separate refactor from feature/fix when possible.
- **Tests as a safety net:** Ensure existing tests pass before and after. Add or update tests if the current coverage is insufficient to detect regressions.
- **Small steps:** Prefer a sequence of small, reviewable commits over one large refactor. Each step should leave the codebase in a working state.
- **Rollback-friendly:** Avoid renaming and logic changes in the same commit; avoid touching many files at once unless the change is mechanical (e.g. project-wide rename with a tool).

## 4. Before Refactoring

1. **Scope:** Identify the exact files and boundaries (e.g. "this service", "this controller"). Do not expand scope mid-refactor.
2. **Run tests:** Full test suite (or at least the affected area) must be green. Fix any existing failures first.
3. **Ticket:** If the refactor is part of a story, ensure the ticket (e.g. TI-XXXX) describes the goal; if it's ad hoc, consider a short note in the commit or a small ticket for traceability.
4. **Dependencies:** Understand callers and callees so you do not break other modules; use "find references" and tests to confirm.

## 5. Common Refactors in V3

- **Extract adapter (hexagonal):** Introduce an interface and DI token; move implementation to an adapter class; inject the adapter in the consumer. Keep the same public behavior; tests should still pass with a stub or the same implementation.
- **Extract method/function:** Move a block of code into a named function in the same file (or a shared helper); replace the block with a call. Improves readability and testability.
- **Rename for clarity:** Rename symbols and update all references; run tests and lint. Use IDE refactor tools to avoid missing references.
- **Reorganize files:** Move a class or module to a new path; update imports and barrel exports; run tests and fix any path or circular dependency issues.
- **Replace implementation:** When swapping one implementation for another (e.g. new library), keep the same interface or adapter contract; compare behavior with tests or a short manual check list.

## 6. After Refactoring

- [ ] All existing tests pass.
- [ ] No new linter or type errors.
- [ ] Commit message describes *what* was refactored and *why* (and ticket if applicable).
- [ ] If the change is large, consider a short note in the PR or in `ti/v3/docs/` so future readers know the new structure.

## 7. Do Not

- Do not refactor and add new behavior in the same commit without explicit approval; it makes review and rollback harder.
- Do not remove or skip tests "because we refactored"; fix or update tests instead.
- Do not change public APIs or contracts without a ticket and callers’ awareness; treat that as a separate change.
- Do not rely on "it still works" without running the test suite; automated tests are the safety net.

## 8. Relation to Other Skills

- **Codebase navigation:** Know where the code lives and who uses it before refactoring.
- **Unit testing:** Tests define "same behavior"; keep them green and add more if coverage is weak.
- **Code review:** Refactor PRs should be reviewed with the same checklist; reviewers should confirm "no behavior change" and "tests pass".
