---
name: ti-strategy-from-playground
description: >
  Turn the Strategic Analysis Playground (or a Working Backwards document) into a rich strategic
  document. Use when you have approach, layers, and backwards output and want a full strategy
  narrative for alignment and execution.
metadata:
  type: skill
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# TI Strategy from Playground

## Purpose

Produce a **rich strategic document** from the Strategic Analysis Playground (or any "Working Backwards"–style input). The output is a single markdown doc with 12 sections grounded in the Playground's approach (Vision → Winning Aspiration → Strategic Imperatives → Customer & Problems → Product Advantage), Working Backwards Output, and optional appendix material (baseball cards, optionality, interview guides).

## When to Use

- You have **Strategic Analysis_ Playground.md** (or a similar playground/backwards doc) and want a formal strategy document for exec alignment or roadmap input.
- You are running the **write-strategy-from-playground** workflow and need the skill to generate the doc from extracted content.

## Input

- **Primary:** File path to the Playground (e.g. `Strategic Analysis_ Playground.md`) or pasted content. Must include at least: **Approach** (non-linear layers), **Working Backwards Output** (strategy objective, opportunity, problems, ecosystem gaps, opportunity size, strategic proposal, GTM, business model, moat, strategic bet).
- **Optional:** Baseball cards, optionality dimensions, interview guides, mapping tables — include in appendix when present.

## Output Structure (12 sections)

Generate markdown in this order. Use Playground content to fill each section; turn bullets/placeholders into narrative where needed; keep or adapt tables.

1. **Framing** — Objective, North Star, JTBD (from "Framing the Objective" and "Strategy Objective").
2. **Approach** — Non-linear layers (Vision → Winning Aspiration → Strategic Imperatives → Customer & Problems → Product Advantage); short summary + "we iterate, not linear."
3. **Opportunity** — Why now, target customer, market shift (from "Opportunity" and "Frame the Opportunity").
4. **Problems to Solve (JTBD)** — Jobs, pain points, workarounds (from "Problems to Solve" and "Identify Customer Problems").
5. **Why the Ecosystem Isn't Solving This Well** — Structural/tech/execution gaps (from "Assess Ecosystem Offerings").
6. **Opportunity Size** — TAM/SAM/SOM, willingness to pay, strategic impact (from "Size the Opportunity").
7. **Strategic Proposal** — Solution framework, technology framework, MVP (from "Define the Strategic Proposal" and "Establish Technology & Platform Direction").
8. **Go-to-Market Motion** — Entry wedge, distribution, expansion (from "Align GTM Motion").
9. **Business Model & Pricing** — Monetization, constraints.
10. **Moat & Defensibility** — What compounds, durable advantage (from "Define Moat & Defensibility").
11. **Summary: The Strategic Bet** — High-conviction bet, next steps (from "Synthesize Strategic Bet").
12. **Appendix (optional)** — Baseball cards, optionality dimensions, interview guides, mapping tables (references or short excerpts from Playground).

## Instructions

1. **Read the input.** Extract the Approach (layers), Working Backwards Output blocks, and any appendix material (baseball cards, optionality table, interview guides).
2. **Identify gaps.** For sections that are empty or placeholder-only (e.g. "Opportunity Size not filled"), ask the user: "Do you have TAM/SAM/SOM or willingness-to-pay data?" or "Any additional sources (competitive NotebookLM summary, finance assumptions) to include?"
3. **Generate section by section.** Use Playground text verbatim where it is already narrative; turn bullet lists into short paragraphs where it improves readability; preserve tables. Do not invent content for sections the Playground does not address — either leave a short "[To be filled]" note or skip and note "Not in source."
4. **Appendix.** If the Playground contains baseball cards, optionality dimensions, or interview guides, add an Appendix section with references (file + section) or short excerpts. Do not duplicate huge tables in full unless the user asks.
5. **Output.** Emit the full markdown. The workflow will save it to `workspace/_notes/strategy/YYYY-MM-DD_ti-product-strategy.md` or a path the user specifies.

## Quality Checklist

- [ ] All 12 sections present (or explicitly "Not in source" / "[To be filled]").
- [ ] Framing and Strategic Bet are grounded in the Playground (no invented North Star or bet).
- [ ] Tables from the Playground are preserved or adapted, not dropped.
- [ ] TI terminology and personas (C1/C2, ICP, JTBD) used consistently.

## References

- **Source of truth:** Strategic Analysis_ Playground.md (repo root or path provided by user)
- **Workflow:** `skills/product/execution/workflow-write-strategy-from-playground/SKILL.md`
- **Working Backwards format:** See "Working Backwards Output" in the Playground
