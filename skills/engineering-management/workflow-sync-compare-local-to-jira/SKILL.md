---
name: workflow-sync-compare-local-to-jira
description: Compare local PRD epics and stories against Jira issues via the Atlassian MCP server
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Compare PRD to Jira

Compare locally generated epics and stories (from the `/generate-epics-and-stories` workflow) against what currently exists in Jira. Works at three levels of granularity: **folder**, **epic**, or **story**.

## Prerequisites

- An epic folder containing `epic-summary.md` and `story-*.md` files. This is either a **phase folder** (e.g. `workspace/projects/<slug>/eng/alpha/`, `eng/beta/`) or a single epic folder (`eng/epic/`, `epics/`). See `docs/WORKSPACE-PHASES.md`.
- The Jira project key where epics/stories should exist (e.g., `TI`)
- The Atlassian MCP server connected (`mcp_atlassian_*` tools available)

---

## Step 0a: Identify the epic folder(s)

The comparison runs on **one epic folder** at a time. An epic folder is either:

- **Phase folder:** `workspace/projects/<slug>/eng/<phase>/` (`alpha`, `beta`, `ga`, `fast-follow`)
- **Single epic folder:** `workspace/projects/<slug>/eng/epic/` or `epics/`

If the project has multiple phase folders, the user may specify which phase to compare, or compare each phase in separate runs. Use the chosen folder as the working directory.

---

## Step 0b: Determine Comparison Scope

The user will specify one of three scopes:

| Scope | Input | What Gets Compared |
|-------|-------|-------------------|
| **Folder** | PRD folder path | All epics and all stories in the folder |
| **Epic** | PRD folder path + epic title | The epic and its child stories |
| **Story** | Path to a single `story-*.md` file | Just that one story |

If the user doesn't specify, default to **Folder** scope.

---

## Step 1: Get Jira Cloud ID

Before any Jira queries, get the cloud ID:

```
Tool: mcp_atlassian_getAccessibleAtlassianResources
```

Store the `cloudId` for all subsequent Jira calls.

---

## Step 2: Read Local PRD Content

### Folder Scope
1. Read the `epic-summary.md` in the PRD folder
2. Extract: Epic title, all story titles, story points, statuses, tags
3. Read each `story-*.md` file
4. For each story, extract: title, user story, acceptance criteria, story points, status (To Do / Done / Deferred)

### Epic Scope
1. Read the `epic-summary.md`
2. Filter to the specified epic
3. Read only the stories belonging to that epic

### Story Scope
1. Read the specified `story-*.md` file
2. Extract its full details

---

## Step 3: Search Jira for Matching Issues

### Find the Epic in Jira

Search for the epic by title using JQL:

```
Tool: mcp_atlassian_searchJiraIssuesUsingJql
JQL: project = "{PROJECT_KEY}" AND issuetype = Epic AND summary ~ "{epic title}"
Fields: summary, status, description, priority, created, updated
```

If no exact match is found, try a broader Rovo search:

```
Tool: mcp_atlassian_search
Query: "{epic title}"
```

### Find Stories in Jira

For each local story, search by title keywords:

```
Tool: mcp_atlassian_searchJiraIssuesUsingJql
JQL: project = "{PROJECT_KEY}" AND issuetype = Story AND summary ~ "{story title keywords}"
Fields: summary, status, description, priority, created, updated, parent
```

**Matching strategy** (in priority order):
1. **Exact title match** — story summary contains the full local story title
2. **Tag + keyword match** — Jira summary contains the category tag (e.g., `[FE]`, `[BE]`) and key terms
3. **Fuzzy match** — Rovo search by story title if JQL returns no results

---

## Step 4: Get Full Details for Matched Issues

For each matched Jira issue, fetch the full details:

```
Tool: mcp_atlassian_getJiraIssue
issueIdOrKey: {matched issue key}
fields: ["summary", "description", "status", "priority", "story_points", "parent", "labels"]
```

If you need to see comments or additional context:

```
Tool: mcp_atlassian_getJiraIssue
issueIdOrKey: {key}
expand: "renderedFields"
```

---

## Step 5: Compare Local vs Jira

For each story, produce a comparison across these dimensions:

| Dimension | Local Source | Jira Source | Comparison Logic |
|-----------|-------------|-------------|-----------------|
| **Exists** | File present | Issue found | Binary: present in Jira or not |
| **Title** | `# Story N: [Tag] Title` | `summary` field | Fuzzy match — flag if significantly different |
| **Status** | To Do / Done / Deferred | Jira workflow status | Map: To Do ↔ Open/Backlog, Done ↔ Done/Closed, Deferred ↔ Won't Do |
| **User Story** | `As a / I want / So that` | Description field | Check if Jira description contains the user story |
| **Acceptance Criteria** | `- [ ]` checklist items | Description field | Count local ACs vs ACs present in Jira description |
| **Story Points** | `Story Points: N` | Story points field | Exact match |
| **Parent Epic** | From `epic-summary.md` | `parent` field | Check Jira story is linked to the correct epic |
| **Cursor Prompt** | `## Cursor Prompt` section | Description field | Check if Jira description includes the Cursor prompt |
| **Dependencies** | `Depends on:` line | Issue links | Check if Jira has corresponding "Blocks"/"is blocked by" links |

### Status Mapping

| Local Status | Expected Jira Statuses |
|-------------|----------------------|
| To Do | Open, To Do, Backlog, New |
| Done | Done, Closed, Resolved |
| Deferred | Won't Do, Deferred, On Hold |

---

## Step 6: Generate Comparison Report

Create a `comparison-report.md` file **inside the epic folder** (or PRD folder for legacy layout) with the following structure:

```markdown
# PRD ↔ Jira Comparison Report

**PRD Folder:** {folder path}
**Jira Project:** {PROJECT_KEY}
**Scope:** {Folder / Epic / Story}
**Date:** {current date}

---

## Summary

| Metric | Count |
|--------|-------|
| Local stories | N |
| Matched in Jira | N |
| Missing from Jira | N |
| In Jira but not local | N |
| Synced (no diffs) | N |
| Diffs found | N |

---

## Epic: {Epic Title}

| Jira Key | Jira Status |
|----------|-------------|
| {KEY} or ❌ Not Found | {status} |

---

## Story Comparison

### ✅ Synced (No Differences)

| # | Local Title | Jira Key | Status |
|---|------------|----------|--------|
| ... | ... | ... | ... |

### ⚠️ Differences Found

#### Story N: {Title}
| Dimension | Local | Jira ({KEY}) | Diff |
|-----------|-------|--------------|------|
| Status | To Do | In Progress | ⚠️ Status mismatch |
| Story Points | 5 | 3 | ⚠️ Points differ |
| Acceptance Criteria | 7 items | 5 items | ⚠️ 2 ACs missing in Jira |
| Cursor Prompt | Present | Missing | ❌ Not in Jira |

### ❌ Missing from Jira

| # | Local Title | SP | Tags |
|---|------------|----|------|
| ... | ... | ... | ... |

### ❓ In Jira but Not in Local PRD

| Jira Key | Title | Status |
|----------|-------|--------|
| ... | ... | ... |
```

---

## Step 7: Suggest Actions

Based on the comparison, suggest concrete actions:

### For stories missing from Jira:
```
"Story 8: [BE] Content Type Indexing is not in Jira.
→ Action: Create Jira issue in project {KEY} with type Story, parent Epic {EPIC_KEY}"
```

### For stories with differences:
```
"Story 3: Event-Driven Indexing — Jira TI-3520 has 3 story points but local says 5.
→ Action: Update TI-3520 story points to 5"
```

### For stories in Jira but not local:
```
"TI-3888: [BE] SCORM Video Extraction exists in Jira but has no local story file.
→ Action: Either add to local PRD or verify it belongs to a different epic"
```

> [!NOTE]
> This workflow is **read-only** — it reports differences but does not automatically create or update Jira issues. Use the suggested actions to decide what to sync.

---

## Scope-Specific Behavior

### Folder Scope (default)
- Compares everything: the epic, all stories, and cross-references Jira for orphaned issues
- Also checks for Jira issues under the epic that don't have a matching local story file
- Produces the fullest report

### Epic Scope
- Targets a specific epic title from `epic-summary.md`
- Only compares stories listed under that epic
- Useful when a PRD folder contains multiple epics

### Story Scope
- Compares a single `story-*.md` file
- Searches Jira for that one story
- Produces a focused single-story diff
- Useful for spot-checking after editing a story locally
