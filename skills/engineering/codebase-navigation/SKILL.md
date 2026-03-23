---
name: codebase-navigation
description: Navigate the TI codebase (ti/, ti/v3) and find the right docs and modules
metadata:
  type: skill
  department: engineering
  source: ti-rd-playbook
  version: "1.0"
---
# Codebase Navigation Skill

## 1. Purpose

Help engineers (and AI assistants) quickly find **where code and docs live** in the TI repo so implementation stays aligned with architecture and existing patterns. When working on a **product feature**, search the codebase first and **surface current state to the user** (what exists today, which patterns and rules apply) before proposing changes. Propose options that respect architecture and conventions. See `standards/conventions.md` (Codebase-first).

## 2. Repo Layout (High Level)

| Path | Purpose |
|------|---------|
| **`ti/`** | Main TI application (legacy Koa, GraphQL, LMS, jobs). Root of the product codebase. |
| **`ti/v3/`** | V3 API — standalone NestJS app; migrated endpoints, vector search, chat, structured data, etc. |
| **`ti/v3/src/`** | V3 source: modules, common adapters, guards, app entry. |
| **`ti/v3/docs/`** | Architecture and flow docs (ARCHITECTURE.md, INTERNAL_RPC.md, FEATURE_FLAGS.md, etc.). |
| **`skills/engineering/`** | Engineering skills: TDD, debugging, code review, implementation. |
| **`skills/engineering-management/`** | Tech lead: epics, stories, capacity planning, Jira workflows. |
| **`skills/product/`** | Product: PRDs, assessments, discovery, strategy, PM skills. |
| **`docs/`** (repo root) | Conventions, PRD template, pipeline, source of truth. |

All **paths in prompts and stories are relative to repo root** (e.g. `ti/v3/src/modules/chat/chat.controller.ts`).

## 3. V3 (NestJS) Structure

- **`ti/v3/src/main.ts`** — Entry point.
- **`ti/v3/src/app.module.ts`** — Root module; imports feature modules.
- **`ti/v3/src/modules/`** — Feature modules (e.g. `chat/`, `vector-search/`, `structured-data/`, `feature-flag/`, `content/`, `snippet/`, `faq/`, `admin/`). Each module typically has:
  - `*.controller.ts` — REST or HTTP layer.
  - `*.service.ts` — Application logic.
  - `domain/` — Models, resolvers, domain logic.
  - `listeners/` — Event listeners (when event-driven).
- **`ti/v3/src/common/`** — Shared guards, adapters (e.g. feature-flag, OpenSearch), decorators, error handling.
- **`ti/v3/test/`** — Unit and integration tests; structure mirrors `src/` (e.g. `test/modules/chat/chat.service.spec.ts`).
- **`ti/v3/docs/`** — Read these when implementing:
  - `ARCHITECTURE.md` — Deployment, modules, auth, data flow.
  - `ARCHITECTURE_VALIDATOR.md` — Build-time architecture rules.
  - `INTERNAL_RPC.md` — Internal service-to-service calls.
  - `SERVICE_BRIDGE.md` — Bridge between legacy and V3.
  - `flows/FEATURE_FLAGS.md` — Feature flag usage and placement.
  - Other flow or auth docs as referenced in Cursor prompts.

## 4. Legacy App (ti/ outside v3)

- **`ti/app.ts`**, **`ti/dev_app.ts`** — App entry.
- **`ti/lib/`** — Shared libraries (e.g. Redis, external APIs).
- **`ti/gql/`** — GraphQL resolvers and mutations.
- **`ti/lms/`** — LMS controllers and logic.
- **Routes and proxy:** Legacy serves on port 4000; V3 on 4001; proxy config in `lib/v3_proxy*`.

When a story touches both legacy and V3, the Cursor prompt or technical notes will usually point to specific files (e.g. `ti/lib/rustici_api.ts`, `ti/lms/controllers/manager/topics.ts`).

## 5. Conventions

- **Paths in Cursor prompts:** Always relative to repo root; use `ti/v3/...` or `ti/...` explicitly.
- **Cross-references:** Use Jira ticket IDs in comments and docs; see `standards/conventions.md`.
- **Source of truth:** `docs/SOURCE-OF-TRUTH.md` lists key paths for codebase, PRD, Jira, and roles.

## 6. Quick Lookups

- **Where is feature X implemented?** — Search under `ti/v3/src/modules/` and `ti/v3/src/common/`; check `ti/v3/docs/` for flows.
- **Where are tests for module Y?** — `ti/v3/test/` with the same relative path (e.g. `test/modules/chat/` for `src/modules/chat/`).
- **Where do I add a new endpoint?** — Add controller + service in the appropriate module under `ti/v3/src/modules/`; register in the module and ensure guards (auth, feature flag) are applied per `ti/v3/docs/` and the story's Cursor prompt.
