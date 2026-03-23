---
name: adr-writer
description: Write Architecture Decision Records (ADR) in a consistent format and location
metadata:
  type: skill
  department: engineering
  source: claude-skills
  version: "1.0"
---
# ADR Writer Skill

## 1. Purpose

Produce **Architecture Decision Records (ADRs)** that capture important technical decisions, context, and consequences in a consistent format and location so future engineers and tech leads can understand why things are built the way they are.

## 2. When This Skill Is Used

- After a significant architecture or design decision (e.g. new integration, data model change, migration strategy).
- When the user or a story asks for an "ADR", "architecture decision record", or "design doc" for a decision.
- When documenting why a spike or POC led to a specific approach.

## 3. Where to Store ADRs

| Context | Location | Naming |
|---------|----------|--------|
| **V3 / NestJS** (repo-wide or V3-specific) | `ti/v3/docs/adr/` (create if missing) | `YYYY-MM-DD-short-title.md` (e.g. `2026-03-07-vector-search-opensearch.md`) |
| **TI-eng workspace** (generic or cross-cutting) | `workspace/_references/adr/` | Same: `YYYY-MM-DD-short-title.md` |
| **Epic-specific** (tied to an epic folder) | `workspace/projects/<slug>/epics/` | `adr-YYYY-MM-DD-short-title.md` or single `adr.md` for the epic |

Prefer **one ADR per decision**. Use the date prefix for ordering.

## 4. ADR Structure

Use this template (adapt section titles if the project already has a standard):

```markdown
# ADR-XXX: Short Title

**Date:** YYYY-MM-DD  
**Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-YYY]  
**Deciders:** (optional: team or role)

## Context

What is the issue or opportunity? What constraints and forces are at play?
(2–4 short paragraphs.)

## Decision

What did we decide to do? Be concrete (e.g. "We will use OpenSearch for vector search with index X and embedding model Y.").

## Alternatives Considered

- **Option A:** Brief description. Why not chosen.
- **Option B:** Brief description. Why not chosen.

## Consequences

- **Positive:** ...
- **Negative / Risks:** ...
- **Follow-ups:** (e.g. "Add monitoring for latency in 2 weeks")

## References

- Links to docs, tickets (e.g. TI-3516), PRs, or other ADRs.
```

- **Status:** Start with `Proposed`; move to `Accepted` when the decision is agreed and implemented. Use `Superseded by [path]` when another ADR replaces this one.
- **Cross-references:** Use Jira ticket IDs where relevant; see `standards/conventions.md`.

## 5. Quality Guidelines

- **Short and scannable:** One decision per ADR; use bullets and short paragraphs.
- **Traceable:** Link to PRD, epic, or Jira ticket when the decision is driven by a story.
- **Honest about trade-offs:** Document downsides and risks, not only benefits.
- **No vague language:** Avoid "flexible", "scalable" without concrete meaning; state what we chose and what we gave up.

## 6. When Not to Write an ADR

- Trivial or reversible choices (e.g. variable naming).
- Purely tactical implementation details that are already clear from code and comments.
- When the team has a different doc standard (e.g. RFC in Notion); in that case, follow that standard and still capture decision, context, and consequences.
