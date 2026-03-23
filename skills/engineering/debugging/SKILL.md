---
name: debugging
description: Systematic debugging (reproduce, isolate, hypothesize, fix, verify)
metadata:
  type: skill
  department: engineering
  source: claude-skills
  version: "1.0"
---
# Debugging Skill

## 1. Purpose

Apply a **systematic approach** to debugging (bugs, test failures, or unexpected behavior) so that root cause is found and fixed without introducing new issues.

## 2. When This Skill Is Used

- The user reports a bug, a failing test, or "this doesn't work as expected".
- Investigating a production or staging incident (logs, errors, user steps).
- Understanding why a change broke something (regression).

## 3. Steps (high level)

1. **Reproduce:** Confirm the failure with clear steps (or a failing test). If you cannot reproduce, gather more data (logs, env, version) or add logging to reproduce next time.
2. **Isolate:** Narrow the scope — which component, which call path, which input? Use breakpoints, logs, or smaller tests to isolate.
3. **Hypothesize:** Form a hypothesis for the cause (e.g. "null not handled", "wrong order of operations", "stale cache").
4. **Verify:** Test the hypothesis (e.g. add a minimal repro, inspect state, or add a temporary assert). If wrong, revise and repeat.
5. **Fix:** Implement a minimal fix that addresses the root cause. Prefer fixing the cause over working around it (e.g. fix the null path instead of adding a global try/catch).
6. **Verify fix:** Re-run the repro and the full test suite; ensure no regression. Add or update a test that would have caught this bug if possible.

## 4. TI / V3 Specific Aids

- **Logs:** Structured logging in V3; search for trace IDs or correlation IDs to follow a request. Check log level (e.g. debug vs info) and where logs are emitted (controller, service, adapter).
- **Guards and auth:** Many "unexpected" behaviors are auth or permission related. Check `CompanyContextGuard`, `CompositeAuthGuard`, and feature-flag checks; confirm the user/company has the right context and flags.
- **Events and async:** V3 uses event-driven flows (e.g. indexation). If something "never happens", check that events are emitted (e.g. `V3_EMIT_EVENTS`), that listeners are registered, and that async work completes (no swallowed promises).
- **Database and Redis:** Stale or missing data: check migrations, connection, and caching (e.g. Redis TTL for feature flags). Compare expected vs actual state in DB/Redis when safe.
- **Tests:** A failing unit test often points to the exact line; use the test to narrow the cause. Run the single test in watch mode while you change code.
- **Docs:** `ti/v3/docs/` (ARCHITECTURE.md, INTERNAL_RPC.md, flows) explain data flow and boundaries; use them to understand where the bug might sit.

## 5. Asking the Right Questions

- **What exactly happens?** (error message, status code, UI state.)
- **What did you expect?** (from ACs or spec.)
- **When did it last work?** (commit, release, or "never in this env.")
- **What changed?** (recent deploy, config change, data change.)
- **Can you reproduce it?** (steps, env, user/company.)

## 6. Output

When helping the user debug:

- Summarize **reproduction steps** and **observed vs expected**.
- State the **hypothesis** and how you verified it.
- Propose a **concrete fix** (file, change) and **how to verify** (run test X, manual step Y).
- If the root cause is unclear, suggest **next steps** (e.g. add logging here, run this query, check that config).

## 7. Do Not

- Do not guess at fixes without a hypothesis; random changes can hide the bug or create new ones.
- Do not ignore failing tests; fix or quarantine with a ticket.
- Do not commit debug code (console.log, debugger) or temporary hacks without a follow-up ticket to clean up.
- Do not change behavior beyond what is needed to fix the bug unless the ticket explicitly includes that change.

## 8. Relation to Other Skills

- **Codebase navigation:** Finding the right file and call path is part of isolation.
- **Unit testing:** Writing a failing test that reproduces the bug is a strong way to isolate and prevent regression.
- **Code review:** After the fix, a quick self-review (e.g. code-review-checklist) helps avoid collateral damage.
