---
name: workflow-write-epic-health-report
description: Weekly Innovation vs Maintenance epic health report — classifies Jira epics and tracks the 80/20 ratio target
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Epic Health Report

Generate a weekly Innovation vs. Maintenance classification report for all Jira epics, tracking progress toward the 80% Innovation / 20% Maintenance target.

## Prerequisites

- Atlassian MCP server connected (`mcp_atlassian_*` tools available)
- Preferences file exists at `skills/engineering-management/workflow-epic-health-report-preferences/SKILL.md`

---

## Step 0: Load Preferences & Previous Session

Read the preferences file at `skills/engineering-management/workflow-epic-health-report-preferences/SKILL.md`. Extract:

1. **Jira config** — Cloud ID, project key, lookback period
2. **KPI targets** — Innovation ratio, maintenance ratio, debt ratio
3. **Classification rules** — work-type, debt-type, strategic-initiative mappings
4. **User overrides** — sticky per-epic-key corrections from previous sessions
5. **Heuristics** — learned patterns for classifying new epics
6. **Previous run history** — last run stats for week-over-week comparison

If the preferences file doesn't exist, create it from the template and ask the user to confirm the configuration before proceeding.

---

## Step 1: Fetch Epics from Jira

// turbo
Get the Jira Cloud ID:

```
Tool: mcp_atlassian_getAccessibleAtlassianResources
```

Query all epics created in the lookback period (default: 6 months):

```
Tool: mcp_atlassian_searchJiraIssuesUsingJql
cloudId: {from preferences}
jql: issuetype = Epic AND created >= "{6 months ago}" ORDER BY created DESC
fields: ["summary", "status", "labels", "components", "priority", "created", "updated", "assignee", "description"]
maxResults: 100
```

If more than 100 results, paginate using `nextPageToken`.

---

## Step 2: Identify New vs. Known Epics

Compare fetched epics against the **User Overrides** table in preferences:

- **Known epics** (key exists in overrides) → apply the stored classification directly
- **New epics** (key not in overrides) → classify using the rules in Step 3
- **Canceled epics** (status = "Canceled") → exclude from stats, list separately

---

## Step 3: Classify New Epics

For each NEW epic not in the overrides table, apply classification using this priority:

### 3a. Check heuristics (from preferences)

Apply the learned patterns in order:

1. "Minor" / "Phase 1" / "Q1 -" prefix → `maintenance:enhancement`
2. "Improvements to" existing system → `maintenance:enhancement`
3. Regression / Observability / Monitoring for existing → `maintenance:keep-the-lights-on`
4. Usability / UX debt → `maintenance:enhancement`
5. Data "uplift" / tool migration → `maintenance:keep-the-lights-on`
6. V3 / NestJS / AI / Conversational Search / Omni-channel / Learning Agent / Starter SKU → `innovation:new-platform` or `innovation:new-feature`
7. AWS cost / InfoSec / Compliance / Component upgrades → `maintenance:keep-the-lights-on`
8. Design spikes for new products → `innovation:new-feature`
9. Panorama enhancements → `maintenance:enhancement` (unless clearly new capability with PRD/HLD)
10. "Consistent experience" / fixing inconsistencies → `maintenance:enhancement`

### 3b. If no heuristic matches

Classify based on the epic summary and description:

- Contains "new", "alpha", "beta", "GA", "pilot" for a new product/feature → `innovation:new-feature` or `innovation:new-product`
- Contains "architecture", "service", "platform", "foundation" → `innovation:new-platform`
- Contains "upgrade", "deprecation", "end of life", "cost" → `maintenance:keep-the-lights-on`
- Contains "bug", "regression", "fix", "incident" → `maintenance:bug-fix`
- Otherwise → flag for user review

### 3c. Flag uncertain classifications

If confidence is low, mark the epic with `⚠️ REVIEW` and ask the user to confirm during the review step.

---

## Step 4: Generate the Report

Create the report artifact at `~/.gemini/antigravity/brain/{conversation-id}/epic_classification_report.md` with:

### Section 1: Epic-by-Epic Classification

Two tables split by target:
- **🟢 Innovation Epics** — # / Key / Name / Work-Type / Reason
- **🔴 Maintenance Epics** — # / Key / Name / Work-Type / Reason
- **⛔ Canceled Epics** — Key / Name (excluded from stats)

### Section 2: Aggregate Statistics

- **Innovation vs. Maintenance ratio** with visual bar and gap-to-target
- **Innovation breakdown** by work-type (new-feature, new-platform, new-product, enhancement)
- **Maintenance breakdown** by work-type (keep-the-lights-on, enhancement, bug-fix)
- **Strategic initiative distribution** table
- **Technical debt analysis** — debt-type breakdown with ratio

### Section 3: Summary Scorecard

| KPI | Current | Target | Status | Δ vs. Last Week |
|-----|---------|--------|--------|-----------------|

### Section 4: Week-over-Week Trend (if previous run exists)

Compare current stats to the last run from preferences:
- Innovation ratio change
- New epics added since last run
- Epics that changed status since last run

### Section 5: New Epics Needing Review

List any epics flagged with `⚠️ REVIEW` for user confirmation.

---

## Step 5: Present to User for Review

Use `notify_user` to present the report. Ask the user to:

1. **Confirm or correct** any `⚠️ REVIEW` flagged epics
2. **Override** any classifications they disagree with

**CRITICAL: DO NOT apply any labels to Jira unless the user explicitly asks.**

---

## Step 6: Update Preferences with Session Results

After user confirms:

1. **Add new overrides** — for any corrections the user made, add rows to the "User Overrides" table
2. **Add new heuristics** — if the user's corrections reveal a new pattern, add it to the "Classification Heuristics" section
3. **Update run history** — append a new entry to "Previous Run History" with:
   - Run date
   - Period covered
   - Active epic count
   - Innovation / Maintenance counts and percentages
   - Debt ratio
   - Gap to target
   - Link to the report artifact

---

## Output

The workflow produces:
1. **`{YYYY-MM-DDTHH:MM:SS}-epic_classification_report.md`** — full report in the conversation artifacts directory
2. **Updated `skills/engineering-management/workflow-epic-health-report-preferences/SKILL.md`** — with new overrides, heuristics, and run history

---

## Notes

- This workflow is **read-only against Jira** — it never creates, updates, or labels issues
- Existing Jira labels (`Quick-Wins`, `UXdebt`, `InfoSec`, `technical_debt`) are preserved and noted but not modified
- The preferences file accumulates knowledge across sessions — the more you run it, the less manual correction is needed
- Run weekly to track progress toward the 80/20 Innovation/Maintenance target