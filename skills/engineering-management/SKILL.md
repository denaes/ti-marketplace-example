---
name: workspace-epic-scanner
description: >
  Discover all projects and epic folders under workspace/projects/ with paths and optional Jira epic
  key. Use when building a sync report or scanning the workspace for Jira alignment.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Workspace Epic Scanner

## Purpose

Produce a **structured list of all projects and epic folders** under `workspace/projects/`, so sync and compare workflows know what to align with Jira. Optionally filter to a single project when the user specifies one.

## When to Use

- When running the **sync-workspace-jira-report** workflow (to decide scope)
- When you need a full inventory of local epic folders for reporting or batch operations
- When the user asks for "all projects in workspace" or "epics under workspace/projects"

## Scope

- **Root:** `workspace/projects/` only. Do not include `_inbox`, `_references`, `_notes` (those live under `workspace/` but are not project folders).
- **Projects:** Every **directory** directly under `workspace/projects/` is a project (identified by its folder name = **project slug**). Examples: `omni-channel-learning-delivery-platform`, `c2-conversational-search`, `instance-cloning-provisioning`.
- **Epic folders:** For each project, find all folders that contain an **epic** (one `epic-summary.md` per folder). These are:
  - **Phase folders:** `workspace/projects/<slug>/eng/<phase>/` where `<phase>` is `alpha`, `beta`, `ga`, or `fast-follow` (see `docs/WORKSPACE-PHASES.md`). Only include phases that **exist** (have an `epic-summary.md`).
  - **Legacy single epic folder:** `workspace/projects/<slug>/epics/` or `workspace/projects/<slug>/eng/epic/` if present with `epic-summary.md`.

## Output Structure

For each epic folder, produce (or make available for the workflow):

| Field | Source |
|-------|--------|
| **project_slug** | Parent directory name under `workspace/projects/` |
| **epic_folder_path** | Full path relative to repo root, e.g. `workspace/projects/omni-channel-learning-delivery-platform/eng/beta` |
| **phase_or_epics** | Phase name (`alpha`, `beta`, `ga`, `fast-follow`) or `epics` / `epic` for legacy |
| **jira_epic_key_from_folder** | If the **project** folder name matches `TI-NNNN-*`, that prefix is the epic key; otherwise leave blank. (After push, project folder is renamed to `{EPIC_KEY}-<slug}` — but the epic folder is inside the project, so the key may be in the **project** name, not the phase subfolder.) |
| **jira_epic_key_from_epic_summary** | From `epic-summary.md`: extract any Jira epic key (e.g. `[TI-3613](url)` or "Jira Epic: TI-3613"). Prefer this when present. |

**Note on Jira key location:** The epic key may appear in (a) the **project folder** name, e.g. `TI-3556-endpoint-catalog-stories`, or (b) inside `epic-summary.md` (e.g. "**Epic (Jira):** [TI-3613](...)" or "**Jira Epic:** TI-3373"). Scan both. For phase-based layout, the same project can have multiple epic folders (alpha, beta, etc.); each may reference a different Jira epic in its `epic-summary.md`.

## How to Implement

1. **List project folders:** List direct children of `workspace/projects/` that are directories. Skip files (e.g. `README.md`). Each directory name = `project_slug`.
2. **Optional filter:** If the user requested a **single project**, keep only that slug (e.g. `omni-channel-learning-delivery-platform`).
3. **Find epic folders:** For each project, check:
   - `workspace/projects/<slug>/epics/epic-summary.md` (legacy)
   - `workspace/projects/<slug>/eng/epic/epic-summary.md` (legacy)
   - `workspace/projects/<slug>/eng/alpha/epic-summary.md`, `eng/beta/epic-summary.md`, `eng/ga/epic-summary.md`, `workspace/projects/<slug>/eng/fast-follow/epic-summary.md`
   Include only paths where `epic-summary.md` exists.
4. **Extract Jira epic key:** For each epic folder, read `epic-summary.md` and look for patterns: `[TI-NNNN](...)`, `TI-NNNN`, "Jira Epic:** TI-NNNN", "**Epic (Jira):** ... TI-NNNN". If the **project** folder name starts with `TI-` and digits, note that as `jira_epic_key_from_folder` for the project (can be used when the epic summary doesn’t name an epic).

## Story Files

For each epic folder, list story files for use by the sync workflow:

- **Pattern:** `story-*.md` or `TI-*-story-*.md` (after push). Exclude `epic-summary.md`, `README.md`, `HLD-*.md`, `comparison-report.md`, and other non-story files.
- **Jira key from filename:** If a story file is named `TI-3927-story-1-aeo-pages-catalog.md`, the Jira story key is `TI-3927`.

## References

- **Workspace layout:** See `standards/conventions.md` for workspace layout conventions.
- **Sync workflow:** `skills/engineering-management/workflow-sync-workspace-jira-report/SKILL.md`
- **Compare workflow:** `skills/engineering-management/workflow-sync-compare-local-to-jira/SKILL.md`
