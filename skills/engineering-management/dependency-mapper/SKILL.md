---
name: dependency-mapper
description: >
  How to express story/epic dependencies (Blocks, Blocked by), Jira link types, and ordering. Use
  when listing Depends on in stories or when linking issues in Jira.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Dependency Mapper

## Purpose

Define **how to express and document** story-to-story and epic-to-epic dependencies so the backlog has a clear dependency graph, and Jira issue links stay correct when pushing or updating.

## When to Use

- When writing the **Depends on:** line in a story file
- When creating or updating **issue links** in Jira (sync-local-to-jira, or manual link creation)
- When ordering stories for generation or sprint planning

## In Story Files

In every story markdown file, use:

```markdown
**Depends on:** TI-3516, TI-3517
```

or, if Jira tickets do not exist yet:

```markdown
**Depends on:** Instance-Level Feature Toggle, Chat Backend Guard
```

- **Use Jira ticket IDs** when they exist (e.g. `TI-3516`). See `standards/conventions.md`.
- **Use story titles** when tickets have not been created yet. After sync-local-to-jira, update local files to replace titles with Jira IDs (sync-local-to-jira Step 6).
- **Never** use only "Story 2" or file names.
- List **all** blockers: any story that must be done before this one.

## Jira Link Types

When creating links in Jira (e.g. via `mcp_atlassian_jiraWrite` or Jira UI):

- **Blocks / Blocked by:** Story A "Blocks" Story B means B is blocked by A (A must be done first). In Jira, create a link of type **Blocks** from A to B (or "is blocked by" from B to A, depending on project configuration).
- Use the project's **issue link types** (e.g. `getIssueLinkTypes`) to get the exact names (e.g. "Blocks", "is blocked by").
- After sync-local-to-jira, Step 7 creates "Blocks" links from the **dependent** story to the **dependency**: e.g. Story 3 depends on Story 1 → link Story 3 "is blocked by" Story 1 (or Story 1 "Blocks" Story 3).

## Ordering

- **Generation order:** When generating stories, list dependencies so that no story depends on a story that comes later in the epic. If circular or ambiguous, call it out and ask the user.
- **Epic summary:** The epic-summary should list dependencies (e.g. "Story 3 blocks Story 5") or a small dependency graph so compare/push and reporting stay consistent.

## References

- **Push to Jira (links):** `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md` Step 7
- **Conventions:** `standards/conventions.md` (cross-referencing)
