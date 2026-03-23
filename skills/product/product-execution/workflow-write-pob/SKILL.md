---
name: workflow-write-pob
description: >
  Write a Product Opportunity Brief (POB) for escalation, opportunity, revenue blocker, compliance,
  or tech debt. Uses ti-write-pob.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Write Product Opportunity Brief (POB)

Produce a Product Opportunity Brief for an escalation, opportunity, revenue blocker, compliance need, or tech-debt initiative. Output is aligned with the TI Product Brief template structure but scoped for a single opportunity or problem.

## When to Use

- You need to document an **escalation**, **opportunity**, **revenue blocker**, **compliance** ask, or **tech debt** initiative
- You want a short, structured brief (not a full product PRD) for prioritization or leadership
- You are responding to a stakeholder ask or incident with a one-brief format

## Prerequisites

- Input: description of the opportunity or problem (paste, email, or conversation)
- TI Product Brief template: `templates/product/[TEMPLATE] Product Brief .md` (for section reference)
- Skill: `skills/product/product-execution/ti-write-pob/SKILL.md`

## Step 1: Clarify type and scope

1. **Confirm with the user:** Which POB type? (escalation / opportunity / revenue blocker / compliance / tech debt)
2. **Gather:** Who is asking, what is the ask, what is the impact if we do nothing, and what success looks like. If unclear, ask per `standards/conventions.md`.

## Step 2: Read reference materials

1. **ti-write-pob skill** — `skills/product/product-execution/ti-write-pob/SKILL.md` (structure, sections for POB)
2. **Product Brief template** — `templates/product/[TEMPLATE] Product Brief .md` (reuse relevant sections: problem, objective, scope, success criteria)

## Step 3: Draft the POB

1. Use **ti-write-pob** to produce the brief: problem statement, opportunity/impact, recommended scope, success criteria, and (if applicable) rough effort or dependency.
2. Keep it to 1–2 pages; avoid turning it into a full PRD unless the user asks.
3. If sections from **create-prd** help (e.g. objectives, segments), use them sparingly.

## Step 4: Output and next steps

1. Write the output to a file. Suggested: `workspace/_inbox/YYYY-MM-DD_<name>-pob.md`.
2. Tell the user they can use this for prioritization, roadmap discussion, or as input to a full PRD later.

## References

- Conventions: `standards/conventions.md`
- Full PRD workflow: `skills/product/product-execution/workflow-write-prd/SKILL.md`
