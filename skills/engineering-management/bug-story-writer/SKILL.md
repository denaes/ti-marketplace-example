---
name: bug-story-writer
description: >
  Structure for bug stories—repro steps, expected vs actual, root cause, AC for fix, regression test.
  Use when creating a story from a bug report or root cause analysis.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Bug Story Writer

## Purpose

Define a **standard structure** for bug stories so each has clear repro steps, expected vs actual behavior, root cause (if known), acceptance criteria for the fix, and a regression test. Supports triage and handoff to engineering.

## When to Use

- When creating a story from a **bug report** or support ticket
- When turning a **root cause analysis** or post-incident finding into a fix story
- When the create-story workflow is used for "bug" type (see `skills/engineering-management/workflow-write-story/SKILL.md`)

## Required Sections

Every bug story must include:

| Section | Content |
|---------|---------|
| **Summary / title** | Short, actionable: e.g. "Search returns 500 when company has no catalog" |
| **Repro steps** | Numbered steps to reproduce (environment, user role, actions, input data). |
| **Expected vs actual** | Expected behavior (from spec or product) vs what actually happens. |
| **Root cause** | If known: code path, config, or design flaw. If unknown: "TBD – investigation in this story" or link to [RESEARCH] spike. |
| **Acceptance criteria** | Testable outcomes: "When X, then Y"; "Error response is 404 with body Z"; "No PII in logs". |
| **Regression test** | How we prevent recurrence: new E2E, unit test, or monitoring check. Can be same story or follow-up [QA] story. |

## Optional

- **Environment / version:** Where it was seen (staging, prod, browser, API version).
- **Impact:** Severity, user impact, workaround.
- **Links:** Jira incident, Sentry, or internal doc.

## Format (in story markdown)

```markdown
## Bug context
**Repro steps:**  
1. …  
2. …

**Expected:** …  
**Actual:** …

**Root cause:** [brief or "TBD – investigate in this story"]

## Acceptance criteria
- [ ] …
- [ ] …

## Regression test
- [ ] Add unit test for … / E2E scenario … / Alert when …
```

## References

- **Create story:** `skills/engineering-management/workflow-write-story/SKILL.md`
- **QA:** `skills/engineering-management/qa_test_planner/SKILL.md` (for regression test ideas)
