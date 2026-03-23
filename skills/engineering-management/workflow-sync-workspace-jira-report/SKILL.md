---
name: workflow-sync-workspace-jira-report
description: >
  Sync report — workspace/projects vs Jira; dated report of what to push vs pull (per
  project/epic/story). Uses workspace-epic-scanner, jira-epic-folder-matcher, sync-report-writer.
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Sync Workspace–Jira Report

Produce a **dated sync report** that compares `workspace/projects/` with Jira and shows **what needs to be pushed to Jira** (create/update) and **what needs to be pulled from Jira** (create local file / update local file), with granular details per project, epic, and story. The report is **read-only** — it does not create or update Jira issues or local files. Use a separate workflow/skill to apply push or pull after review.

## Prerequisites

- **Workspace:** Only projects under `workspace/projects/` are considered. See `standards/conventions.md` for workspace layout and phase conventions.
- **Jira:** Atlassian MCP server connected; Jira project key (default `TI`).
- **Skills:** Read and use `skills/engineering-management/workspace-epic-scanner/SKILL.md`, `skills/engineering-management/jira-epic-folder-matcher/SKILL.md`, `skills/engineering-management/sync-report-writer/SKILL.md`.

---

## Step 0: Scope (optional single project)

- If the user asked for **one specific project**, note the **project slug** (e.g. `omni-channel-learning-delivery-platform`). The report will:
  - Include only that project’s epic folders.
  - Be saved as `memory/reports/YYYY-MM-DD-HH-mm-ss-sync-report-<project-slug>.md`.
- Otherwise, include **all projects** in `workspace/projects/` and save as `memory/reports/YYYY-MM-DD-HH-mm-ss-sync-report.md`.

---

## Step 1: Get Jira Cloud ID

Call `getAccessibleAtlassianResources` and store the **cloudId** for all subsequent Jira MCP calls.

---

## Step 2: Scan workspace (workspace-epic-scanner)

Using **workspace-epic-scanner**:

1. List all **project** folders under `workspace/projects/` (directories only). If scope is a single project, keep only that slug.
2. For each project, find every **epic folder** (paths where `epic-summary.md` exists): `epics/`, `eng/epic/`, `eng/alpha/`, `eng/beta/`, `eng/ga/`, `eng/fast-follow/`.
3. For each epic folder, extract:
   - `project_slug`, `epic_folder_path`, `phase_or_epics`
   - Jira epic key from project folder name (if pattern `TI-NNNN-*`) and from `epic-summary.md` (e.g. `[TI-3613](...)` or "Jira Epic: TI-3613")
   - List of **local story files** (e.g. `story-*.md`, `TI-*-story-*.md`) and, when present, Jira story key from filename.

Produce a list of **epic folder entries** with the above. This is the scope for the rest of the workflow.

---

## Step 3: For each epic folder — match to Jira (jira-epic-folder-matcher)

For each epic folder from Step 2:

1. **Resolve Jira epic:** If we have a Jira epic key (from epic-summary or folder), fetch it with `getJiraIssue`. Otherwise search by epic title from `epic-summary.md` (JQL: `project = TI AND issuetype = Epic AND summary ~ "..."`). Confirm issue type is Epic.
2. **List Jira stories:** JQL `project = TI AND issuetype = Story AND parent = {epic_key}` (or equivalent "Epic Link" if needed). Fetch summary, status, updated, parent. Paginate if > 100.
3. **Match local ↔ Jira:** For each local story file, match by (a) Jira key in filename, or (b) title similarity to Jira summary. For each Jira story, mark if it has a matching local file or not.
4. **Classify:**
   - **Push to Jira — create:** Local story, no Jira issue.
   - **Push to Jira — update:** Local story + Jira issue, but status/points/ACs/description differ.
   - **In sync:** Local + Jira match, no material diff.
   - **Pull from Jira — create local:** Jira story, no local file.
   - **Pull from Jira — update local:** Jira story + local file, but Jira updated more recently or content differs.

Use the same **status mapping** as sync-compare-local-to-jira (To Do ↔ Open/Backlog, Done ↔ Done/Closed, Deferred ↔ Won't Do). For "Jira newer", compare Jira `updated` to file mtime and/or content diff.

Aggregate results per epic folder so the report writer can fill the tables.

---

## Step 4 (optional): Epics in Jira with no local folder

To "consider as much as possible": search Jira for epics that are **not** linked to any epic folder we scanned (e.g. recent TI epics). JQL example: `project = TI AND issuetype = Epic ORDER BY updated DESC` with `maxResults` 50. Exclude epic keys we already have from Step 2/3. Add a short list to the report: "Epics in Jira with no local folder" so the user can consider creating or linking a folder.

---

## Step 5: Write the report (sync-report-writer)

Using **sync-report-writer**:

1. Build the report body from the template in `skills/engineering-management/sync-report-writer/SKILL.md`: Summary table, then per-project/per-epic sections with tables for Push (create), Push (update), Pull (create local), Pull (update local), In sync. Optionally add "Epics in Jira with no local folder".
2. **Timestamp:** Current time in format `YYYY-MM-DD-HH-mm-ss` (e.g. `2026-03-11-14-30-00`).
3. **Filename:**
   - All projects: `memory/reports/YYYY-MM-DD-HH-mm-ss-sync-report.md`
   - Single project: `memory/reports/YYYY-MM-DD-HH-mm-ss-sync-report-<project-slug>.md`
4. Ensure **memory/reports/** exists; write the file.
5. Tell the user where the report was saved and that push/pull actions are **not** applied automatically — use the sync-local-to-jira workflow or a dedicated "pull from Jira" skill after review.

---

## Step 6: Suggest next steps

- For **Push to Jira:** "Run the **sync-local-to-jira** workflow for the epic folder(s) and stories listed under 'Push to Jira'."
- For **Pull from Jira:** "A separate skill/workflow can create or update local story files from Jira; run that after reviewing this report. This workflow does not perform pull automatically."

---

## References

- **Skills:** `skills/engineering-management/workspace-epic-scanner/SKILL.md`, `skills/engineering-management/jira-epic-folder-matcher/SKILL.md`, `skills/engineering-management/sync-report-writer/SKILL.md`
- **Compare (single epic folder):** `skills/engineering-management/workflow-sync-compare-local-to-jira/SKILL.md`
- **Push:** `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md`
- **Memory reports:** `memory/README.md`
