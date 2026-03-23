---
name: workflow-guide-me-to-refine-epic
description: >
  Re-estimate stories, fix dependencies, split oversized stories, refresh epic-summary. Uses
  story-estimation, dependency-mapper, story-splitting, epic-summary-writer.
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Refine epic (estimation and dependencies)

Given an epic folder with `epic-summary.md` and story files, (re)estimate story points, fix dependency ordering, split any oversized stories, and refresh the epic summary so the epic is ready for sprint planning or push-to-jira.

## When to Use

- An epic has been generated but story points or dependencies need adjustment
- Stories are too large (e.g. [BE] with >3 endpoints) and should be split
- You want to refresh the epic-summary table and dependency graph after adding/removing stories

## Prerequisites

- An epic folder with `epic-summary.md` and `story-*.md` files. This is either a **phase folder** (`workspace/projects/<slug>/eng/<phase>/` where `<phase>` is `alpha`, `beta`, `ga`, or `fast-follow`) or a single epic folder (`eng/epic/`, `epics/`). See `docs/WORKSPACE-PHASES.md`.
- Skills: `skills/engineering-management/story-estimation/SKILL.md`, `skills/engineering-management/dependency-mapper/SKILL.md`, `skills/engineering-management/story-splitting/SKILL.md`, `skills/engineering-management/epic-summary-writer/SKILL.md`

## Step 1: Read the epic and skills

1. **Read** `epic-summary.md` and list all story files.
2. **Read** story-estimation (point scale 1/2/3/5/8, justification, when to split), dependency-mapper (Depends on, Jira link types), story-splitting (when to split [BE]/[FE], naming), epic-summary-writer (required fields and format).

## Step 2: Review each story — estimation and split

1. For each story file:
   - **Estimate:** Apply story-estimation. Ensure points have a one-line justification; if 5 or 8, consider splitting per story-splitting.
   - **Split:** If a story is oversized (e.g. [BE] >3 endpoints, or points would be 5/8), apply story-splitting: create [BE-1], [BE-2] (or similar) with clear scope and Depends on. Re-estimate each new story.
2. Update or create story files; keep naming consistent (e.g. story-N-short-description.md).

## Step 3: Review and fix dependencies

1. Apply **dependency-mapper**: for each story, set **Depends on:** to Jira IDs (if known) or story titles. Ensure no story depends on a story that comes later in the epic; if circular or ambiguous, call it out and ask the user.
2. Order the story list so dependencies are respected (e.g. [DESIGN] and [DB] before [BE]/[FE], [QA] after implementation stories).

## Step 4: Refresh epic-summary.md

1. Apply **epic-summary-writer**: update the stories table with title, tag, status, story points, Depends on, and Jira column (if pushed). Recompute total story points. Update the dependency graph section (which story blocks which).
2. Save `epic-summary.md` in the same epic folder.

## Step 5: Confirm with user

1. Summarize changes: stories split, points changed, dependencies fixed, epic-summary updated.
2. Tell the user they can run **push-to-jira** or **compare-prd-to-jira** next if the epic is already in Jira.

## References

- Conventions: `standards/conventions.md`
- Workspace: `standards/conventions.md`
- Push to Jira: `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md`
