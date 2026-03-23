---
name: workflow-write-design-story-from-hld
description: >
  From an existing HLD doc to a [DESIGN] story (and optionally more stories). Uses ti-write-hld,
  api-contract-spec, jira_architect, create-story.
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# HLD to design story

Turn an existing High-Level Design document into a [DESIGN] story (and optionally a [DESIGN] + follow-on stories). Ensures API contract and architecture are captured in a Jira-ready story format.

## When to Use

- You have an HLD (or architecture doc) and need a [DESIGN] story for the backlog
- You want to add a design story to an existing epic without running full generate-epics-and-stories
- Design was done outside the PRD pipeline and you want it tracked in Jira

## Prerequisites

- Input: HLD markdown file or path (e.g. from `docs/` or `ti/v3/docs/`)
- Template: `templates/product/[TEMPLATE] HLD.md`
- Skills: `skills/engineering-management/ti-write-hld/SKILL.md`, `skills/engineering-management/api-contract-spec/SKILL.md`, `skills/engineering-management/jira_architect/SKILL.md`; workflow: `skills/engineering-management/workflow-write-story/SKILL.md`
- Optional: Epic folder or Jira epic key for parent

## Step 1: Read the HLD and references

1. **Read** the HLD document. Extract: scope, architecture, data flow, new or changed APIs, components, and risks.
2. **Read** ti-write-hld: how HLD is structured and how it ties to TI context (`ti/v3/`). Read api-contract-spec: checklist for each new/changed endpoint (method, path, request/response, errors, auth, rate limit).
3. **Read** jira_architect for [DESIGN] story type: HLD & API Contract, data flow, OpenAPI/Swagger.

## Step 2: Ensure API contract is explicit (if HLD defines APIs)

1. For each **new or changed** endpoint in the HLD, apply **api-contract-spec**: method/path, request/response schema, errors, auth, rate limiting, versioning. If the HLD is missing any of these, add a short section or bullet list (or call it out in the story as "To be detailed in DESIGN").
2. Optionally produce a minimal OpenAPI snippet (or list of endpoints with key fields) and attach to the story or keep in the HLD.

## Step 3: Write the [DESIGN] story

1. Use **create-story** structure (Step 4 "For Stories") with tag **[DESIGN]**.
2. Title: e.g. "HLD & API contract: [Feature name]". Include: User story (as a dev/architect I want…), Context (link to HLD, PRD, or epic), Technical details (architecture summary, data flow, API summary or link to OpenAPI), Acceptance criteria (HLD approved, API contract documented, diagrams updated, etc.), Story points and justification.
3. In the description, reference the HLD path and any API contract artifact. Add a Cursor prompt (cursor_prompt_builder) if the story will be implemented later.

## Step 4: Optional follow-on stories

1. If the HLD implies concrete [DB], [BE], or [FE] work already scoped elsewhere, you can add "Depends on: [DESIGN] story" to those stories; no need to create them here unless the user asks.
2. If the user wants a full set of stories from the HLD (not just [DESIGN]), run **generate-epics-and-stories** with the HLD as input or point them to that workflow.

## Step 5: Output and optionally push to Jira

1. **Save** the [DESIGN] story to a file, e.g. in the epic folder as `story-N-design-<feature>.md` or in workspace as `YYYY-MM-DD_design-<feature>.md`.
2. **If the user wants it in Jira:** Run create-story Step 5 (push to Jira), set parent to the epic if known. Use **jira-labels-and-metadata** for label `design`.

## References

- HLD template: `templates/product/[TEMPLATE] HLD.md`
- ti-write-hld: `skills/engineering-management/ti-write-hld/SKILL.md`
- api-contract-spec: `skills/engineering-management/api-contract-spec/SKILL.md`
- Create story: `skills/engineering-management/workflow-write-story/SKILL.md`
- Conventions: `standards/conventions.md`
