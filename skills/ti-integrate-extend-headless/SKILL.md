---
name: ti-integrate-extend-headless
description: >
  Describe Thought Industries’ integration story: headless framework, webhooks, APIs, prebuilt and
  custom integrations, and automation across the tech stack. Use for integration planning,
  composable UX, or “TI in the middle of the stack” architectures.
metadata:
  type: skill
  department: ti-skills
  source: thought-industries-website
  version: "1.0"
---
# Thought Industries — integrate, extend & headless

## Purpose

Capture Thought Industries’ public message on **integrations and extensibility**: **headless** options, **webhooks**, and **APIs** to build customer experiences; **prebuilt and custom** integrations; **automation** of business workflows across the tech stack.

## When to Use

- Solution architecture workshops with TI + CRM + identity + data warehouse
- Defining event-driven flows (enrollment, completion, purchase)
- Building custom front-ends or embedded experiences “around” TI

## Instructions

1. **List systems of record.** For each (identity, CRM, billing, CS, LMS-adjacent tools), state whether TI is source, consumer, or bidirectional for the data in question.
2. **Prefer events for real-time.** When the user needs near-real-time updates, start from **webhooks** and event semantics; batch exports for analytics where appropriate.
3. **Headless UX.** If the learner experience lives partly outside TI’s default UI, clarify what must remain in-platform (commerce, compliance, certificates) vs what can be composed externally—requires customer-specific decisions.
4. **Prebuilt vs custom.** Map common integrations to “likely prebuilt” vs “custom API work” only when the user names vendors; otherwise stay at capability level.
5. **Security.** Call out OAuth/scopes, secrets handling, and least-privilege API access at a requirements level; detailed threat modeling belongs with security review.

## Quality checklist

- [ ] Integration pattern named (API, webhook, batch, embedded)
- [ ] Ownership of data (system of record) stated or flagged as TBD
- [ ] No fabricated endpoint names or unsupported integration claims

## References

- [Integrate & extend](https://www.thoughtindustries.com/platform/integrate-and-extend)
