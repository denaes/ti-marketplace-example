---
name: capacity-planning
description: >
  Capacity math, pod mapping, and cross-pod rules for sprint planning. Use when computing sprint
  load, recommending assignments, or checking capacity after pushing stories to Jira.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Capacity Planning

## Purpose

Provide the rules and formulas for computing sprint capacity, per-engineer load, and per-pod allocation. Referenced by the `sprint-capacity-plan` workflow and optionally by `push-to-jira` and `create-story` when checking whether a sprint or engineer is over-allocated.

## When to Use

- Running the **sprint-capacity-plan** workflow
- After **push-to-jira** — to warn if the target sprint is overloaded
- During **create-story** — to suggest an assignee based on available capacity
- Any time the user asks about sprint load, team capacity, or who is available

## Data Sources

| Data | Source | Location |
|------|--------|----------|
| Team roster (engineer, pod, capacity) | Preferences file | `skills/engineering-management/workflow-sprint-capacity-preferences/SKILL.md` |
| Issue data (SP, assignee, sprint, status) | Jira via MCP | `mcp_atlassian_searchJiraIssuesUsingJql` |
| Visual dashboard + structured data | Google Sheets via MCP | `tools/capacity-sheets/` (setup in README) |

**Data filter:** Issues are scoped to `project = TI` with pods matching the configured filter (see preferences). Infrastructure work lives in TI tickets with the Infrastructure pod set. This applies to both the Google Sheets sync and the Cursor workflow.

### Google Sheets MCP — `_index` lookup pattern

The R&D Capacity Planning spreadsheet has a `_index` sheet that maps logical keys to exact A1-notation ranges. This lets you read specific sprint data in two targeted calls instead of scanning the full Roadmap (2000+ rows).

**Step 1 — Read the index:**

```
readSpreadsheet(spreadsheetId: "<id>", range: "_index!A:H")
```

To get the spreadsheet ID, read the `_index` row where Key = `spreadsheet_id` (column C has the ID). Or use `listSpreadsheets(query: "R&D Capacity Planning")` to discover it.

**Step 2 — Find the key you need:**

| To get… | Look for Key = |
|---------|----------------|
| Active sprint issues + capacity | `roadmap/sprint_<N>` where Sprint State = `ACTIVE` |
| Next sprint (future) | `roadmap/sprint_<N>` where Sprint State = `FUTURE` (first one) |
| Backlog | `roadmap/backlog` |
| Team roster + capacity | `users` |
| All sprint metadata | `sprints` |
| All issues (raw) | `issues` |
| DevEsc sprint | `devesc_roadmap/sprint_<N>` |

**Step 3 — Read the target range:**

```
readSpreadsheet(spreadsheetId: "<id>", range: "<value from column C>")
```

**Example — get the active sprint:**

1. `readSpreadsheet(id, "_index!A:H")` → find row where D = `ACTIVE`
2. That row's C column = `Roadmap!A45:R92` → `readSpreadsheet(id, "Roadmap!A45:R92")`

This returns the sprint header, capacity summary, progress, issue rows, and engineer availability — everything needed for capacity analysis.

**When to use Sheets MCP vs Jira MCP:**

| Need | Use |
|------|-----|
| Sprint capacity overview (load vs capacity, engineer status) | Sheets MCP via `_index` |
| Specific issue details, transitions, comments | Jira MCP |
| Team roster and capacity numbers | Sheets MCP (`users` key) |
| Issue search by JQL | Jira MCP |
| Per-sprint issue list with LOE breakdown | Sheets MCP via `_index` |

See `tools/capacity-sheets/SHEET-SCHEMA.md` for full column layouts of each sheet.

## Capacity Math

### Per-engineer capacity (by role)

Capacity is tracked per role. Each engineer has five capacity buckets:

```
Remaining Fullstack SP = Fullstack Capacity - Assigned Dev LOE
Remaining SRE SP       = SRE Capacity       - Assigned SRE work (story points on infra/ops issues)
Remaining DE SP        = DE Capacity        - Assigned DE work (story points on data engineering issues)
Remaining QA SP        = QA Capacity        - Assigned Testing LOE
Remaining UX SP        = UX Capacity        - Assigned UX LOE (or SP on UX-tagged issues)
```

- **Fullstack / SRE / DE / QA / UX Capacity** — from the team roster in preferences
- **Assigned Dev LOE** — sum of `customfield_10066` (Est Dev LOE) on assigned issues
- **Assigned Testing LOE** — sum of `customfield_10067` (Est Testing LOE) on assigned issues
- **Assigned UX LOE** — sum of `customfield_10412` (Est UX LOE) on assigned issues; or SP on UX-pod issues when no LOE breakdown
- **Story Points** (`customfield_10037`) — overall effort; used for sprint-level totals
- **Unestimated issues** — count as 0 but flag them; they represent hidden load

For engineers who do multiple roles (e.g., a fullstack dev who also does some QA), their capacity is the sum across all role buckets.

### Allocation status

| Remaining SP | Status | Meaning |
|-------------|--------|---------|
| < 0 | `OVER` | Engineer has more work than capacity allows |
| 0–2 | `TIGHT` | Engineer is near capacity; avoid adding more |
| 3–5 | `OK` | Some room but limited |
| > 5 | `AVAILABLE` | Engineer can take on more work |

### Per-pod capacity

```
Pod Fullstack Cap = SUM(Fullstack SP for all engineers in this pod)
Pod SRE Cap       = SUM(SRE SP for all engineers in this pod)
Pod DE Cap        = SUM(DE SP for all engineers in this pod)
Pod QA Cap        = SUM(QA SP for all engineers in this pod)
Pod UX Cap        = SUM(UX SP for all engineers in this pod)
Pod Dev Assigned  = SUM(Est Dev LOE on issues in this pod)
Pod QA Assigned   = SUM(Est Testing LOE on issues in this pod)
Pod UX Assigned   = SUM(Est UX LOE on issues in this pod)
```

For pod assignment on an issue, use this priority:
1. The issue's **pod custom field** value (if set)
2. The **assignee's pod** from the team roster (if assigned)
3. The **parent epic's pod** (if the epic has a pod field)
4. `"No Pod"` — flag for triage

### Capacity type → Pod mapping

| Capacity type | Pods it covers | Jira LOE field |
|---|---|---|
| **Fullstack** | Pod 1, Pod 2, Architecture, LVA, LP | Est Dev LOE (`customfield_10066`) |
| **SRE** | Infrastructure | Story Points on infra issues |
| **DE** | Data Engineering | Story Points on DE issues |
| **QA** | All pods (cross-cutting) | Est Testing LOE (`customfield_10067`) |
| **UX** | UX | Est UX LOE (`customfield_10412`) or SP on UX-tagged issues |

When computing pod-level capacity:
- **Pod 1 / Pod 2 / Architecture / LVA / LP** — sum Fullstack Capacity from engineers in that pod
- **Infrastructure** — sum SRE Capacity from engineers in that pod
- **Data Engineering** — sum DE Capacity from engineers in that pod
- **UX** — sum UX Capacity from engineers in that pod
- **QA capacity** is cross-cutting: sum QA Capacity across all engineers regardless of pod, then compare against total Est Testing LOE in the sprint

### Per-sprint capacity

```
Sprint Fullstack Cap = SUM(Fullstack SP for all engineers in this sprint)
Sprint SRE Cap       = SUM(SRE SP for all engineers in this sprint)
Sprint DE Cap        = SUM(DE SP for all engineers in this sprint)
Sprint QA Cap        = SUM(QA SP for all engineers in this sprint)
Sprint UX Cap        = SUM(UX SP for all engineers in this sprint)
Sprint Total Load    = SUM(Story Points for all issues in this sprint)
Sprint Dev Load      = SUM(Est Dev LOE for all issues in this sprint)
Sprint QA Load       = SUM(Est Testing LOE for all issues in this sprint)
Sprint UX Load       = SUM(Est UX LOE for all issues in this sprint)
```

## Cross-Pod Engineers

Some engineers work across multiple pods. Handle this as follows:

1. In the team roster, list all pods comma-separated: `Content, Platform`
2. Add a note with the split: `split 8/5` (meaning 8 SP to Content, 5 SP to Platform)
3. When computing pod capacity:
   - If a split is specified, allocate that many SP to each pod
   - If no split is specified, divide capacity equally across listed pods
4. When computing the engineer's personal remaining SP, use their **total** capacity regardless of pod split
5. When recommending assignments, prefer matching the engineer's primary pod (first listed)

### Example

> Bob: Pods = "Content, Platform", Capacity = 13, Notes = "split 8/5"
>
> - Content pod gets 8 SP of Bob's capacity
> - Platform pod gets 5 SP of Bob's capacity
> - Bob's personal remaining = 13 - (all his assigned SP across both pods)

## Unestimated Issues

Issues with 0 or null story points are **not counted** in SP totals but are **flagged** in the report:

- List them in a separate "Unestimated" section
- Recommend estimating before finalizing sprint plans
- If the user asks to count them, use the team's average SP per issue as a rough estimate

## Assignment Recommendations

When suggesting assignments for unassigned issues:

1. **Filter** — only consider engineers with status `OK` or `AVAILABLE`
2. **Match pod** — prefer engineers whose pod matches the issue's pod
3. **Sort by remaining SP** — assign to the engineer with the most remaining capacity
4. **Respect cross-pod** — a cross-pod engineer can take work from any of their listed pods
5. **Cap recommendations** — don't recommend assigning more SP than the engineer's remaining capacity
6. **Present, don't apply** — always show recommendations and wait for user confirmation

## Integration with Other Workflows

### push-to-jira

After pushing stories, the workflow can optionally check capacity:

1. Identify which sprint the stories were assigned to
2. Query current sprint load
3. If the sprint is now over capacity, warn the user with a summary table
4. Reference: `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md`

### create-story

When the user specifies an assignee or asks "who should work on this":

1. Load the team roster
2. Query the target sprint's current load
3. Suggest the engineer with the most remaining capacity in the matching pod
4. Reference: `skills/engineering-management/workflow-write-story/SKILL.md`

## References

- **Workflow:** `skills/engineering-management/workflow-write-sprint-capacity-plan/SKILL.md`
- **Preferences:** `skills/engineering-management/workflow-sprint-capacity-preferences/SKILL.md`
- **Google Sheets tool:** `tools/capacity-sheets/` (README, Code.gs, SHEET-SCHEMA.md)
- **Jira labels/metadata:** `skills/engineering-management/jira-labels-and-metadata/SKILL.md`
