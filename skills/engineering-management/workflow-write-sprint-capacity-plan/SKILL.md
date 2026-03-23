---
name: workflow-write-sprint-capacity-plan
description: >
  Sprint capacity planning — query Jira for sprint load, compare against team capacity, and generate
  a capacity report with assignment recommendations
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Sprint Capacity Plan

Generate a capacity report for active and upcoming sprints. Shows total load, per-pod breakdown, per-engineer allocation, over/under warnings, and unassigned work. Optionally recommends assignments.

## Prerequisites

- Atlassian MCP server connected (`mcp_atlassian_*` tools available)
- Preferences file exists at `skills/engineering-management/workflow-sprint-capacity-preferences/SKILL.md`
- Capacity-planning skill: `skills/engineering-management/capacity-planning/SKILL.md`

---

## Step 0: Load Preferences

Read the preferences file at `skills/engineering-management/workflow-sprint-capacity-preferences/SKILL.md`. Extract:

1. **Jira config** — Cloud ID, project key, board ID, pod custom field ID
2. **Team roster** — Engineer name, pod(s), capacity per sprint (SP), notes
3. **Default capacity** — SP for engineers not in the roster
4. **Sprint length** — days per sprint (for reference)
5. **Previous run history** — last run stats for delta comparison

Read the capacity-planning skill at `skills/engineering-management/capacity-planning/SKILL.md` for capacity math rules, pod mapping, and cross-pod handling.

If the preferences file doesn't exist, ask the user for the minimum config (board ID, team roster) and create it.

---

## Step 1: Get Jira Cloud ID

```
Tool: mcp_atlassian_getAccessibleAtlassianResources
```

---

## Step 2: Fetch Active and Upcoming Sprints

Query for sprints that are open or in the future:

```
Tool: mcp_atlassian_searchJiraIssuesUsingJql
cloudId: {from preferences}
jql: project = "{PROJECT_KEY}" AND sprint in openSprints()
fields: ["summary", "status", "assignee", "customfield_10037", "customfield_10020", "issuetype", "parent", "labels", "customfield_10138"]
maxResults: 100
```

Also query future sprints:

```
Tool: mcp_atlassian_searchJiraIssuesUsingJql
cloudId: {from preferences}
jql: project = "{PROJECT_KEY}" AND sprint in futureSprints()
fields: ["summary", "status", "assignee", "customfield_10037", "customfield_10020", "issuetype", "parent", "labels", "customfield_10138"]
maxResults: 100
```

If more than 100 results, paginate using `nextPageToken`.

Group all issues by sprint name.

---

## Step 3: Aggregate Sprint Data

For each sprint, compute:

### 3a. Sprint totals

- **Total issues** — count of all issues in the sprint
- **Total SP** — sum of story points (treat unestimated as 0, flag them)
- **By status** — SP in each status category (To Do, In Progress, Done)
- **Unestimated count** — issues with 0 or null story points

### 3b. Per-engineer breakdown

For each assignee in the sprint:

- **Assigned SP** — sum of their story points
- **Issue count** — number of issues assigned
- **Capacity (SP)** — from the team roster in preferences
- **Remaining SP** — capacity minus assigned SP
- **Status** — `OVER` if remaining < 0, `TIGHT` if remaining < 2, `OK` otherwise

### 3c. Per-pod breakdown

For each pod (from the issue's pod custom field or the engineer's pod in the roster):

- **Total SP** — sum of story points for issues in this pod
- **Pod capacity** — sum of capacity for all engineers in this pod
- **Remaining** — pod capacity minus total SP
- **Engineers** — list of engineers in this pod with their individual load

### 3d. Unassigned work

- List all issues with assignee = Unassigned or null
- Group by pod (if pod field is set) or "No Pod"
- Total unassigned SP

---

## Step 4: Compare Against Capacity

Using the team roster from preferences and the capacity math from the skill:

1. For each engineer: flag if assigned SP > capacity (OVER-ALLOCATED)
2. For each pod: flag if total assigned SP > pod capacity
3. For each sprint: flag if total SP > total team capacity
4. Identify engineers with significant remaining capacity (> 5 SP)

---

## Step 5: Generate the Report

Create the report with these sections:

### Section 1: Sprint Summary

| Sprint | State | Issues | Total SP | Estimated | Unestimated | Team Capacity | Remaining | Status |
|--------|-------|--------|----------|-----------|-------------|---------------|-----------|--------|

### Section 2: Per-Pod Breakdown

For each sprint, one table per pod:

| Pod | Engineers | Pod Capacity | Assigned SP | Remaining | Status |
|-----|-----------|-------------|-------------|-----------|--------|

### Section 3: Per-Engineer Allocation

For each sprint:

| Engineer | Pod | Capacity | Assigned SP | Remaining | Issues | Status |
|----------|-----|----------|-------------|-----------|--------|--------|

Flag rows with `OVER` or `TIGHT` status.

### Section 4: Unassigned Work

| Sprint | Key | Type | Summary | SP | Pod | Epic |
|--------|-----|------|---------|-----|-----|------|

### Section 5: Warnings and Recommendations

- List all over-allocated engineers with specific issues that could be reassigned
- List under-utilized engineers who could take on unassigned work
- Suggest assignments: match unassigned issues to available engineers by pod and remaining capacity
- Flag any unestimated issues that should be pointed before sprint planning

### Section 6: Delta (if previous run exists)

Compare current stats to the last run from preferences:

- Sprint load changes
- New issues added since last run
- Engineers whose allocation changed significantly

---

## Step 6: Present to User

Present the report to the user. Ask if they want to:

1. **Accept the report as-is** — save to `memory/reports/`
2. **Reassign issues** — for any recommended reassignments, offer to update Jira via MCP
3. **Move issues between sprints** — if a sprint is overloaded, offer to defer issues to the next sprint
4. **Update the roster** — if capacity or pod assignments need changing

**CRITICAL: Do NOT modify any Jira issues unless the user explicitly confirms each change.**

---

## Step 7: Save Report and Update Preferences

1. Save the report to `memory/reports/{YYYY-MM-DD}-sprint-capacity-report.md`
2. Update the preferences file with:
   - **Run history** — append date, sprint names, total SP, capacity utilization %
   - **Roster changes** — if the user updated any engineer's capacity or pod

---

## Step 8: Apply Changes (Optional)

If the user confirmed reassignments or sprint moves in Step 6:

For each reassignment:
```
Tool: mcp_atlassian_editJiraIssue
cloudId: {from preferences}
issueIdOrKey: {issue key}
fields:
  assignee:
    accountId: {new assignee account ID}
```

For sprint moves, update the sprint field on the issue.

Look up account IDs using:
```
Tool: mcp_atlassian_lookupJiraAccountId
cloudId: {from preferences}
query: {engineer display name}
```

---

## Output

The workflow produces:

1. **`{YYYY-MM-DD}-sprint-capacity-report.md`** — full capacity report in `memory/reports/`
2. **Updated `skills/engineering-management/workflow-sprint-capacity-preferences/SKILL.md`** — with run history and any roster changes
3. **(Optional) Jira updates** — reassignments or sprint moves if user confirmed

---

## Notes

- This workflow is **read-only against Jira by default** — it only modifies issues when the user explicitly confirms
- The Google Sheets capacity tool (`tools/capacity-sheets/`) provides the same data as a visual dashboard; this workflow is the conversational interface
- Cross-pod engineers: if an engineer works across pods, their capacity is split per the rules in the capacity-planning skill
- Unestimated issues are flagged but counted as 0 SP in totals — recommend estimating them before finalizing sprint plans
