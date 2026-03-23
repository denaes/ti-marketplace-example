---
name: jira-epic-folder-matcher
description: >
  Resolve Jira epic and child stories for a local epic folder; match local stories to Jira issues.
  Use when building sync report or comparing one epic folder to Jira.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Jira Epic–Folder Matcher

## Purpose

Given a **local epic folder** (path + optional Jira epic key from workspace-epic-scanner), **resolve the Jira epic** (by key or by title search) and **list all Jira stories** under that epic. Then **match** local story files to Jira issues so the sync report can classify: Create in Jira, Update in Jira, In sync, Jira-only (create local), Jira newer (update local).

## When to Use

- When running the **sync-workspace-jira-report** workflow for each epic folder
- When you need to know "what's in Jira for this epic" and "how does that map to local files"
- After **workspace-epic-scanner** has produced the list of epic folders

## Prerequisites

- **Cloud ID:** From `getAccessibleAtlassianResources` (store for all Jira MCP calls).
- **Jira project key:** Typically `TI`. Use `getVisibleJiraProjects` if needed.
- **Epic folder path** and, if known, **Jira epic key** from epic-summary or folder name.

## Step 1: Resolve Jira Epic

- If we already have a **Jira epic key** (e.g. `TI-3613`) from the scanner: fetch the epic with `getJiraIssue(cloudId, issueIdOrKey)` and confirm it is an Epic issue type. Use this as the **resolved epic**.
- If we have **no key** or the key is ambiguous: search by **epic title** from `epic-summary.md` using JQL:
  - `project = TI AND issuetype = Epic AND summary ~ "{epic title}"`
  - Use `searchJiraIssuesUsingJql` with `maxResults` 10; pick best match by title similarity.
- If multiple epics match (e.g. Alpha vs Beta): prefer the one whose summary/description best matches the **phase** (alpha/beta/ga/fast-follow) indicated by the epic folder path or epic-summary.

**Output:** `epic_key`, `epic_summary`, `epic_status`.

## Step 2: List Jira Stories Under the Epic

Use JQL to get all issues that are **children** of the resolved epic:

- **JQL:** `project = TI AND issuetype = Story AND parent = {epic_key}`  
  (Standard Jira: Stories link to Epic via `parent`. If the project uses "Epic Link" field instead, use the appropriate field name in JQL, e.g. `"Epic Link" = {epic_key}` — check project metadata if needed.)

Fetch with `searchJiraIssuesUsingJql`; request fields: `summary`, `status`, `description`, `updated`, `parent`. Use `maxResults` 100 and paginate if needed.

**Output:** List of `{ key, summary, status, updated }` for each Jira story.

## Step 3: Match Local Stories to Jira

For each **local story file** in the epic folder (from workspace-epic-scanner):

- **If filename has Jira key** (e.g. `TI-3927-story-1-aeo-pages-catalog.md`): match to that Jira issue key. If that key is in the list from Step 2, it's a **match**.
- **If no key in filename:** derive a **title** from the file (first `# Story N: ...` or first `#` line). Search in the Jira story list by **summary** (fuzzy: contains or very similar). If one Jira story matches, associate it.

For each **Jira story** from Step 2:

- If it was matched to a local file: we have a **pair** (local ↔ Jira).
- If it was **not** matched to any local file: it's **Jira-only** (candidate for "pull from Jira → create local" or at least list in report).

## Step 4: Classify Sync Direction

For each **local story**:

| Classification | Condition | Report section |
|----------------|-----------|----------------|
| **Create in Jira** | No matching Jira issue | Push to Jira |
| **Update in Jira** | Matching Jira issue exists but content differs (e.g. status, ACs, story points, description) | Push to Jira |
| **In sync** | Matching Jira issue and no material diff | In sync |

For each **Jira story**:

| Classification | Condition | Report section |
|----------------|-----------|----------------|
| **Jira-only (create local)** | No local story file | Pull from Jira |
| **Jira newer (update local)** | Has matching local file but Jira `updated` > local file mtime or Jira content differs | Pull from Jira |
| **In sync** | Same as above "In sync" | In sync |

**Diff rules (for Update in Jira / Jira newer):** Compare status (map local To Do/Done/Deferred to Jira status), story points, acceptance criteria count or key text, description. If any differ, mark as needing update. Do **not** auto-update; the sync report only reports. A separate skill/workflow can "apply pull" or "apply push" later.

## Optional: Discover Epics Not Linked to Workspace

To "consider as much as possible" (per user): optionally search Jira for **other** epics that might relate to the same project (e.g. same product name in summary). Use JQL like `project = TI AND issuetype = Epic ORDER BY updated DESC` with a reasonable `maxResults`, then filter by title/keywords. List in the report as "Epics in Jira (no local folder)" or "Consider linking" so the user can decide to create a local folder or link later.

## References

- **Compare workflow:** `skills/engineering-management/workflow-sync-compare-local-to-jira/SKILL.md` (matching strategy, status mapping)
- **Push workflow:** `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md` (parent epic, story create/update)
- **Conventions:** `standards/conventions.md` (cross-references, Jira key in filenames)
