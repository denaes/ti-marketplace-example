---
name: sync-reporting-category-from-sheet
description: >
  Sync the Reporting Category field in Jira from the ESC Metrics and Epics Ratio Google spreadsheet.
  Use when pushing Reporting category from the "Epics - Innovation vs Maint. ratio DATA" sheet to Jira
  (single epic or batch).
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Sync Reporting Category from Spreadsheet to Jira

## Purpose

Read **Reporting Category** from the ESC Metrics spreadsheet and write it to the corresponding Jira epic’s **Reporting Category** custom field (`customfield_10478`), so Jira stays aligned with the sheet used for innovation vs maintenance reporting.

## When to Use

- After updating Reporting category in the spreadsheet and needing Jira in sync
- When asked to “write Reporting category to Jira”, “sync sheet to Jira”, or “push Reporting category for TI-XXXX”
- For a single epic (e.g. verify with TI-3940) or for all epics listed in the sheet

## Prerequisites

- **Google Docs MCP** enabled and with read access to the spreadsheet
- **Jira (Atlassian) MCP** enabled with read/write on the TI project
- Spreadsheet must be shared with the Google Docs MCP’s identity if using a service account

## Constants

| Item | Value |
|------|--------|
| Spreadsheet ID | `1WpRIM23zf8FSBtUb37j5ybVMXxmxGs-jNsIbQ0btQfU` (from URL `/d/{id}/edit`) |
| Sheet name | `Epics - Innovation vs Maint. ratio DATA` (gid=2085197388) |
| Jira Reporting Category field | `customfield_10478` (text field) |
| Column Key | A (issue key, e.g. TI-3940) |
| Column Reporting Category | H (value to write to Jira) |

## Workflow

### 1. Get Jira cloud ID

Call **getAccessibleAtlassianResources** (no args). Use the returned `id` (e.g. `a0491fd7-7605-437a-bf79-b508a7c60f3b`) as `cloudId` for all Jira MCP calls. If the user’s link is `https://thoughtindustries.atlassian.net/...`, the hostname can sometimes be used as `cloudId`; if that fails, use the UUID from this call.

### 2. Read the spreadsheet

Call **readSpreadsheet** (Google Docs MCP):

- `spreadsheetId`: `1WpRIM23zf8FSBtUb37j5ybVMXxmxGs-jNsIbQ0btQfU`
- `range`: `Epics - Innovation vs Maint. ratio DATA!A1:H1000` (or a smaller range if only a subset is needed)

First row is headers: **Key**, Name, Status, Created, Target, Labels, Primary, **Reporting Category**. Column index 0 = Key, 7 = Reporting Category.

### 3. Build Key → Reporting Category map

From the returned `values` (array of rows), skip the header row. For each data row, use `row[0]` as issue key and `row[7]` as Reporting Category. Ignore rows where Key is empty or where Reporting Category is empty/placeholder (e.g. "—") unless the user explicitly wants to clear the field.

### 4. Update Jira

For each issue key to sync (single key or list):

- Call **editJiraIssue** (Atlassian MCP):
  - `cloudId`: from step 1
  - `issueIdOrKey`: e.g. `TI-3940`
  - `fields`: `{ "customfield_10478": "<Reporting Category value>" }`

Use the exact string from the sheet (e.g. `innovation:new-feature`, `maintenance:enhancement`). The field is a text field; no extra formatting needed.

### 5. Scope (single vs batch)

- **Single epic:** User says e.g. “only TI-3940” or “try with TI-3940”. Read the sheet, find the row where Key = TI-3940, then call editJiraIssue once with that key and its Reporting Category.
- **Batch:** Read the sheet, then loop over all rows (or a user-specified list of keys) and call editJiraIssue for each. Optionally report success/failure per key.

## Resolving the field ID

If `customfield_10478` ever changes or is unknown in another Jira instance:

1. Call **getJiraIssueTypeMetaWithFields** with `cloudId`, `projectIdOrKey`: `TI`, and the Epic `issueTypeId` (e.g. `10000`).
2. Search the returned metadata for a field whose `name` is **"Reporting Category"** and note its `key` (e.g. `customfield_10478`).

## References

- **Spreadsheet:** [ESC Metrics and Epics Ratio](https://docs.google.com/spreadsheets/d/1WpRIM23zf8FSBtUb37j5ybVMXxmxGs-jNsIbQ0btQfU/edit?gid=2085197388) — tab “Epics - Innovation vs Maint. ratio DATA”
- **Jira field:** Reporting Category = `customfield_10478` (TI project)
- **Sync/reporting workflows:** `skills/engineering-management/workflow-sync-workspace-jira-report/SKILL.md`, `.agents/workflows/write-report.md`
