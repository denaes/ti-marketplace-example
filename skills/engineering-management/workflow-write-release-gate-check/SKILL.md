---
name: workflow-write-release-gate-check
description: Check if an epic is ready for Alpha/Beta/GA per defined gates. Uses release-milestone-gates, epic-summary-writer (read).
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Release gate check

Evaluate whether an epic meets the criteria for a given phase gate (Alpha, Beta, GA). Produces a pass/fail or gap list so the team knows what is missing before release.

## When to Use

- You are planning a release and need to know if an epic is "done" for Alpha, Beta, or GA
- You want to avoid "almost done" surprises by checking required story types and dependency order
- You are defining or auditing phase gates for a product

## Prerequisites

- An epic folder with `epic-summary.md` and story files. This is either a **phase folder** (`workspace/projects/<slug>/eng/<phase>/`, e.g. `eng/alpha/`) or a single epic folder (`eng/epic/`, `epics/`). See `docs/WORKSPACE-PHASES.md`.
- Skill: `skills/engineering-management/release-milestone-gates/SKILL.md`; reference `skills/engineering-management/epic-summary-writer/SKILL.md` for epic structure

## Step 1: Clarify target phase

1. **Confirm with the user:** Which gate? (Alpha / Beta / GA) and (if relevant) which product or release name.
2. **Read** release-milestone-gates: definition of Alpha, Beta, GA; required story types before each gate; dependency ordering expectations.

## Step 2: Read the epic

1. **Read** `epic-summary.md`: phase, stories table (tag, status, points), total points, dependency graph.
2. **Read** each story file (or a representative set) to see which story types exist and their status (To Do / Done / Deferred).

## Step 3: Evaluate against the gate

1. For the chosen phase (Alpha/Beta/GA), apply the **required story types** from release-milestone-gates:
   - Alpha: [RESEARCH] done if any; [DESIGN], [DB] done; [BE], [FE] for scope done; [SEC], [FF] for feature done or N/A; at least one [QA] happy path.
   - Beta: Alpha + [QA] E2E main flows; [LOG], [ALERT] for new surface; [DOCS] minimal user-facing.
   - GA: Beta + [DOCS] complete; [PERF]/[OPS] as per DoR; no blocking bugs.
2. Check **dependency order**: no story in "Done" that is blocked by a story still "To Do". Use dependency-mapper logic if needed.
3. Produce a **gap list**: missing story types, stories still To Do that are required, or dependency violations.

## Step 4: Report and next steps

1. Write a short report: **Ready / Not ready** for [Phase], with bullet list of gaps (or "No gaps").
2. Optionally suggest concrete stories or tasks to close gaps (e.g. "Add [QA] E2E for flow X", "Complete [SEC] story TI-XXXX").
3. Save to the epic folder, e.g. `release-gate-check-<phase>.md`. No timestamp prefix; Git versions the file.

## References

- Release gates: `skills/engineering-management/release-milestone-gates/SKILL.md`
- Epic summary: `skills/engineering-management/epic-summary-writer/SKILL.md`
- Conventions: `standards/conventions.md`
