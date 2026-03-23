---
name: workflow-guide-me-to-feature-prioritization-and-investment
description: >
  Prioritize features or evaluate feature investment (build vs don't). Uses prioritize-features,
  prioritization-frameworks, analyze-feature-requests, feature-investment-advisor.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Feature prioritization and investment

Prioritize a list of features or evaluate a single feature investment (build vs don't build) using frameworks and unit-economics-style reasoning. Use when triaging a backlog, planning a release, or deciding whether to invest in a feature.

## When to Use

- You have a **list of features** or requests and need a prioritized order
- You need to **evaluate one feature** (revenue impact, cost, ROI, strategic value) and get a build/don't-build recommendation
- You are in **backlog refinement** or **roadmap** planning and want a consistent prioritization method

## Prerequisites

- Input: list of features (titles + short description) or one feature with context (segment, revenue impact, effort)
- Skills: `skills/product/product-discovery/prioritize-features/SKILL.md`, `skills/product/product-execution/prioritization-frameworks/SKILL.md`, `skills/product/product-discovery/analyze-feature-requests/SKILL.md`, `skills/product/product-discovery/feature-investment-advisor/SKILL.md`

## Step 1: Clarify scope and mode

1. **Confirm with the user:** List prioritization (rank many) or single-feature investment (evaluate one)?
2. **List mode:** Do they have a backlog export, spreadsheet, or bullet list? Any existing criteria (e.g. strategic theme, segment)?
3. **Investment mode:** Do they have rough effort, revenue impact, or cost? If not, ask for what they know; use "TBD" where needed per `standards/conventions.md`.

## Step 2: Read reference materials

1. **prioritization-frameworks** — Choose a framework (value vs effort, RICE, MoSCoW, etc.) and apply consistently.
2. **prioritize-features** — For ranking a list by criteria and producing a rationale.
3. **analyze-feature-requests** — For grouping by theme, strategic alignment, impact, effort, risk.
4. **feature-investment-advisor** — For a single-feature build/don't-build with revenue, cost, ROI, strategic value.

## Step 3: Prioritize list (if list mode)

1. Apply **analyze-feature-requests** to group and score the list (theme, alignment, impact, effort, risk).
2. Use **prioritize-features** with the chosen framework to produce a ranked list and short rationale per item (or per tier).
3. Share the ranking with the user; adjust if they want different weights or constraints.

## Step 4: Evaluate single feature (if investment mode)

1. Use **feature-investment-advisor** with the feature description and any numbers they provided (revenue, cost, strategic value).
2. Produce: build / don't build (or conditional), key drivers, and what would change the recommendation.
3. If they have a list and want both ranking and investment view, do Step 3 first, then run the advisor on the top 1–2 items.

## Step 5: Output and next steps

1. Write the prioritized list or investment recommendation to a file (e.g. `workspace/_notes/YYYY-MM-DD_prioritization.md` or `YYYY-MM-DD_feature-investment-<name>.md`).
2. Tell the user how to use this in roadmap or backlog (e.g. feed into **roadmap-and-release-planning**).

## References

- Conventions: `standards/conventions.md`
- Roadmap: `skills/product/product-execution/workflow-guide-me-to-roadmap-and-release-planning/SKILL.md`
