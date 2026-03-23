---
name: jira-labels-and-metadata
description: >
  Map story tags ([BE], [FE], …) to Jira labels, fix version, and components. Use when pushing
  stories to Jira or configuring project metadata.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Jira Labels and Metadata

## Purpose

Provide the **mapping from story tags** (e.g. [BE], [FE], [SEC]) to **Jira labels** and guidance on **fix version** and **components** so pushed issues are consistently tagged and reportable.

## When to Use

- When pushing stories to Jira (sync-local-to-jira workflow Step 5.3)
- When creating or updating a Jira story manually and applying labels
- When configuring or documenting project standards for labels and versions

## Tag → Label Mapping

Use this mapping when adding labels to a Jira story (align with `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md`):

| Story tag | Jira label |
|-----------|------------|
| [BE] | `backend` |
| [FE] | `frontend` |
| [FF] | `feature-flag` |
| [QA] | `qa` |
| [SEC] | `security` |
| [DB] | `database` |
| [LOG] | `observability` |
| [ANALYTICS] | `analytics` |
| [RESEARCH] | `spike` |
| [OPS] | `operations` |
| [DOCS] | `documentation` |
| [PERF] | `performance` |
| [ALERT] | `alerting` |
| [DESIGN] | `design` |

**Sub-tags** (e.g. [BE-1], [BE-2]): use the same label as the parent tag (e.g. `backend`). Optionally add a second label for the sub-index if the project uses it (e.g. `be-1`); otherwise one label is enough.

## Fix Version

- Set **fix version** from the epic's phase or milestone when known (e.g. "Alpha 2026-Q2", "Beta 2026-03"). If the epic has a Jira fix version, use that.
- If the project does not use fix versions, leave unset or follow project conventions.

## Components

- Use **components** only if the Jira project has them configured (e.g. "Catalog", "Search", "Auth"). Map from epic or PRD product area when obvious.
- When in doubt, leave components empty; labels are the primary taxonomy.

## Summary and Description

- **Summary:** Story title **without** the "Story N:" prefix and **without** the [Tag] prefix (e.g. "Conversational Search UI" not "Story 2: [FE] Conversational Search UI"). The tag is represented by the label.
- **Description:** Full story content in markdown (User Story, Context, Technical Details, Acceptance Criteria, Story Points, Cursor Prompt). See sync-local-to-jira Step 5.2.

## References

- **Push to Jira:** `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md` (Step 5.3, 5.4)
- **Jira Architect (tags):** `skills/engineering-management/jira_architect/SKILL.md`
