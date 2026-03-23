---
name: ti-write-pob
description: >
  Write a TI Product Opportunity Brief (POB) for escalations, opportunities, revenue blockers,
  compliance, or tech debt. Output aligns with templates/product/[TEMPLATE] Product Brief .md. Use when
  capturing an escalation, customer opportunity, or problem brief for TI.
metadata:
  type: skill
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# TI Write POB (Product Opportunity Brief)

## Purpose

Create a **TI Product Opportunity Brief (POB)** — a problem- or opportunity-focused brief used to evaluate escalated customer feedback, revenue blockers, and strategic product opportunities. The output **must** follow the **TI Product Brief template** exactly so it can be used for prioritization and product review. This skill is TI-specific and uses Thought Industries (TI) terminology and the standard brief format.

## When to Use

- Escalated customer requests or repeated feature requests
- Revenue blockers or expansion enablers
- Strategic roadmap proposals or opportunity assessments
- Significant workflow or scalability gaps
- Compliance or tech debt that needs product visibility
- When the user asks for a "POB," "opportunity brief," "problem brief," or "escalation brief" for TI

## Template (mandatory)

The output **must** follow the structure and section order of:

**`templates/product/[TEMPLATE] Product Brief .md`**

Read that file before writing. For a POB, emphasize:

1. **Initiative / Project Summary** — Table: Title, **Type** (choose one: Escalation / Opportunity / Revenue Blocker / Compliance / Tech Debt), Primary Customer, Additional Customers / Signal Strength, Customer Segment(s) (C1 / C2 / Enterprise / Mid-Market), Product Area(s), Submitted By, Date, Evidence Links (Gong, ticket, screenshots, academy URL), Concept Links (prototype, mockup)
2. **Opportunity Brief** — All required sections (*):
   - Executive Summary (one-sentence summary, impacted personas, severity/urgency)
   - Customer Problem (objective, problem statement in the prescribed format, **top 3 user stories only**)
   - Current State & Product Gap (what TI supports today, product gap, evidence)
   - Impact & Opportunity (customer impact, business impact for TI, why now, competition & leapfrog)
   - Workarounds & Limitations (current workarounds, why not viable long-term)
   - Success Criteria & Measurement (quantitative metrics table, qualitative indicators)
   - Solution Concept (desired outcome, constraints/non-goals, concept prototype)
   - Assumptions to Validate
   - Risks, Dependencies, Compliance (if applicable)
   - Repro Steps (if applicable — e.g. for defects)
3. **Product Review Notes** (Product only) — Decision, Next Step (Discovery / Backlog / Roadmap / Decline), Related PRD / Discovery Doc

Use **TI terminology**: course, learning path, Panorama, sublicense, C1/C2, etc. Follow the template's "Writing Guidelines" and "Before Completing This Doc" (speak to at least one customer or review validated feedback; confirm not solvable with existing functionality).

## Instructions

1. **Ask before writing (mandatory).** Do not write the POB until you have enough input. Ask as many clarifying questions as possible: type (escalation/opportunity/revenue blocker/compliance/tech debt), primary customer, problem statement, what TI supports today vs gap, evidence, impact (customer and business), success metrics. Prefer asking over assuming. See `standards/conventions.md` (Ask before deciding).

2. **If the opportunity touches existing TI product/code:** Search the codebase (`ti/`, `ti/v3/`) for the area involved. Surface **current state** to the user (what TI supports today, relevant workflows, constraints). The "Current State & Product Gap" section must accurately reflect this. See `standards/conventions.md` (Codebase-first).

3. **Leverage existing skills** for structure and quality:
   - Problem framing: use the prescribed problem statement format from the template
   - Evidence: link to Gong, tickets, screenshots, or academy URL where possible
   - Success criteria: quantitative (metric, baseline, target, how measured) and qualitative
   - Keep user stories to **top 3 maximum**

4. **Output structure.** Produce markdown that **matches the template section headings and table formats** in `templates/product/[TEMPLATE] Product Brief .md`. All required sections (*) must be present. Omit only "Repro Steps" and "Risks/Dependencies" if not applicable.

5. **Save.** Save the output as a markdown file (e.g. `[Title] - POB.md` or `POB-[short-name].md`) in the user's workspace (e.g. `workspace/_inbox/` or a folder they specify).

## Quality Checklist

- [ ] Type is exactly one of: Escalation / Opportunity / Revenue Blocker / Compliance / Tech Debt
- [ ] Problem statement format: "I am a [persona] trying to [outcome], but [barrier] because [root cause], which results in [consequence]"
- [ ] Top 3 user stories only (maximum 3)
- [ ] Current State & Product Gap: what TI supports today + specific product gap + evidence
- [ ] TI terminology used consistently
- [ ] Evidence links or placeholders included
- [ ] Conventions: `standards/conventions.md`; ask-before-deciding and codebase-first followed

## References

- **Template:** `templates/product/[TEMPLATE] Product Brief .md`
- **Conventions:** `standards/conventions.md`
- **Related (full PRD with staged criteria):** `skills/product/execution/ti-write-prd/SKILL.md` — use when the opportunity is approved and needs full PRD with staged features/acceptance criteria
