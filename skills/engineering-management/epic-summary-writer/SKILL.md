---
name: epic-summary-writer
description: >
  Standard format and required fields for epic-summary.md (title, phase, story list with points/tags,
  dependencies, risks). Use when creating or updating an epic folder.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Epic Summary Writer

## Purpose

Define the **standard format and required fields** for `epic-summary.md` so epic folders stay consistent, and workflows (generate-epics-and-stories, push-to-jira, compare-prd-to-jira) can rely on the same structure.

## When to Use

- When creating or updating an epic folder. Epic folders live at **phase** path: `workspace/projects/<slug>/eng/<phase>/` where `<phase>` is one of `alpha`, `beta`, `ga`, `fast-follow` (see `docs/WORKSPACE-PHASES.md`). Legacy single epic folder `workspace/projects/<slug>/eng/epic/` or `epics/` is still valid.
- When the generate-epics-and-stories workflow writes the epic summary (one per phase)
- When adding or removing stories from an existing epic and the summary must be updated

## Required Fields

Every `epic-summary.md` must include:

| Section | Required content |
|---------|------------------|
| **Epic title** | Clear name (e.g. `[Product Area] - [Capability] — [Milestone]`) |
| **Epic description** | 2–3 sentences: business objective, PRD requirements covered |
| **Phase / milestone** | Alpha, Beta, GA, or Fast Follow — must match the epic folder name (`alpha`, `beta`, `ga`, `fast-follow`) |
| **Stories table** | For each story: number or ID, title, tag ([BE], [FE], etc.), status (To Do / Done / Deferred), story points, dependencies (Jira ID or story title), Jira ticket (after push) |
| **Total story points** | Sum of story points for non-deferred stories |
| **Dependency graph** | Which stories block which (optional but recommended; can be a short list or "Story 3 blocks Story 5") |
| **Risks / notes** | Optional: key risks, assumptions, or handoff notes |

## Format (markdown)

Use a markdown table for the stories list. Example:

```markdown
# Epic: [Title]

**Phase:** Alpha | **PRD:** [link or path]

[2-3 sentence description]

## Stories

| # | Title | Tag | Status | Points | Depends on | Jira |
|---|-------|-----|--------|--------|------------|------|
| 1 | Feature toggle | [FF] | To Do | 3 | — | TI-xxxx |
| 2 | Chat guard | [BE] | To Do | 2 | TI-xxxx | |
...

**Total story points:** [sum]

## Dependencies

- Story 1 blocks Story 2, Story 3
- Story 4 (QA) depends on 1, 2, 3

## Risks / Notes

[Optional]
```

## Conventions

- **Cross-references:** Use Jira ticket IDs when they exist; otherwise story titles. Never use local file names or "Story N" only. See `standards/conventions.md`.
- **Naming:** File is `epic-summary.md` in the epic folder. The epic folder is either a **phase folder** (`eng/<phase>/`) or a single epic folder (`eng/epic/`, `epics/`). After push to Jira, the folder is renamed `{EPIC_KEY}-<slug>`; epic-summary.md can stay as-is or be renamed per team preference (see `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md`).

## References

- **Workflows:** `skills/engineering-management/workflow-write-epics-and-stories-from-prd/SKILL.md` (Step 8), `push-to-jira.md`, `compare-prd-to-jira.md`
- **Workspace:** `standards/conventions.md`
