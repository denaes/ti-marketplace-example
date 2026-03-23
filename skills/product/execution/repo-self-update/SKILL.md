---
name: repo-self-update
description: >
  Add or update skills, workflows, and rules in this repo and keep Cursor, Antigravity, and Claude in
  sync. Use when adding a skill, adding a workflow, registering a new command, or when the user says
  "add a skill", "add workflow", "sync repo", "update catalog", or "make skills visible everywhere".
metadata:
  type: skill
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Repo self-update: add skills, workflows, sync catalog

Use this skill when adding or changing skills, workflows, or rules so that Cursor, Antigravity, and the orbit catalog stay in sync.

## Adding a new skill

1. **Create the skill folder** — e.g. `skills/product/<skill-name>/`, `skills/engineering-management/<skill-name>/`, or `skills/engineering/<skill-name>/`.
2. **Add `SKILL.md`** — YAML frontmatter with `name` and `description`; body with instructions. See existing skills in `skills/product/` or `skills/engineering-management/` for format.
3. **Run sync** — Follow the workflow **Sync repo: skills and catalog** (`.agents/workflows/sync-repo-skills-and-catalog.md`):
   - Run `python3 catalog/generate-catalog.py` from repo root.
   - Verify `.cursor/skills` and `.agent/skills` symlinks.
   - If you added a workflow, update `.cursor/rules/prd-jira-workflows.mdc` workflow table.

## Adding a new workflow (root)

1. **Create the workflow file** — `.agents/workflows/<workflow-name>.md` with YAML frontmatter (`description`) and step-by-step instructions.
2. **Register it in Cursor** — Add one row to the workflows table in `.cursor/rules/prd-jira-workflows.mdc` (task, workflow file, "Use when").
3. **Optional:** Update `docs/SOURCE-OF-TRUTH.md` if the workflow introduces new paths or conventions.

## Adding a new Cursor rule

1. **Create the rule** — `.cursor/rules/<name>.mdc` with YAML frontmatter (`description`, optional `globs`, `alwaysApply`).
2. **Optional:** Mention the rule in `docs/SOURCE-OF-TRUTH.md` under "Workflows and rules".

## Syncing after changes

Whenever you add or edit skills, commands, or workflows:

- **Quick sync (add-only):** Run **sync-repo-skills-and-catalog** or at least `python3 catalog/generate-catalog.py` and verify symlinks.
- **Full sync (add, update, or delete):** Run **Sync project meta** (`.agents/workflows/sync-project-meta.md`). It reconciles workflow/skill tables, SOURCE-OF-TRUTH, catalog, symlinks, and templates so nothing is stale after a deletion or rename.

## Reference

- **Full sync (recommended after any structural change):** `.agents/workflows/sync-project-meta.md`
- **Quick sync:** `.agents/workflows/sync-repo-skills-and-catalog.md`
- **Source of truth:** `docs/SOURCE-OF-TRUTH.md`
- **End-of-session (wrap + update rules):** `.agents/workflows/guide-me-to-wrap-up-session.md`
