---
name: workflow-write-strategy-from-playground
description: >
  Take the Strategic Analysis Playground (or a Working Backwards doc) as input; produce a rich
  strategic document. Uses ti-strategy-from-playground.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Write Strategy from Playground

Produce a **rich strategic document** from the Strategic Analysis Playground. Output is a single markdown file with 12 sections (Framing, Approach, Opportunity, Problems, Ecosystem Gaps, Opportunity Size, Strategic Proposal, GTM, Business Model, Moat, Strategic Bet, Appendix), ready for exec alignment and roadmap input.

## When to Use

- You have **Strategic Analysis_ Playground.md** (or similar) with approach, layers, and Working Backwards Output.
- You want a formal strategy doc that can be updated over time and referenced by product and leadership.

## Prerequisites

- Playground file (e.g. `Strategic Analysis_ Playground.md` at repo root) or user-provided strategy/backwards doc
- Skill: `skills/product/product-strategy/ti-strategy-from-playground/SKILL.md`

## Step 1: Get the input

1. **Confirm the source.** Is the user providing the Playground file path (e.g. `Strategic Analysis_ Playground.md`) or pasting content? If path, read the file.
2. **Extract.** Identify: Approach (non-linear layers), Working Backwards Output, and any Baseball Cards, optionality dimensions, or interview guides for the appendix.

## Step 2: Clarify scope (optional)

Ask the user:
- "Which sections are most important to fill first?"
- "Any additional sources to include (e.g. competitive NotebookLM summary, finance assumptions)?"

## Step 3: Generate the strategy doc

1. Use **ti-strategy-from-playground** to produce the full markdown:
   - Input: Playground content (or path) from Step 1.
   - Follow the 12-section structure in the skill.
   - For gaps (e.g. empty Opportunity Size), ask for data or note "[To be filled]."
2. Turn Playground bullets/placeholders into narrative where it helps; preserve tables.

## Step 4: Save and link

1. **Save** the output to:
   - Default: `workspace/_notes/strategy/YYYY-MM-DD_ti-product-strategy.md` (create `workspace/_notes/strategy/` if needed)
   - Or a project folder: `workspace/projects/<strategy-slug>/strategy-doc.md` if the user has a project slug.
2. Tell the user where the file was written. If the Playground lives in the repo, they can add a line there: "Generated strategy doc: `workspace/_notes/strategy/YYYY-MM-DD_ti-product-strategy.md`."

## Step 5: Next steps (optional)

- "Want me to generate **OKRs** from the North Star and Strategic Bet?" (use **ti-prd-okrs** with the strategy doc as context, or a short narrative summary of North Star + bet.)

## References

- **Skill:** `skills/product/product-strategy/ti-strategy-from-playground/SKILL.md`
- **Playground:** Strategic Analysis_ Playground.md (repo root)
- **OKRs:** `skills/product/product-execution/ti-prd-okrs/SKILL.md` (optional follow-up)
