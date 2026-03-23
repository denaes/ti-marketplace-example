---
name: workflow-write-prd
description: >
  From problem statement or brief to a TI PRD or Product Brief (template-aligned). Uses ti-write-prd,
  create-prd, deliver-prd.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Write PRD / Product Brief

Produce a TI-aligned PRD or Product Brief from a problem statement, outline, or rough brief. Output follows `templates/product/[TEMPLATE] Product Brief .md` (or PRD template) so it is ready for write-prd-assessment and write-epics-and-stories-from-prd.

## When to Use

- You have a problem statement, pitch, or rough brief and need a full PRD or Product Brief
- You want template-aligned output for the TI pipeline (assess → epics → Jira)
- You are drafting a new feature or product and need structure

## Prerequisites

- Input: problem statement, brief, or outline (paste, file path, or conversation)
- TI Product Brief template: `templates/product/[TEMPLATE] Product Brief .md`
- PRD template: `templates/product/Product Brief [TEMPLATE].md`
- Skills: `skills/product/product-execution/ti-write-prd/SKILL.md`, `skills/product/product-execution/create-prd/SKILL.md`, `skills/product/product-execution/deliver-prd/SKILL.md`, `skills/product/product-execution/prd-development/SKILL.md`, `skills/product/product-execution/ti-prd-okrs/SKILL.md` (optional)

## Step 1: Clarify scope and format

1. **Confirm with the user:** Product Brief vs PRD (Brief is the full template; PRD can be shorter). What product/feature name and phase (Alpha/Beta/GA)?
2. **Optional — OKRs:** Ask whether to **generate OKRs as part of the brief**. If yes, OKRs will be produced during the same generation pass and written as `06-okrs.md` in the project prd folder (see product-brief-multi-file rule). Uses `skills/product/product-execution/ti-prd-okrs/SKILL.md`.
3. **Gather:** Any existing bullets, requirements, or links the user has. If scope is vague, ask what is in/out of scope per `standards/conventions.md`.
4. **If the brief will include Staged Features & ACs:** Set the expectation that the user will be asked for scenario details (happy path, errors, branching) so acceptance criteria are testable.

## Step 2: Read reference materials

1. **TI Product Brief template** — `templates/product/[TEMPLATE] Product Brief .md` (sections, required fields)
2. **ti-write-prd skill** — `skills/product/product-execution/ti-write-prd/SKILL.md` (TI alignment, codebase references)
3. **create-prd / deliver-prd** — `skills/product/product-execution/create-prd/SKILL.md`, `skills/product/product-execution/deliver-prd/SKILL.md` (structure, quality bar)

## Step 3: Draft the document

1. Use **ti-write-prd** to produce a draft aligned with the Product Brief template and TI context (`ti/`, `ti/v3/`).
2. **Before or while drafting Staged Features & Acceptance Criteria:** Use the interactive requirements pass from ti-write-prd — ask the user for **happy path**, **non‑happy path** (errors, validation, permission denied), and **if-this-then-that** (e.g. Panorama, paywall, feature flags) for each epic/feature in scope. Use their answers to populate Detailed Requirements and Acceptance Criteria (no placeholder-only ACs).
3. Fill every required section from the template; use placeholders only where the user must supply input (call that out).
4. Optionally use **prd-development** or **create-prd** for specific sections (objectives, solution, release planning).
5. Apply **deliver-prd** expectations: clear acceptance criteria, testable outcomes, no TBD without follow-up.
6. **If OKRs were opted in (Step 1):** During the same brief generation pass, run **ti-prd-okrs** using the draft content (Project Summary, Product Opportunity including Success Criteria & Impact). Write the OKR output to `workspace/projects/<slug>/prd/06-okrs.md` and add a link to it in `00-index.md`. This makes OKRs part of the generated brief, not a separate follow-up step.

## Step 4: Polish and place output

1. Optionally run **grammar-check** (`skills/product/product-toolkit/grammar-check/SKILL.md`) on the draft.
2. Write the output to file(s). If generating multi-file: `workspace/projects/<slug>/prd/` with `00-index.md`, section files, and — if OKRs were opted in — `06-okrs.md`. If single-file: `workspace/_inbox/` or project folder; name e.g. `YYYY-MM-DD_<feature>-product-brief.md`.
3. Tell the user they can run **write-prd-assessment** next (or that the brief is already in `workspace/projects/<slug>/prd/` for the full pipeline).

## References

- Conventions: `standards/conventions.md`
- Assess PRD: `skills/product/product-execution/workflow-write-prd-assessment/SKILL.md` (next step after writing)
