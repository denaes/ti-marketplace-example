---
name: workflow-write-hld-and-epics-from-product-brief
description: >
  Product gave you a Product Brief; run codebase check → HLD → generate epics and stories in one
  flow. Optional: stop before sync-local-to-jira for review.
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Product Brief → HLD → Epics and Stories

Single flow for when **Product hands you a Product Brief**: (1) check current state in the codebase, (2) write or update the HLD, (3) generate epics and stories. Optionally **do not push to Jira** so you can verify everything first.

## Prerequisites

- A **Product Brief** (markdown) — path or @-reference
- **TI codebase** (`ti/`, `ti/v3/`) available for search (codebase-first)
- Access to **ti-write-hld** and **write-epics-and-stories-from-prd** (skills and workflow)

---

## Step 0: Clarify scope and output location

1. **Confirm** the Product Brief file and that you are acting as **ti-em** (tech lead).
2. **Ask if unclear:** Scope (GA vs Fast Follow, phases), priorities (which requirements are P0), and whether to **push to Jira** at the end (default: no — user verifies first).
3. **Output location:** Use the **phase-based workspace structure** (`docs/WORKSPACE-PHASES.md`):
   - **HLD:** `workspace/projects/<slug>/eng/HLD-<name>.md` (one per project/feature; high level, all phases)
   - **Epics and stories:** One epic per phase in `workspace/projects/<slug>/eng/<phase>/` (`alpha/`, `beta/`, `ga/`, `fast-follow/`). Each phase folder contains `epic-summary.md` and `story-*.md`.
   - If the project already exists with a single `eng/epic/` or `epics/` layout, keep using it until migrated or user asks for phase folders.

Derive **slug** from the Product Brief name. Create `workspace/projects/<slug>/` with `product/brief/`, `product/`, `eng/`, and for each release phase in the brief create `eng/<phase>/`.

---

## Step 1: Ingest Product Brief and check codebase

1. **Read** the Product Brief fully. Extract: goal, phases (Alpha/Beta/GA), requirements table, non-goals, metrics/instrumentation.
2. **Search the codebase** (`ti/`, `ti/v3/`) for the areas the brief touches:
   - Recent deployments, existing modules, endpoints, patterns (see `skills/engineering-management/workflow-write-epics-and-stories-from-prd/SKILL.md` Step 3b).
   - Surface **current state** to the user: what exists today, how it works, what patterns apply. See `standards/conventions.md` (Codebase-first).
3. **Optional:** If scope or priorities are unclear, **ask the user** before writing the HLD. Do not assume. See `standards/conventions.md` (Ask before deciding).

---

## Step 2: Write or update the HLD

1. **Read** the HLD template: `templates/product/[TEMPLATE] HLD.md` (or the TI HLD template referenced in `skills/engineering-management/ti-write-hld/SKILL.md`).
2. **Apply** the **ti-write-hld** skill (`skills/engineering-management/ti-write-hld/SKILL.md`):
   - Executive summary, Strangler plan, Proposed architecture, Options analysis, Engineering recommendation, Anti-regression & QA, Data & infrastructure, Security & compliance.
   - Use codebase search results so the HLD reflects **current state** and migration path.
3. **Save** the HLD under the project folder:
   - **Target structure:** `workspace/projects/<slug>/eng/HLD-<feature-name>.md`
   - **Legacy:** `workspace/projects/<slug>/epics/HLD-<feature-name>.md`

---

## Step 3: Generate epics and stories (no Jira push unless requested)

1. **Run** the **write-epics-and-stories-from-prd** workflow (`skills/engineering-management/workflow-write-epics-and-stories-from-prd/SKILL.md`):
   - **Input:** The same Product Brief; output is **per phase** into `workspace/projects/<slug>/eng/<phase>/` (alpha, beta, ga, fast-follow).
   - Follow its steps: reference materials, ingest PRD, validate DoR, codebase search (already done in Step 1 — reuse), define one epic per phase, write epic-summary.md and story files into each phase folder.
2. **Do not run sync-local-to-jira** unless the user explicitly asked to push. Tell the user that stories are ready for review and they can run **sync-local-to-jira** when ready.

---

## Step 4: Confirm and hand off

Report to the user:

- **HLD** path and one-line summary (scope, strangler, main recommendation).
- **Phase epics** created: for each phase folder (e.g. `eng/alpha/`, `eng/beta/`), epic-summary path and story count (and total story points).
- **Sample stories** created (e.g. [DESIGN], first few [BE]/[FE]/[QA]) per phase.
- **Next step:** Review HLD and phase epics; when satisfied, run **sync-local-to-jira** for the desired phase(s).

---

## Reference

- **HLD skill:** `skills/engineering-management/ti-write-hld/SKILL.md`
- **Generate epics and stories:** `skills/engineering-management/workflow-write-epics-and-stories-from-prd/SKILL.md`
- **Push to Jira (when ready):** `skills/engineering-management/workflow-sync-local-to-jira/SKILL.md`
- **Workspace structure (target):** `docs/WORKSPACE-PHASES.md` and `.agents/workflows/guide-me-to-wrap-up-session.md` (phase-based: eng/<phase>/)
