---
name: story-estimation
description: >
  Story point scale and justification rules (1/2/3/5/8, when to split). Use when writing or reviewing
  story points in generate-epics or create-story.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Story Estimation

## Purpose

Apply a **consistent story point scale** and **justification rules** so estimates are comparable across epics and so oversized stories are split before implementation.

## When to Use

- When writing story points in generate-epics-and-stories or create-story
- When reviewing or refining an epic (re-estimating stories)
- When a story feels "too big" and you need a rule to split it

## Point Scale

| Points | Meaning | Typical scope |
|--------|---------|----------------|
| **1** | Trivial | Small config change, copy tweak, single narrow fix. No design. |
| **2** | Small | One clear component or endpoint; well-defined pattern; few files. |
| **3** | Medium | One feature area; multiple files but one module; some integration. |
| **5** | Large | Cross-module or cross-layer; non-trivial design; multiple acceptance criteria. |
| **8** | X-Large | Epic-level scope; must be split. Use only if explicitly agreed as a spike or placeholder. |

**No 13 or 21.** If the work is that large, split into multiple stories (see `story-splitting` skill).

## Justification

Every story with points **must** have a short **justification** (one line in the story file). Example:

- *"Single controller method + unit tests; follows existing VectorSearchController pattern."* → 2
- *"New module + adapter + 2 endpoints + tests; no new infra."* → 5

If the justification stretches beyond one sentence or touches "and also…", consider splitting.

## When to Split

- **Backend:** If a [BE] story covers **more than 3 endpoints or 3 distinct services**, split into [BE-1], [BE-2], etc. (per `jira_architect` skill).
- **Frontend:** If a [FE] story covers more than one major screen or flow, split.
- **Points:** If the honest estimate is **5 or 8**, ask: "Can this be two 2s or two 3s?" Split by logical boundary (e.g. by endpoint, by user flow).
- **Uncertainty:** If the team is unsure (spike needed), use a [RESEARCH] story first; then estimate the implementation stories.

## References

- **Granularity:** `skills/engineering-management/jira_architect/SKILL.md` (backend >3 endpoints → split)
- **Splitting:** `skills/engineering-management/story-splitting/SKILL.md`
- **Conventions:** `standards/conventions.md`
