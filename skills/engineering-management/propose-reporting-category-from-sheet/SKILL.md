---
name: propose-reporting-category-from-sheet
description: >
  Propose Reporting Category values for epics that have an empty Reporting Category in the ESC
  Metrics spreadsheet. Reads the sheet, finds empty cells, and suggests a category per
  docs/reporting-epic-categories.md heuristics. Use when filling in missing Reporting categories or
  "suggest categories for empty rows".
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Propose Reporting Category from Sheet (Empty Rows)

## Purpose

For rows in the **Epics - Innovation vs Maint. ratio DATA** sheet where **Reporting Category** is empty or "—", propose a value using the heuristics in `docs/reporting-epic-categories.md`. The user can then review, edit the sheet, and optionally run **sync-reporting-category-from-sheet** to push to Jira.

## When to Use

- When asked to "propose Reporting category for empty rows", "suggest categories for the sheet", or "fill in missing Reporting category"
- Before or after a sync: identify epics that still need a category and get suggestions
- Does **not** write to the sheet or Jira; output is a proposal table for the user

## Prerequisites

- **Google Docs MCP** enabled with read access to the spreadsheet
- Read **`docs/reporting-epic-categories.md`** for the heuristics (work-type tags, debt-type, initiatives, and the ordered list of rules for suggesting a category)

## Constants (same as sync skill)

| Item | Value |
|------|--------|
| Spreadsheet ID | `1WpRIM23zf8FSBtUb37j5ybVMXxmxGs-jNsIbQ0btQfU` |
| Sheet name | `Epics - Innovation vs Maint. ratio DATA` (gid=2085197388) |
| Column Key | A (index 0) |
| Column Name | B (index 1) — used for heuristics |
| Column Reporting Category | H (index 7) |

## Workflow

### 1. Read the heuristics

Read **`docs/reporting-epic-categories.md`**. Use the section **"Heuristics for suggesting a category (new epics)"**: apply the rules **in order** (1 → 15). The first rule that matches the epic **Name** determines the suggested tag (e.g. `maintenance:enhancement`, `innovation:new-feature`). If none match, suggest **REVIEW** (user chooses).

### 2. Read the spreadsheet

Call **readSpreadsheet** (Google Docs MCP):

- `spreadsheetId`: `1WpRIM23zf8FSBtUb37j5ybVMXxmxGs-jNsIbQ0btQfU`
- `range`: `Epics - Innovation vs Maint. ratio DATA!A1:H1000`

Headers: Key, Name, Status, Created, Target, Labels, Primary, Reporting Category. Data: `row[0]` = Key, `row[1]` = Name, `row[7]` = Reporting Category.

### 3. Find rows with empty Reporting Category

Skip the header row. For each data row: if **Reporting Category** (`row[7]`) is empty, or is the placeholder "—", then the row needs a proposal. Ignore rows that already have a non-empty category (e.g. `innovation:new-feature`).

### 4. Propose a category per row

For each row with empty Reporting Category:

- Take the epic **Name** (`row[1]`).
- Apply the heuristics from `docs/reporting-epic-categories.md` **in order** (rule 1, then 2, … then 15).
- Assign the **first matching** tag (e.g. `maintenance:enhancement`, `innovation:new-feature`, `maintenance:keep-the-lights-on`). If no rule matches, use **REVIEW**.
- Optionally note the rule number or a short reason (e.g. "Minor prefix → maintenance:enhancement").

### 5. Output a proposal table

Produce a markdown table for the user, for example:

| Key | Name | Proposed Reporting Category | Reason |
|-----|------|-----------------------------|--------|
| TI-XXXX | Epic title… | maintenance:enhancement | Minor / Phase 1 prefix |
| TI-YYYY | Other title… | REVIEW | No heuristic matched |

Add a short summary: how many rows had empty category, how many got a suggestion vs REVIEW. Remind the user they can paste these into the sheet and then run **sync-reporting-category-from-sheet** to push to Jira (TI project only).

## Heuristics quick reference (from docs)

Apply in this order; first match wins:

1. "Minor" / "Phase 1" / "Q1 -" prefix → `maintenance:enhancement`
2. "Improvements to" existing system → `maintenance:enhancement`
3. Regression / Observability / Monitoring for existing → `maintenance:keep-the-lights-on`
4. Usability / UX debt → `maintenance:enhancement`
5. Data "uplift" / tool migration → `maintenance:keep-the-lights-on`
6. V3 / NestJS / AI / Conversational Search / Omni-channel / Learning Agent / Starter SKU → `innovation:new-platform` or `innovation:new-feature`
7. AWS cost / InfoSec / Compliance / Component upgrades → `maintenance:keep-the-lights-on`
8. Design spikes for new products → `innovation:new-feature`
9. Panorama enhancements → `maintenance:enhancement` (unless clearly new capability)
10. "Consistent experience" / fixing inconsistencies → `maintenance:enhancement`
11. "new", "alpha", "beta", "GA", "pilot" for new product/feature → `innovation:new-feature` or `innovation:new-product`
12. "architecture", "service", "platform", "foundation" → `innovation:new-platform`
13. "upgrade", "deprecation", "end of life", "cost" → `maintenance:keep-the-lights-on`
14. "bug", "regression", "fix", "incident" → `maintenance:bug-fix`
15. Otherwise → **REVIEW**

Use the **full text** in `docs/reporting-epic-categories.md` for nuance (e.g. initiative tags, debt-type).

## References

- **Heuristics and tag list:** `docs/reporting-epic-categories.md`
- **Spreadsheet:** [ESC Metrics and Epics Ratio](https://docs.google.com/spreadsheets/d/1WpRIM23zf8FSBtUb37j5ybVMXxmxGs-jNsIbQ0btQfU/edit?gid=2085197388) — tab "Epics - Innovation vs Maint. ratio DATA"
- **Push to Jira after editing sheet:** `skills/engineering-management/sync-reporting-category-from-sheet/SKILL.md`
