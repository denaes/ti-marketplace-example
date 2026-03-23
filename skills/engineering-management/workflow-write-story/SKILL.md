---
name: workflow-write-story
description: Interactively create a Jira-ready Story or Bug with the IDE agent — no PRD needed
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Create Story or Bug (Interactive)

An interactive, conversational workflow for creating individual Stories or Bugs directly with the IDE agent. No PRD required — the agent gathers context through questions, optionally researches the codebase, and produces a fully specified, Jira-ready issue.

## When to Use

- You have an idea for a feature, improvement, or bug fix but no formal PRD
- You want to quickly create a well-structured story from a verbal description or chat
- You spotted a bug and want to document it properly with codebase context
- You need to add stories to an existing epic without going through the full PRD pipeline

## Prerequisites

- Access to the skills in `skills/engineering-management/` for quality standards
- Access to the Atlassian MCP server (`mcp_atlassian_*` tools) if pushing to Jira
- Access to the codebase (optional — for code-aware stories)

---

## Step 1: Read Reference Materials

Read these files to understand quality standards:

1. **Shared conventions** — `standards/conventions.md`
2. **Jira Architect Skill** — `skills/engineering-management/jira_architect/SKILL.md` — story types and tags
3. **Cursor Prompt Builder Skill** — `skills/engineering-management/cursor_prompt_builder/SKILL.md` — prompt template
4. **Story examples** — Read 2-3 files from `workspace/_references/story-examples/` for format reference

---

## Step 2: Gather Context (Interactive)

**Ask as many questions as needed** — do not write the story until scope, type, and key acceptance criteria are clear. Do not make decisions in place of the user. If something is ambiguous, ask. See `standards/conventions.md` (Ask before deciding). Before writing the story (Step 4), **search the codebase** for the area involved and **surface current state to the user** (what exists today, relevant files/patterns) so proposals respect existing architecture. See `standards/conventions.md` (Codebase-first).

Start a structured conversation with the user to understand the request. Ask **one round** of questions covering (expand with more questions if needed):

### 2a. Issue Type

> **What type of issue is this?**
> - **Story** — A new feature, enhancement, or capability
> - **Bug** — Something is broken or behaving unexpectedly

### 2b. Core Description

> **Describe what you want in 2-3 sentences.**
> - For a Story: What should the user be able to do? Who benefits?
> - For a Bug: What's happening? What should happen instead?

### 2c. Context & Scope

> **A few quick scoping questions:**
> 1. Does this belong to an **existing Jira epic**? If so, which one? (key or name)
> 2. Should this be **assigned** to someone specific?
> 3. What's the **priority**? (Critical / High / Medium / Low)
> 4. Any **specific files, modules, or areas** of the codebase involved?
> 5. Any **acceptance criteria** you already have in mind?

### 2d. Optional: Codebase Research

> **Should I research the codebase** to add technical context?
> - If yes: I'll search for relevant files, patterns, and existing implementations
> - If no: I'll write the story from your description only

**Adapt the questions to what the user has already provided.** If they gave a detailed description upfront, skip redundant questions. If they mentioned specific files, don't ask about codebase areas. The goal is to **fill gaps by asking, not by assuming**. When in doubt, ask one more question rather than deciding for the user.

---

## Step 3: Codebase Research (if requested)

If the user wants codebase-aware context:

1. **Search for related code** using keywords from the description:
   ```
   grep_search, find_by_name, view_code_item
   ```

2. **Identify:**
   - Which module(s) and files are affected
   - Existing patterns that can be reused (feature flags, event system, guards, adapters)
   - Related existing stories or implementations
   - Schema or API surface changes needed

3. **Summarize findings** for the user before writing the story — confirm direction is correct

---

## Step 4: Write the Story/Bug

### For Stories

Write the story following the established format:

```markdown
# [Tag] Story Title

**Depends on:** (if any)

## User Story

**As a** [persona],
**I want** [capability],
**so that** [benefit].

## Context & Current State

[2-5 paragraphs from codebase research or user description]

## Technical Details

### [BE] Backend Changes
### [FE] Frontend Changes
### [SEC] Security
### [DB] Data Changes
### [LOG] Observability
(Include only relevant subsections)

## Acceptance Criteria

- [ ] [Specific, testable criterion]
- [ ] ...

## Story Points: N

**Justification:** [1-2 sentences]

---

## Cursor Prompt

(Generated from cursor_prompt_builder skill)
```

**Tag selection** — Choose the primary tag from:
`[RESEARCH]`, `[DESIGN]`, `[DB]`, `[BE]`, `[FE]`, `[SEC]`, `[QA]`, `[ANALYTICS]`, `[LOG]`, `[ALERT]`, `[FF]`, `[DOCS]`, `[PERF]`, `[OPS]`

If the story spans multiple areas, use the dominant one for the tag and include subsections for the others.

### For Bugs

Write the bug following this format:

```markdown
# [BUG] Bug Title

**Severity:** Critical / High / Medium / Low
**Reported by:** [user name or source]

## Bug Description

**What happens:** [Current broken behavior]
**What should happen:** [Expected behavior]
**How to reproduce:**
1. [Step 1]
2. [Step 2]
3. [Observed result]

## Context & Root Cause Analysis

[From codebase research — explain WHY this is happening]
- Affected files and functions
- The code path that leads to the bug
- Related components or side effects

## Proposed Fix

### Technical Details
[Specific code changes needed]

### Impact & Risk
- Blast radius: [What else could be affected]
- Regression risk: [Low / Medium / High]

## Acceptance Criteria

- [ ] [The bug is fixed — specific verification]
- [ ] [No regression in related areas]
- [ ] [Test coverage added]

## Story Points: N

**Justification:** [1-2 sentences]

---

## Cursor Prompt

(Generated from cursor_prompt_builder skill)
```

---

## Step 5: Save the Story/Bug

Save the file with an ISO datetime prefix:

- **Location:** If linked to an epic folder in `prds/`, save there. Otherwise save in the conversation artifacts directory.
- **Filename:** `{YYYY-MM-DDTHH:MM:SS}-story-{short-slug}.md` or `{YYYY-MM-DDTHH:MM:SS}-bug-{short-slug}.md`
- Example: `2026-03-06T11:20:00-story-feature-flag-auto-backfill.md`

Present to the user for review via `notify_user`.

---

## Step 6: Push to Jira (optional)

If the user wants to push to Jira:

1. **Get Jira context:**
   ```
   mcp_atlassian_getAccessibleAtlassianResources → Cloud ID
   ```

2. **Resolve the parent epic** (if specified):
   ```
   mcp_atlassian_searchJiraIssuesUsingJql
   jql: project = TI AND issuetype = Epic AND summary ~ "{epic name}"
   ```

3. **Look up assignee** (if specified):
   ```
   mcp_atlassian_lookupJiraAccountId
   ```

4. **Create the issue:**
   ```
   mcp_atlassian_createJiraIssue
   - projectKey: TI (or user-specified)
   - issueTypeName: "Story" or "Bug"
   - summary: Title (without tag prefix)
   - description: Full markdown content
   - parent: Epic key (if applicable)
   - assignee_account_id: (if applicable)
   ```

5. **Add labels** based on the story tag (same mapping as `/push-to-jira`):
   - `[BE]` → `backend`, `[FE]` → `frontend`, `[QA]` → `qa`, etc.

6. **Report back** with the Jira ticket key and link.

---

## Interaction Style

This workflow is designed to be **lightweight and conversational**:

- **Don't over-ask** — If the user gives a rich description, skip unnecessary questions
- **Show, don't tell** — Write the story draft, then ask for feedback rather than discussing format
- **Iterate fast** — If the user wants changes, update the story and re-present
- **Default to pushing** — After the user approves, ask "Want me to push this to Jira?" rather than requiring them to ask
- **Remember context** — If the user mentions an epic, file, or person from earlier in the conversation, use that context

## Quality Checklist

Before finalizing, verify:

- [ ] Story has concrete acceptance criteria (no vague language)
- [ ] Story points are justified
- [ ] Dependencies are stated (if any)
- [ ] Cursor prompt includes specific file paths and code patterns (if codebase was researched)
- [ ] For bugs: reproduction steps are clear and root cause is identified
- [ ] Tag matches the primary work area
