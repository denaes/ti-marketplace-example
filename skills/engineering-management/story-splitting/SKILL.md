---
name: story-splitting
description: >
  How to split oversized stories (e.g. [BE] >3 endpoints) into [BE-1], [BE-2] with clear scope and
  dependencies. Use when a story exceeds point cap or scope.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Story Splitting

## Purpose

Define **when and how** to split an oversized story into smaller stories (e.g. [BE-1], [BE-2]) so each stays within the point scale and remains implementable in one sprint. Aligns with `jira_architect` and `story-estimation`.

## When to Use

- When a [BE] story covers **more than 3 endpoints or 3 distinct services**
- When a story is estimated at **5 or 8** and could be split by logical boundary
- When a [FE] story spans more than one major screen or user flow
- When refinement identifies a "and also…" scope that belongs in a separate story

## Splitting Rules

| Story type | Trigger to split | How to split |
|------------|------------------|--------------|
| **[BE]** | >3 endpoints or >3 services | One story per endpoint group or per service; shared [DESIGN]/[DB] as dependency. |
| **[FE]** | >1 major screen or flow | One story per screen or per user journey; shared [BE] or [DESIGN] as dependency. |
| **[QA]** | >1 test suite or >1 epic area | One story per suite or per epic; dependencies on the stories under test. |
| **Generic** | Points would be 5 or 8 | Split by "vertical slice" (one capability) or by layer (e.g. API first, then integration). |

## Naming and Tags

- Use **sub-tags** when useful: [BE-1], [BE-2], [FE-1], [FE-2]. Not required; plain [BE] with distinct titles is fine.
- **Titles** must be distinct and scoped: e.g. "Catalog AEO pages list endpoint" vs "Catalog AEO pages update endpoint".
- In **epic-summary.md**, list each child story with its own row and dependency (e.g. [BE-2] depends on [BE-1] if order matters).

## Dependencies Between Split Stories

- If order matters (e.g. "list" before "update"), set **Depends on:** from the later story to the earlier one.
- Shared work (e.g. [DESIGN], [DB]) should be a single story that **blocks** all [BE-x] stories.
- After splitting, **re-estimate** each new story (see `story-estimation`).

## References

- **Estimation:** `skills/engineering-management/story-estimation/SKILL.md`
- **Jira Architect:** `skills/engineering-management/jira_architect/SKILL.md`
- **Dependencies:** `skills/engineering-management/dependency-mapper/SKILL.md`
