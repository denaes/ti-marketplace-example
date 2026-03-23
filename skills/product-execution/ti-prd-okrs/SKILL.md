---
name: ti-prd-okrs
description: >
  Generate OKRs (Objectives and Key Results) from a TI PRD or Product Brief. Use during or after
  PRD/Brief creation so measurable outcomes align to Success Criteria and Impact. Output fits as
  06-okrs.md in multi-file briefs.
metadata:
  type: skill
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# TI PRD to OKRs

## Purpose

Produce **1–2 Objectives** with **2–4 Key Results** each from a TI Product Brief or PRD. OKRs are TI-friendly (revenue, retention, adoption, NRR, win rate) and explicitly tied to the brief’s Success Criteria & Measurement and Impact & Opportunity.

## When to Use

- **During** Product Brief generation (write-prd-product-brief workflow): when the user opts in for OKRs, run this skill as part of the same pass and write output to `06-okrs.md` in `workspace/projects/<slug>/prd/`.
- **After** a Brief exists: user asks for “OKRs for this PRD” or “generate OKRs from [file].”

## Input

- PRD or Product Brief: file path, or pasted content (at minimum: Project Summary, Product Opportunity including Success Criteria & Measurement and Impact & Opportunity).
- Optional: fiscal period, North Star metric, or team context.

## Instructions

1. **Read the brief.** Extract:
   - Initiative/project title and type (Escalation / Opportunity / Revenue Blocker / Compliance / Tech Debt).
   - **Success Criteria & Measurement** (Section 6): quantitative metrics (baseline, target, how measured), qualitative indicators.
   - **Impact & Opportunity** (Section 4): customer impact, business impact for TI (ARR at risk, expansion, accounts affected, competitive risk).
   - **Staged outcomes** (Alpha/Beta/GA) if the brief is phased.

2. **If Success Criteria is light or missing:** Ask the user for target metrics, baseline, and how they will measure (tool/owner). Do not invent numbers without asking.

3. **Derive Objectives.** One primary (main business outcome), optionally one secondary (e.g. adoption, efficiency):
   - Primary: from Impact & Opportunity and main Success Criteria (e.g. “Prove learning drives retention,” “Increase win rate in competitive deals”).
   - Secondary: only if the brief clearly supports a second outcome (e.g. “Increase platform adoption,” “Reduce time to value”).

4. **Write Key Results** in SMART form. Prefer metrics already named in the PRD. Each KR should have:
   - Measurable result (with baseline → target when possible).
   - How measured (tool, owner, or “per Success Criteria”).

5. **Output format.** Use the structure below. When used **during** brief generation, this content is written to `06-okrs.md`; include the H1 so the file is self-contained.

## Output Structure

```markdown
# OKRs for [Initiative Name]

**Source:** [PRD/Brief name], Section 6 Success Criteria & Section 4 Impact

## Objective 1: [Outcome in one line]

- **KR1:** [Measurable result; baseline → target; how measured]
- **KR2:** …
- **KR3:** …

## Objective 2 (optional): [e.g. Adoption or Efficiency]

- **KR1:** …
- **KR2:** …

## Leading indicators (optional)

- [Input metric or behavior that predicts the KRs]
```

## Quality Checklist

- [ ] Each Objective is one clear outcome (no multiple objectives in one line).
- [ ] Key Results are measurable and tied to the brief’s Success Criteria or Impact.
- [ ] No invented baselines/targets; use brief or user input.
- [ ] TI terminology consistent (ARR, NRR, C1/C2, adoption, win rate, etc.).

## References

- **Template:** `templates/product/Product Brief [TEMPLATE].md` (Sections 4 & 6)
- **Multi-file brief:** When generating as part of a brief, output goes to `workspace/projects/<slug>/prd/06-okrs.md` and must be linked from `00-index.md`.
