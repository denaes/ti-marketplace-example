---
name: ti-write-hld
description: >
  Write a TI High-Level Design (HLD) aligned with the TI HLD template. Use when creating an HLD for a
  feature or migration (NestJS/React, strangler pattern, DoD). Leverages codebase awareness, options
  analysis, and optionally ADR for key decisions.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# TI Write HLD

## Purpose

Create a **TI High-Level Design (HLD)** for a feature or modernization initiative. The output **must** follow the **TI HLD template** exactly so it serves as the source of truth for development, aligns with the Definition of Done (DoD), and bridges legacy state and target architecture. This skill is TI-specific (Thought Industries stack: legacy Node/Ember, NestJS/React, strangler migration).

## When to Use

- Designing a new feature or capability in the V3 (NestJS/React) stack
- Planning a migration from legacy Node/Ember to NestJS/React
- When the user asks for an "HLD," "high-level design," or "technical design doc" for TI
- When an epic or story requires an HLD before implementation (e.g. [DESIGN] story type)

## Template (mandatory)

The output **must** follow the structure and section order of:

**`templates/product/[TEMPLATE] HLD.md`**

Read that file before writing. Sections:

1. **Header** — Feature Name, Author, Date, Status (Draft / Under Review / Approved), Jira Epic (link)
2. **1. Executive Summary** — Goal (problem we're solving), Business Value, Technical Impact (systems touched, blast radius). *Architect's Guidance: value in three sentences.*
3. **2. The 'Strangler' Migration Plan** — Interoperability (new NestJS/React ↔ legacy Node/Ember), Routing (API Gateway / CloudFront), State Management (shared DB, schema protection). *Architect's Guidance: how we keep the legacy app alive while replacing.*
4. **3. Proposed Architecture** — NestJS (module breakdown, services, DTOs), React (component hierarchy, state, Design library), Integration (FE–BE contract). *Architect's Guidance: modularity, avoid distributed monolith.*
5. **4. Options Analysis** — Option A (Proposed): pros, cons, technical risks. Option B (Alternative): pros/cons, rejection reason. Option C (Status Quo): why we can't stay. Summary table (Options | Pros | Cons). *Architect's Guidance: valid Option B required; no confirmation bias.*
6. **5. Engineering Recommendation** — Statement of intent: why Option A is the most scalable and maintainable path relative to 2-year growth plan. *Architect's Guidance: own the trade-offs.*
7. **6. Anti-Regression & QA Strategy** — Test Plan (Unit/Jest, Integration, E2E/Playwright), Parity Verification (React vs Ember checklist), Observability (CloudWatch, alerts). *Architect's Guidance: machine must prove it's not broken; per DoD.*
8. **7. Data & Infrastructure** — Schema changes, AWS resources (K8s, RDS, S3), Cost estimate at 10x scale. *Architect's Guidance: design for target scale.*
9. **8. Security & Compliance** — AuthN/AuthZ, Data Privacy (GDPR/SOC2), Encryption (at rest, in transit). *Architect's Guidance: isolation boundaries clearly defined.*

Preserve the **Architect's Guidance** italic lines from the template where they appear; they are part of the TI standard.

## Instructions

1. **Ask before writing (mandatory).** Do not write the HLD until you have enough input. Ask clarifying questions: feature/epic name, goal, scope (which systems are in scope), Jira epic link if any, known constraints, and whether there are existing spikes or ADRs to reference. See `standards/conventions.md` (Ask before deciding).

2. **Search the codebase (codebase-first).** Search `ti/` and `ti/v3/` for the area the feature or migration touches:
   - **Legacy:** Relevant Koa/Node routes, Ember areas, GraphQL resolvers, shared DB usage.
   - **V3:** Existing NestJS modules (`ti/v3/src/modules/`), `ti/v3/docs/` (ARCHITECTURE.md, SERVICE_BRIDGE.md, INTERNAL_RPC.md), patterns (guards, adapters, events).
   Surface **current state** to the user (what exists today, how legacy and V3 interact) so the HLD accurately describes interoperability and migration path. See `standards/conventions.md` (Codebase-first). Use `skills/engineering/codebase-navigation/SKILL.md` for paths and patterns.

3. **Options Analysis (Section 4).** Treat this as a structured decision. For any major choice (e.g. where to put the new API, how to route traffic, which module owns the logic):
   - Propose at least **Option A (recommended)** and **Option B (alternative)** with clear rejection reason; include **Option C (status quo)** and why it's not viable.
   - If the decision is significant and should be recorded long-term, **create or reference an ADR** per `skills/engineering/adr-writer/SKILL.md` (e.g. in `ti/v3/docs/adr/` or the epic folder). The HLD can reference the ADR in Section 5 (Engineering Recommendation) or in the Options Summary.

4. **Leverage existing skills for content quality:**
   - **QA / test strategy (Section 6):** Align with `skills/engineering-management/qa_test_planner/SKILL.md` and `skills/engineering/unit-testing-v3/SKILL.md`, `skills/engineering/e2e-playwright/SKILL.md` — unit targets, integration approach, E2E critical paths, parity checklist.
   - **Module/technical detail (Section 3):** Use patterns from `skills/engineering-management/cursor_prompt_builder/SKILL.md` (CODEBASE CONTEXT, module boundaries) so the proposed architecture matches how V3 is actually structured (see `ti/v3/docs/ARCHITECTURE.md`).
   - **DoD:** The template and DoD link require "feature passes end to end regression"; Section 6 must show how that is verified.

5. **Output structure.** Produce markdown that **matches the template section headings, numbering, and Architect's Guidance** in `templates/product/[TEMPLATE] HLD.md`. Use the same heading style (e.g. **1. Executive Summary**). Include the options summary table in Section 4.

6. **Save.** The HLD is **project/feature-level**: one HLD per project or feature, covering all phases (Alpha, Beta, GA, Fast Follow) at a high level. Save to `workspace/projects/<slug>/eng/HLD-[feature-name].md` (in `eng/`, **not** inside a phase folder like `eng/alpha/`). If the user specifies a different path, use it. If you create an ADR for a key decision, save it per `skills/engineering/adr-writer/SKILL.md` and link it from the HLD.

## Quality Checklist

- [ ] All 8 template sections present and in order
- [ ] Header has Feature Name, Author, Date, Status, Jira Epic
- [ ] Section 2 addresses strangler pattern (interop, routing, state/DB)
- [ ] Section 4 has Option A, Option B (with rejection reason), Option C (status quo), and summary table
- [ ] Section 6 ties to DoD (E2E regression, parity, observability)
- [ ] Codebase (`ti/`, `ti/v3/`) was searched and current state reflected
- [ ] Conventions: `standards/conventions.md`; ask-before-deciding and codebase-first followed
- [ ] Optional: key decisions recorded in an ADR and linked from the HLD

## References

- **Template:** `templates/product/[TEMPLATE] HLD.md`
- **TI V3 architecture:** `ti/v3/docs/ARCHITECTURE.md`, `ti/v3/docs/SERVICE_BRIDGE.md`, `ti/v3/docs/INTERNAL_RPC.md`
- **ADR (for key decisions):** `skills/engineering/adr-writer/SKILL.md`
- **Codebase navigation:** `skills/engineering/codebase-navigation/SKILL.md`
- **QA / test planning:** `skills/engineering-management/qa_test_planner/SKILL.md`, `skills/engineering/unit-testing-v3/SKILL.md`, `skills/engineering/e2e-playwright/SKILL.md`
- **Conventions:** `standards/conventions.md`
