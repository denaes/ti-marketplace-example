---
name: sync-report-writer
description: >
  Template and rules for the workspace–Jira sync report (push vs pull, per project/epic/story). Use
  when generating the dated sync report file.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Sync Report Writer

## Purpose

Define the **structure and content** of the **Workspace ↔ Jira Sync Report** so every run produces a consistent, dated markdown file with clear actions: what to push to Jira, what to pull from Jira, and what is in sync — with granular details per project, epic, and story.

## When to Use

- When the **sync-workspace-jira-report** workflow has collected data (from workspace-epic-scanner and jira-epic-folder-matcher) and is ready to write the report
- When you need a human-readable, file-based report for "what needs to sync" without performing any automatic updates

## Output File

- **Path:** `memory/reports/YYYY-MM-DD-HH-mm-ss-sync-report.md`
- **Single-project variant:** If the user requested one project only: `memory/reports/YYYY-MM-DD-HH-mm-ss-sync-report-<project-slug>.md`
- **Timestamp:** Use current date/time at report generation time; format `YYYY-MM-DD-HH-mm-ss` (24h, zero-padded). Example: `2026-03-11-14-30-00-sync-report.md`

## Report Structure (Markdown)

Use the following sections. Fill from the workflow’s collected data.

```markdown
# Workspace ↔ Jira Sync Report

**Generated:** YYYY-MM-DD HH:mm
**Scope:** All projects in workspace/projects/  [or: Single project: <slug>]
**Jira project:** TI

---

## Summary

| Metric | Count |
|--------|--------|
| Projects scanned | N |
| Epic folders scanned | N |
| Stories to create in Jira | N |
| Stories to update in Jira | N |
| Stories in sync | N |
| Stories to create locally (Jira-only) | N |
| Stories to update locally (Jira newer) | N |
| Epics in Jira with no local folder | N (optional) |

---

## Per project and epic

(Repeat for each project and each epic folder.)

### Project: <project_slug>
**Epic folder:** `workspace/projects/<slug>/<path>`
**Jira epic:** TI-NNNN — <epic title> [or: Not linked / Not found]

#### Push to Jira (create)
| Local story file | Title | Notes |
|------------------|-------|-------|
| story-N-....md   | ...   | Create as Story under TI-NNNN |

#### Push to Jira (update)
| Local story file | Jira key | Title | Diff summary |
|------------------|----------|-------|--------------|
| TI-XXXX-story-....md | TI-XXXX | ... | Status, points, or ACs differ |

#### Pull from Jira (create local)
| Jira key | Title | Jira status | Notes |
|----------|-------|-------------|-------|
| TI-YYYY | ... | ... | No local file; create story file from Jira |

#### Pull from Jira (update local)
| Jira key | Local file | Title | Diff summary |
|----------|------------|-------|--------------|
| TI-YYYY | TI-YYYY-story-....md | ... | Jira updated more recently or content differs |

#### In sync
| Local file | Jira key | Title |
|------------|----------|-------|
| ... | ... | ... |

---

## Epics in Jira with no local folder (optional)

| Jira epic | Title | Story count | Note |
|-----------|-------|-------------|------|
| TI-NNNN | ... | N | Consider creating workspace folder or linking |

---

## Next steps

- **Push to Jira:** Use workflow `sync-local-to-jira.md` for the listed epic folders / stories.
- **Pull from Jira:** Use a separate skill/workflow (to be called after the report) to create or update local story files from Jira; this report does not perform updates.
```

## Conventions

- **Cross-references:** Use Jira keys (e.g. `TI-3927`) and relative paths from repo root. See `standards/conventions.md`.
- **No automatic updates:** This skill only defines the report content. The workflow that uses it must not create/update Jira issues or local files; that is a different workflow/skill to run after the user reviews the report.
- **Empty sections:** If a section has no rows (e.g. no "Pull from Jira (create local)"), still show the section header and write "None." or leave the table empty with a note "No items."

## References

- **Workflow:** `skills/engineering-management/workflow-sync-workspace-jira-report/SKILL.md`
- **Memory reports:** `memory/README.md` (report naming, delta)
- **Compare report:** `skills/engineering-management/workflow-sync-compare-local-to-jira/SKILL.md` (comparison dimensions, status mapping)
