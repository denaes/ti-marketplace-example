---
name: code-review-checklist
description: Quick checklist for reviewing code (PRs, security, tests, conventions)
metadata:
  type: skill
  department: engineering
  source: ti-rd-playbook
  version: "1.0"
---
# Code Review Checklist Skill

## 1. Purpose

Provide a **consistent checklist** for engineers (and AI) when reviewing code changes so that PRs meet quality, security, and convention bars before merge.

## 2. When This Skill Is Used

- Reviewing a pull request (user asks "review this PR" or "check my changes").
- Before marking a story done: self-review against the checklist.
- When the user asks "what should I check before submitting?"

## 3. Checklist (apply as relevant to the change)

### Functionality and scope

- [ ] Changes match the ticket scope (Jira key or story); no unrelated edits.
- [ ] Acceptance criteria are met; edge cases and error paths are handled.
- [ ] No debug code, commented-out blocks, or TODOs without a ticket reference (or remove before merge).

### Architecture and patterns

- [ ] Follows existing patterns (e.g. hexagonal adapters in V3: inject interface via DI token, not concrete class).
- [ ] No new `@ts-ignore` or `eslint-disable` without a short comment and/or ticket; prefer fixing the cause.
- [ ] Respects module boundaries and architecture rules (see `ti/v3/docs/ARCHITECTURE_VALIDATOR.md` when applicable).
- [ ] New dependencies are justified; no unnecessary new packages.

### Security and data

- [ ] No secrets, API keys, or credentials in code or committed config; use env vars or secure config.
- [ ] Auth and authorization are enforced where required (guards, permission checks); no privilege escalation.
- [ ] PII and sensitive data are not logged in plain text; inputs are validated/sanitized where needed.

### Tests

- [ ] New or changed behavior has tests (unit and/or E2E as specified in the story).
- [ ] Tests are stable (no flaky or order-dependent tests); failing tests are fixed, not skipped, unless with a ticket.
- [ ] Test names and structure are clear; coverage is sufficient for the changed code paths.

### Conventions and docs

- [ ] Paths and cross-references use Jira ticket IDs where relevant; see `standards/conventions.md`.
- [ ] Public APIs, config, or env vars are documented (README, .env.sample, or inline) when they affect other devs or ops.
- [ ] If the change is a significant decision, consider an ADR (see `skills/engineering/adr-writer/SKILL.md`).

### Performance and operations

- [ ] No obvious N+1 queries, unbounded loops, or heavy work on hot paths without justification.
- [ ] Logging is structured and useful for debugging; no excessive log volume in normal operation.
- [ ] Feature flags or rollout considerations are in place when the change is user-facing or risky.

## 4. Output

When performing a review, produce a short summary:

- **LGTM** (or "Approved") with optional notes if the checklist is satisfied.
- **Comments** listing specific items to fix (file + line or area) with the checklist category (e.g. "Security: no hardcoded key").
- **Suggestions** (non-blocking) for clarity, tests, or docs.

Keep feedback actionable and tied to the checklist so the author knows what to change.

## 5. Relation to Other Skills

- **Implementation:** Implementation should already follow `implementation-from-story` and Cursor prompt DO NOTs; the checklist catches what might have been missed.
- **Testing:** Align with `unit-testing-v3` and `e2e-playwright` for test quality.
- **Conventions:** `standards/conventions.md` and `codebase-navigation` for paths and references.
