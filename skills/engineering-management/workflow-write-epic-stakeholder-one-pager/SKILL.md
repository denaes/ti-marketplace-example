---
name: workflow-write-epic-stakeholder-one-pager
description: >
  Produce a one-pager for product/leadership from an existing epic folder. Uses
  epic-stakeholder-summary, epic-summary-writer (read).
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Epic stakeholder one-pager

Produce a one-page summary of an epic for product or leadership: scope, story count, risks, timeline. Not the full epic-summary or backlog — a short narrative for prioritization and roadmap.

## When to Use

- You need to communicate epic status or scope to stakeholders outside the backlog
- You are preparing a roadmap slot or release update and need a short epic summary
- Someone asks "what's in this epic?" and you want a consistent one-pager format

## Prerequisites

- An epic folder with `epic-summary.md` (and optionally story files). This is either a **phase folder** (`workspace/projects/<slug>/eng/<phase>/`) or a single epic folder (`eng/epic/`, `epics/`). See `docs/WORKSPACE-PHASES.md`.
- Skill: `skills/engineering-management/epic-stakeholder-summary/SKILL.md`; reference `skills/engineering-management/epic-summary-writer/SKILL.md` for epic-summary structure

## Step 1: Read the epic

1. **Read** `epic-summary.md` in the epic folder. Extract: epic title, description, phase, stories table (count, points, tags), total points, dependency graph, risks/notes.
2. **Read** epic-stakeholder-summary: required sections (objective, scope, story count, points, risks, timeline) and one-page max format.

## Step 2: Draft the one-pager

1. Use **epic-stakeholder-summary** to fill: Epic name, Objective (1–2 sentences), Scope (3–5 bullets), Story count and optional breakdown, Story points and optional "~N sprints", Risks/blockers (1–3 bullets), Timeline (phase and target date/quarter).
2. Keep to **one page**. Do not copy the full stories table; link to the epic folder or Jira epic for details.
3. Optionally add "Out of scope" or "Dependencies on other epics" if relevant.

## Step 3: Output and next steps

1. Write the one-pager to a file in the epic folder, e.g. `epic-stakeholder-one-pager.md`. No timestamp prefix; Git versions the file.
2. Tell the user they can paste it into Confluence, email, or roadmap doc.

## References

- Epic summary format: `skills/engineering-management/epic-summary-writer/SKILL.md`
- Conventions: `standards/conventions.md`
