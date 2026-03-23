---
name: implementation-from-story
description: Implement a story by following its Cursor prompt and acceptance criteria
metadata:
  type: skill
  department: engineering
  source: ti-rd-playbook
  version: "1.0"
---
# Implementation From Story Skill

## 1. Purpose

Guide engineers to implement a Jira story (or local story file) by **following the story's Cursor prompt** and **acceptance criteria** in a consistent, codebase-aware way.

## 2. When This Skill Is Used

- After loading a Jira ticket via `guide-me-to-start-from-jira-ticket` or `jira-ticket-context`.
- When the user is implementing a story that has a **Cursor prompt** (in Jira description or in a local `story-*.md` file).
- When the user asks to "implement TI-XXXX" or to "code the story".

## 3. Relationship to Other Skills

- **Cursor prompt structure** is defined by the tech lead skill: `skills/engineering-management/cursor_prompt_builder/SKILL.md`. The prompt contains: Role, Task, CRITICAL docs, CODEBASE CONTEXT, WHAT TO IMPLEMENT (Parts), ARCHITECTURE RULES, DO NOT, TESTING.
- **Codebase paths and patterns** come from `skills/engineering/codebase-navigation/SKILL.md` and from the TI codebase at `ti/` (especially `ti/v3/`).
- **Testing** follows `skills/engineering/unit-testing-v3/SKILL.md` (unit) and `skills/engineering/e2e-playwright/SKILL.md` (E2E) as applicable.

## 4. Implementation Order

0. **Surface current state to the user.** Before implementing, **search the codebase** for the files and areas the story touches. Summarize for the user: what exists today, how it works, and what the ARCHITECTURE RULES allow. **Propose options** that respect those rules; do not assume—if something is ambiguous, ask the user. See `standards/conventions.md` (Codebase-first, Ask before deciding).

1. **Read the Cursor prompt** (full block from the story or Jira).
2. **CRITICAL — Read these docs FIRST:** Open and skim the listed docs in order (paths relative to repo root, e.g. `ti/v3/docs/ARCHITECTURE.md`). Do not skip; they define architecture and patterns.
3. **CODEBASE CONTEXT:** Visit the referenced files and patterns (controllers, adapters, DI tokens). Understand existing code before adding new code.
4. **WHAT TO IMPLEMENT — Parts:** Implement in Part order. Each Part is a logical unit (e.g. "Part 1 — Backend guard", "Part 2 — Frontend conditional"). Verify each part before moving on.
5. **ARCHITECTURE RULES:** Respect build-time and runtime constraints (e.g. `ti/v3/docs/ARCHITECTURE_VALIDATOR.md`, hexagonal boundaries).
6. **DO NOT:** Avoid every listed anti-pattern (e.g. no `@ts-ignore`, no importing concrete implementations instead of DI tokens).
7. **TESTING:** Add or run tests that match the prompt's TESTING section and the story's acceptance criteria.

## 5. Paths and Conventions

- **Paths:** All paths in Cursor prompts are **relative to repo root** (e.g. `ti/v3/src/modules/chat/chat.controller.ts`). Use them as-is when navigating or editing.
- **Cross-references:** Use Jira ticket IDs (e.g. TI-3516) in commits and comments; see `standards/conventions.md`.
- **Naming:** Follow existing module and file naming in the codebase (see `ti/v3/src/modules/` structure).

## 6. When There Is No Cursor Prompt

If the ticket has acceptance criteria and technical notes but **no** Cursor prompt:

1. Summarize the ACs and technical scope.
2. Propose a small implementation plan (2–4 parts) based on the technical notes.
3. Point to `ti/v3/docs/ARCHITECTURE.md` and the relevant module under `ti/v3/src/modules/` or `ti/` legacy.
4. Suggest reading existing similar code (e.g. same controller or adapter) before writing new code.
5. Add tests that cover the acceptance criteria.

## 7. Definition of Done

Before considering the story done:

- All acceptance criteria are met.
- Code follows the Cursor prompt's DO NOT and ARCHITECTURE RULES.
- New or updated tests pass (unit and/or E2E as specified).
- No new linter errors; no `@ts-ignore` or `eslint-disable` unless explicitly justified and documented.
