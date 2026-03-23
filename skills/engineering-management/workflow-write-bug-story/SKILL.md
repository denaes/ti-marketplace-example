---
name: workflow-write-bug-story
description: >
  From a bug report or root cause doc to a well-structured bug story (and optionally create in Jira).
  Uses bug-story-writer, create-story (bug path).
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Bug to story

Turn a bug report, support ticket, or root cause analysis into a single, well-structured bug story (repro, expected vs actual, root cause, AC for fix, regression test). Optionally create the story in Jira via the create-story workflow.

## When to Use

- You have a bug report or post-incident write-up and need a Jira-ready bug story
- You want consistent structure (repro steps, AC, regression test) for triage and handoff to engineering
- You are turning a root cause analysis into a fix story

## Prerequisites

- Input: bug description, repro steps, or root cause doc (paste, file, or link)
- Skills: `skills/engineering-management/bug-story-writer/SKILL.md`; workflow: `skills/engineering-management/workflow-write-story/SKILL.md` (bug path)
- Optional: Atlassian MCP for creating the Jira issue

## Step 1: Gather bug context

1. **Confirm with the user:** Do they have repro steps, expected vs actual, environment, and (if known) root cause? If not, ask for what they have; use "TBD – investigate in this story" where needed per `standards/conventions.md`.
2. **Optional:** If the bug is in the TI codebase, search for relevant code (affected area, stack trace, or error message) to inform root cause and proposed fix.

## Step 2: Read reference materials

1. **bug-story-writer** — `skills/engineering-management/bug-story-writer/SKILL.md`: required sections (repro steps, expected vs actual, root cause, AC, regression test), optional (environment, impact, links).
2. **create-story** — `skills/engineering-management/workflow-write-story/SKILL.md` Step 4 "For Bugs": markdown format (title, severity, description, root cause, proposed fix, AC, story points).

## Step 3: Write the bug story

1. Apply **bug-story-writer** to produce the full bug story in markdown: Bug context (repro, expected/actual, root cause), Acceptance criteria, Regression test.
2. Use the **create-story** bug format so the output is consistent with other bugs (Severity, Reported by, Bug Description, Context & Root Cause, Proposed Fix, AC, Story Points).
3. If root cause is unknown, state "TBD – investigate in this story" and add an AC to document root cause.

## Step 4: Output and optionally push to Jira

1. **Save** the story to a file, e.g. in the epic folder or `workspace/` as `YYYY-MM-DD_bug-<short-name>.md`.
2. **If the user wants it in Jira:** Run the create-story workflow from Step 2 (gather context) and Step 4 (write bug) using this content; then use create-story Step 5 (push to Jira) with issue type "Bug" (or "Story" with [BUG] label per project). Use **jira-labels-and-metadata** for labels if needed.

## References

- Bug story skill: `skills/engineering-management/bug-story-writer/SKILL.md`
- Create story: `skills/engineering-management/workflow-write-story/SKILL.md`
- Conventions: `standards/conventions.md`
