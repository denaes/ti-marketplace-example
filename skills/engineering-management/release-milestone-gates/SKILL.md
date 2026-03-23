---
name: release-milestone-gates
description: >
  What "done" means per phase (Alpha/Beta/GA); which story types are required before a gate;
  dependency ordering. Use when planning releases or defining epic phases.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Release Milestone Gates

## Purpose

Define **what "done" means** per phase (Alpha, Beta, GA) and **which story types** are required before passing a gate, plus **dependency ordering**, so releases have clear criteria and fewer "almost done" surprises.

## When to Use

- When **planning a release** or defining epic phases in generate-epics-and-stories
- When setting **epic phase** (Alpha/Beta/GA) and checking readiness
- When answering "can we ship Alpha?" for an epic

## Phase Definitions (typical)

| Phase | Meaning | Typical gates |
|-------|---------|----------------|
| **Alpha** | Internal or limited rollout; core path works; known gaps OK. | Core [BE]/[FE] done; [DESIGN]/[DB] done; [SEC] and [FF] for the feature done or N/A; [QA] smoke / critical path. |
| **Beta** | Broader rollout; quality and observability in place. | Alpha gates + [QA] E2E for main flows; [LOG]/[ALERT] for new surface; [SEC] and [FF] complete; [DOCS] user-facing. |
| **GA** | General availability; support and compliance in place. | Beta gates + [DOCS] final; [PERF]/[OPS] as needed; no known P0/P1; compliance sign-off if required. |

Adjust per product (e.g. "Alpha = dogfood only" vs "Alpha = first customer pilot").

## Required Story Types Before Gate

Before marking an epic "done" for a phase:

- **Alpha:** [RESEARCH] (if any) done; [DESIGN] and [DB] done; [BE] and [FE] for scope done; [SEC] and [FF] for this feature done or explicitly N/A; at least one [QA] covering the happy path.
- **Beta:** All Alpha + [QA] E2E for main flows; [LOG] and [ALERT] for new components; [DOCS] minimal user-facing.
- **GA:** All Beta + [DOCS] complete; [PERF]/[OPS] as per DoR; no blocking bugs.

See `jira_architect` for the "Required 14" story types; not every epic has all 14, but the ones that apply to the scope must be done or N/A before the gate.

## Dependency Ordering

- Stories must be **ordered** so that dependencies are done before dependents (see `dependency-mapper`).
- **Phase ordering:** Typically [RESEARCH] → [DESIGN] → [DB] → [BE]/[FE] (parallel where possible) → [SEC], [FF] → [QA] → [LOG], [ALERT], [DOCS], [PERF], [OPS]. Epic-summary and story "Depends on" should reflect this.

## Epic Summary and Phase

In **epic-summary.md**, set **Phase** to Alpha, Beta, or GA. Use this skill when generating or updating that field and when checking readiness for a release.

## References

- **Epic summary:** `skills/engineering-management/epic-summary-writer/SKILL.md`
- **Dependencies:** `skills/engineering-management/dependency-mapper/SKILL.md`
- **Story types:** `skills/engineering-management/jira_architect/SKILL.md`
