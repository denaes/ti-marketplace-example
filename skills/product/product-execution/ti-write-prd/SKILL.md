---
name: ti-write-prd
description: >
  Write a TI Product Requirements Document (PRD) that follows the TI Product Brief template. Use when
  creating a PRD for a TI product feature, initiative, or capability. Leverages create-prd; output
  must align with templates/product/[TEMPLATE] Product Brief .md.
metadata:
  type: skill
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# TI Write PRD

## Purpose

Create a **TI Product Requirements Document** for a product feature, initiative, or capability. The output **must** follow the **TI Product Brief template** exactly so it can be used for prioritization, assessment, and decomposition into epics and stories. This skill is TI-specific and aligns with Thought Industries (TI) terminology, product areas, and the standard brief format.

## When to Use

- Creating a PRD for a new TI feature or initiative
- Documenting product requirements for engineering handoff in TI format
- When the user asks for a "TI PRD," "product brief," or "write PRD in our template"

## Template (mandatory)

The output **must** follow the structure and section order of:

**`templates/product/[TEMPLATE] Product Brief .md`**

Read that file before writing. Key parts:

1. **Initiative / Project Summary** — Table: Title, Type (Escalation / Opportunity / Revenue Blocker / Compliance / Tech Debt), Primary Customer, Customer Segment(s), Product Area(s), Submitted By, Date, Evidence Links, Concept Links
2. **Opportunity Brief** — Sections: Executive Summary (one-sentence, impacted personas, severity/urgency), Customer Problem (objective, problem statement, top 3 user stories), Current State & Product Gap (what TI supports today, product gap, evidence), Impact & Opportunity, Workarounds & Limitations, Success Criteria & Measurement, Solution Concept (with prototype), Assumptions to Validate, Risks/Dependencies/Compliance, Repro Steps (if applicable)
3. **Staged Features & Acceptance Criteria** (if scope warrants) — Feature comparison table (Alpha/Beta/GA), Staged User Stories & Acceptance Criteria by epic
4. **Learning Plan** (if applicable) — Stage table with duration, hypothesis, audience, learning design, decision framework

Use **TI terminology**: course, learning path, Panorama, sublicense, C1/C2, etc. See the template's "Writing Guidelines" in the Instructions section.

## Instructions

1. **Leverage create-prd.** Follow the process in `skills/product/product-execution/create-prd/SKILL.md`:
   - **Ask before writing (mandatory).** Ask as many clarifying questions as possible (problem, target users, success metrics, scope, constraints, prior art). Do not write until you have enough input. See `standards/conventions.md` (Ask before deciding).
   - **Why now:** Explicitly ask: "Why now? (market shift, customer change, launch/renewal timing, repeated signal, competitive pressure)." If the answer is thin, prompt: "Any market trend, customer signal, or event that makes this urgent this quarter/year?"
   - **Competition:** For "Competition & How we Leap Frog," if the user has competitive intel (e.g. NotebookLM or files in `workspace/_references/competitive/`), ask them to paste a summary or give the file path so it can be included. See `workspace/_references/competitive-intel-README.md`.
   - **Estimated impact:** If the user can provide rough numbers (ARR, churn rate, deal count, ACV), offer to generate an **Estimated Impact** subsection using `templates/product/Estimated Impact [TEMPLATE].md` (reference: Measurement Loop Alpha Product Brief).
   - **If the feature touches existing TI product/code:** Search the codebase (`ti/`, `ti/v3/`) for the area involved, surface current state to the user (what TI supports today, relevant modules), then propose solution options that respect existing architecture. See `standards/conventions.md` (Codebase-first).
   - Gather information, think step by step (problem, who for, success, constraints).

2. **Map create-prd content to the TI Product Brief template.** Do not output the generic 8-section create-prd format. Instead:
   - Map Summary → Initiative/Project Summary table + Executive Summary
   - Map Background/Objective → Customer Problem (objective, problem statement), Current State & Product Gap
   - Map Market Segment(s) → Customer Segment(s), Impacted Personas
   - Map Value Proposition / Solution → Solution Concept, Workarounds & Limitations
   - Map success metrics → Success Criteria & Measurement (quantitative and qualitative)
   - Map Release → Staged Features / Learning Plan if applicable
   - Map assumptions → Assumptions to Validate
   - Map risks → Risks, Dependencies, Compliance

3. **Requirements & Acceptance Criteria (interactive).** Before writing the "Staged Features & Acceptance Criteria" section, run an interactive pass. Do **not** fill Detailed Requirements or Acceptance Criteria with placeholders only. For each user story or epic in scope, ask the user:
   - **Happy path:** "Describe the ideal flow from start to finish. What does the user do, and what does the system do at each step?"
   - **Non‑happy path:** "What can go wrong (validation errors, missing data, permission denied, timeout)? For each, what should the user see or what should the system do?"
   - **If-this-then-that:** "Are there branching rules? (e.g. If user is in Panorama X, then …; if content is paywalled, then …). List conditions and outcomes."
   - **Edge cases:** "Any limits (rate limits, max size, concurrency)? What happens at the limit?"
   Use the user's answers to write **concrete** requirements and ACs (Given/When/Then or bullet form per template). Reference: Product Brief template "Staged User Stories & Acceptance Criteria" table and the stage standards link in the template.
   **Reusable prompt for one epic:** "For **[Epic / feature name]**: (1) Happy path: step-by-step ideal flow? (2) What can go wrong, and what should happen? (3) Any if-this-then-that rules (roles, segments, flags)? (4) Any limits or edge cases?"

4. **Output structure.** Produce markdown that **matches the template section headings and table formats** in `templates/product/[TEMPLATE] Product Brief .md`. Preserve required sections (marked * in the template). Omit only sections that are explicitly "If Applicable" and not relevant.

5. **Save.** Save the output as a markdown file (e.g. `PRD-[short-name].md` or `[Initiative Title] - Product Brief.md`) in the user's workspace (e.g. `workspace/_inbox/` or a folder they specify).

6. **Customer evidence.** If the user mentions customer evidence (calls, Gong, tickets, surveys), suggest: store raw files in `workspace/_evidence/raw/` and add a row to `workspace/_evidence/evidence-to-artifacts.md` mapping the evidence to this PRD or epic. See `workspace/_evidence/README.md`.

## Quality Checklist

- [ ] All required template sections present and in order
- [ ] Type is one of: Escalation / Opportunity / Revenue Blocker / Compliance / Tech Debt
- [ ] Problem statement uses the format: "I am a [persona] trying to [outcome], but [barrier] because [root cause], which results in [consequence]"
- [ ] Top 3 user stories only (maximum 3)
- [ ] TI terminology used consistently
- [ ] Current State & Product Gap describes what TI supports today and the specific gap
- [ ] Conventions: `standards/conventions.md`; codebase-first and ask-before-deciding followed

## References

- **Template:** `templates/product/[TEMPLATE] Product Brief .md`
- **Process (create-prd):** `skills/product/product-execution/create-prd/SKILL.md`
- **Conventions:** `standards/conventions.md`
