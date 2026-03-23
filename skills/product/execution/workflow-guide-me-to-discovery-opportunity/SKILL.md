---
name: workflow-guide-me-to-discovery-opportunity
description: >
  Run a discovery cycle — interviews → synthesis → problem statement → opportunity tree / hypothesis.
  Uses discover-* and define-* skills.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Discovery to opportunity

Orchestrate a discovery cycle from raw interviews or research to a structured problem statement, opportunity tree, and testable hypothesis. Use when you have (or plan) customer interviews or competitive input and want a clear opportunity frame for the product team.

## When to Use

- You have interview notes, survey snippets, or competitive notes to synthesize
- You are planning or have run discovery interviews and need synthesis and framing
- You want a problem statement and opportunity tree before writing a PRD

## Prerequisites

- Input: interview notes, summaries, or research artifacts (or plan to run interviews first)
- Skills: discover-interview-prep, summarize-interview, discover-interview-synthesis, define-problem-statement, define-opportunity-tree, define-hypothesis, discover-competitive-analysis (all under `skills/product/`)

## Step 1: Clarify inputs and goals

1. **Confirm with the user:** What do they have? (raw notes, already summarized interviews, competitor links, none yet)
2. **Goal:** Problem statement only, or full opportunity tree + hypothesis? Which segment or persona?
3. If they have nothing yet, use **discover-interview-prep** (`skills/product/discovery/discovery-interview-prep/SKILL.md`) to build an interview plan and script; then they can run interviews and return with notes.

## Step 2: Synthesize research (if interviews/notes exist)

1. **Summarize interviews** — Use **summarize-interview** on each interview or batch. Extract themes, quotes, pains, and jobs.
2. **Synthesis** — Use **discover-interview-synthesis** to turn summaries into themes, insights, and opportunity areas.
3. **Competitive context** — If relevant, use **discover-competitive-analysis** and feed key findings into the synthesis.

## Step 3: Define problem and opportunity

1. **Problem statement** — Use **define-problem-statement** (`skills/product/execution/define-problem-statement/SKILL.md`) to produce a clear, stakeholder-ready problem statement.
2. **Opportunity tree** — Use **define-opportunity-tree** to map opportunities from the problem and synthesis.
3. **Hypothesis** — Use **define-hypothesis** to turn the chosen opportunity into a testable if/then hypothesis (for experiments or PRD).

## Step 4: Output and next steps

1. Write outputs to files, e.g. in `workspace/_notes/` or a dated folder: problem-statement.md, opportunity-tree.md, hypothesis.md.
2. Tell the user they can feed these into **write-prd-product-brief** or **assess-prd** when moving to a PRD.

## References

- Conventions: `standards/conventions.md`
- Discovery process (full cycle): `skills/product/discovery/discovery-process/SKILL.md`
- Write PRD: `skills/product/execution/workflow-write-prd/SKILL.md`
