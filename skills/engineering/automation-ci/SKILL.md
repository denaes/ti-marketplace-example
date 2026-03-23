---
name: automation-ci
description: Where CI, lint, and test automation live and how to add or fix them
metadata:
  type: skill
  department: engineering
  source: claude-skills
  version: "1.0"
---
# Automation & CI Skill

## 1. Purpose

Help engineers find **where CI, lint, and test automation** are defined and how to **add or fix** jobs, so that every change is validated consistently and new tests or checks are wired correctly.

## 2. When This Skill Is Used

- Adding a new test suite or lint rule and ensuring it runs in CI.
- Debugging a failing pipeline (e.g. "why did CI fail?").
- Documenting or updating how to run checks locally vs in CI.
- When a story involves "CI", "pipeline", "lint", or "automation".

## 3. Where to Look (TI repo)

- **Root / monorepo:** Check repo root for:
  - `.github/workflows/` — GitHub Actions (if the project uses GitHub).
  - `.gitlab-ci.yml` or similar — GitLab CI (if applicable).
  - `Makefile`, `package.json` scripts — common entry points for lint, test, build.
- **V3 app:** `ti/v3/`:
  - `package.json` — scripts such as `test`, `lint`, `build`; run with `npm run <script>` from `ti/v3/`.
  - Jest config (e.g. `jest.config.js` or in `package.json`) — test runner and coverage.
  - ESLint/Prettier config — usually at repo root or in `ti/v3/`.
- **Architecture / build-time checks:** `ti/v3/docs/ARCHITECTURE_VALIDATOR.md` and plugins (e.g. `ti/v3/plugins/validate-architecture.js`) — may run as part of build or a dedicated script.

If the exact paths differ in your clone, search for `workflows`, `ci`, `jest`, `eslint`, and `npm test` to locate the current setup.

## 4. Adding a New Check

1. **Local first:** Add the test or lint rule so it runs locally (e.g. `npm test`, `npm run lint`). Verify it fails when it should and passes when the code is correct.
2. **Script:** Expose it via a script in `package.json` (or Makefile) so CI can call the same command.
3. **CI job:** Add or update a CI step that runs that script (e.g. `npm run test`, `npm run lint`) in the appropriate job. Use the same Node/npm version as local when possible.
4. **Document:** Update README or developer docs so others know how to run the check locally and what the CI job does.

## 5. Fixing a Failing Pipeline

1. **Reproduce locally:** Run the same command that failed in CI (e.g. `npm test`, `npm run lint`). Fix any failures locally first.
2. **Environment differences:** If it passes locally but fails in CI, check: Node version, env vars, secrets, network (e.g. no external calls in unit tests), file paths, and permissions.
3. **Flaky tests:** If the failure is intermittent, fix or quarantine the test and create a ticket to address the flake; do not leave red CI without a tracked follow-up.
4. **Dependencies:** Ensure lockfile (e.g. `package-lock.json`) is committed and CI installs from it so dependency versions match.

## 6. Conventions

- **No secrets in CI config:** Use repository secrets or env vars provided by the platform; never commit credentials.
- **Fast feedback:** Keep the main pipeline fast (e.g. unit tests and lint first; E2E or heavy jobs in a separate step or on demand).
- **Clear failure messages:** Assertions and lint rules should produce messages that point to the file and fix; document any non-obvious failure in the README or in the skill.

## 7. Relation to Other Skills

- **Unit tests:** `unit-testing-v3` — ensure new tests are run by the same `npm test` (or equivalent) that CI uses.
- **E2E:** `e2e-playwright` — E2E may run in a separate CI job with a different env (e.g. staging); document that job here or in the project README.
- **Code review:** `code-review-checklist` — CI should cover the same quality bar (lint, tests, build) that reviewers expect.
