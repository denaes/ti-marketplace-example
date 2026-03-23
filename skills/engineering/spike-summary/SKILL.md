---
name: spike-summary
description: Document the output of a technical spike or research task in a consistent format
metadata:
  type: skill
  department: engineering
  source: ti-rd-playbook
  version: "1.0"
---
# Spike Summary Skill

## 1. Purpose

Turn a **spike**, **proof-of-concept**, or **research task** into a clear, reusable document so that:
- The team can decide next steps (e.g. proceed, pivot, or abandon).
- Implementation stories can be written from the findings.
- Future engineers can avoid redoing the same research.

## 2. When This Skill Is Used

- After a [RESEARCH] or spike story is completed (from Jira or from a local story).
- When the user asks to "document the spike", "write up the POC results", or "summarize the research".
- When closing a technical investigation that did not produce code (or produced only throwaway POC code).

## 3. Where to Store Spike Summaries

| Context | Location | Naming |
|---------|----------|--------|
| **Epic-specific** | `workspace/projects/<slug>/eng/<phase>/` or `epics/` | `spike-summary-<topic>.md` or `spike-<topic>.md` |
| **Standalone / ti-eng** | `workspace/_references/spikes/` | `spike-<short-topic>.md` |
| **V3-specific** | `ti/v3/docs/` (if it becomes long-lived reference) | `SPIKE-<topic>.md` |

No timestamp prefix required; Git versions the file. Use descriptive topic in the name.

## 4. Spike Summary Structure

```markdown
# Spike: [Short Title]

**Date:** YYYY-MM-DD  
**Ticket:** TI-XXXX (if applicable)  
**Author / assignee:** (optional)

## Goal

One or two sentences: what question were we trying to answer or what risk were we de-risking?

## Approach

What did we do? (e.g. "Evaluated libraries A and B; built a minimal POC for A against our API.")

## Findings

- **Option / Path 1:** What we learned. Pros/cons. Effort or constraints.
- **Option / Path 2:** Same.
- **Recommendation:** Which option we recommend and why.

## Constraints / Risks

- Technical, security, or operational limits discovered.
- What we did *not* test or validate.

## Next Steps

- [ ] Story/decision 1 (e.g. "Create [BE] story for X")
- [ ] Story/decision 2
- [ ] Link to follow-up ticket(s) if created

## References

- Links to POC branch, docs, Jira tickets, ADRs.
```

- **Cross-references:** Use Jira ticket IDs; see `standards/conventions.md`.

## 5. Quality Guidelines

- **Actionable:** The "Next Steps" section should allow a tech lead to create or refine stories without re-reading the whole spike.
- **Honest:** Include "we did not test X" or "blocked by Y" when relevant.
- **Concise:** Prefer bullets and short paragraphs; long prose belongs in an appendix or linked doc.
- **Traceable:** Link the spike to the originating ticket (e.g. [RESEARCH] story) and to any follow-up epics or ADRs.

## 6. Relation to ADR

- A **spike summary** answers "what did we learn?" and "what should we do next?"
- An **ADR** records "what did we decide?" and "why?"  
If the spike leads to a clear decision, consider writing an ADR (see `skills/engineering/adr-writer/SKILL.md`) and referencing the spike in the ADR's References.
