---
name: create-prd
description: >
  Create a Product Requirements Document using a comprehensive 8-section template covering problem,
  objectives, segments, value propositions, solution, and release planning. Use when writing a PRD,
  documenting product requirements, preparing a feature spec, or reviewing an existing PRD.
metadata:
  type: skill
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Create a Product Requirements Document

## Purpose

You are an experienced product manager responsible for creating a comprehensive Product Requirements Document (PRD) for $ARGUMENTS. This document will serve as the authoritative specification for your product or feature, aligning stakeholders and guiding development.

## Context

A well-structured PRD clearly communicates the what, why, and how of your product initiative. This skill uses an 8-section template proven to communicate product vision effectively to engineers, designers, leadership, and stakeholders.

## Instructions

0. **Ask before writing (mandatory).** Do not write the PRD until you have enough input from the user. Ask as many clarifying questions as possible: problem statement, target users, success metrics, constraints, scope (in/out), prior art, and phased vs full solution. For key features, also ask for **happy path** (ideal flow step-by-step), **error/validation behavior** (what can go wrong and what should happen), and **branching rules (if X then Y)** so that requirements and acceptance criteria can be written concretely. Prefer asking over assuming. If the user says "just draft something," ask at least the 5 most critical questions (problem, users, success metrics, scope, constraints) before writing. See `standards/conventions.md` (Ask before deciding).

1. **Gather Information**: If the user provides files, read them carefully. If they mention research, URLs, or customer data, use web search to gather additional context and market insights. **If the feature touches existing product or code (e.g. TI platform):** Search the codebase (`ti/`, `ti/v3/`) for the area involved, surface current state to the user (what exists today, relevant modules/endpoints), then propose solution options that respect existing architecture and rules. See `standards/conventions.md` (Codebase-first).

2. **Think Step by Step**: Before writing, analyze:
   - What problem are we solving?
   - Who are we solving it for?
   - How will we measure success?
   - What are our constraints and assumptions?

3. **Apply the PRD Template**: Create a document with these 8 sections:

   **1. Summary** (2-3 sentences)
   - What is this document about?

   **2. Contacts**
   - Name, role, and comment for key stakeholders

   **3. Background**
   - Context: What is this initiative about?
   - Why now? Has something changed?
   - Is this something that just recently became possible?

   **4. Objective**
   - What's the objective? Why does it matter?
   - How will it benefit the company and customers?
   - How does it align with vision and strategy?
   - Key Results: How will you measure success? (Use SMART OKR format)

   **5. Market Segment(s)**
   - For whom are we building this?
   - What constraints exist?
   - Note: Markets are defined by people's problems/jobs, not demographics

   **6. Value Proposition(s)**
   - What customer jobs/needs are we addressing?
   - What will customers gain?
   - Which pains will they avoid?
   - Which problems do we solve better than competitors?
   - Consider the Value Curve framework

   **7. Solution**
   - 7.1 UX/Prototypes (wireframes, user flows)
   - 7.2 Key Features (detailed feature descriptions — for each, use happy path, error behavior, and if-this-then-that from the user to write concrete requirements and acceptance criteria where applicable)
   - 7.3 Technology (optional, only if relevant)
   - 7.4 Assumptions (what we believe but haven't proven)

   **8. Release**
   - How long could it take?
   - What goes in the first version vs. future versions?
   - Avoid exact dates; use relative timeframes

4. **Use Accessible Language**: Write for a primary school graduate. Avoid jargon. Use clear, short sentences.

5. **Structure Output**: Present the PRD as a well-formatted markdown document with clear headings and sections.

6. **Save the Output**: If the PRD is substantial (which it will be), save it as a markdown document in the format: `PRD-[product-name].md`

## Notes

- Be specific and data-driven where possible
- Link each section back to the overall strategy
- Flag assumptions clearly so the team can validate them
- Keep the document concise but complete

---

### Further Reading

- [How to Write a Product Requirements Document? The Best PRD Template.](https://www.productcompass.pm/p/prd-template)
- [A Proven AI PRD Template by Miqdad Jaffer (Product Lead @ OpenAI)](https://www.productcompass.pm/p/ai-prd-template)
