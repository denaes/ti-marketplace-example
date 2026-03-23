---
name: workflow-write-epics-and-stories-from-prd
description: Generate Jira-ready Epics and Stories from a PRD document
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Generate Epics and Stories from a PRD

This workflow transforms a Product Requirements Document (PRD) into a structured set of **Epics** and **Stories** following the project's "Full-Baked" standard. Each story is implementation-ready with acceptance criteria and a Cursor IDE prompt.

## Prerequisites

- A PRD markdown file (local path or content)
- Access to the story examples in `workspace/_references/story-examples/` for format reference
- Access to the skills in `skills/engineering-management/` for evaluation criteria

---

## Step 0: Organize the PRD Input and phase folders

If the PRD file is located in `workspace/_inbox/`:

1. **Create a dated project folder** in `workspace/projects/` using the format `{YYYY-MM-DD}-{slugified-prd-name}/`
   - Derive the slug from the PRD filename: lowercase, spaces → hyphens, drop the `.md` extension
   - Example: `SEO PRD.md` dropped on 2026-03-06 → `workspace/projects/2026-03-06-seo-prd/`
2. **Create the phase-based layout** (see `docs/WORKSPACE-PHASES.md`):
   - `product/brief/`, `product/`, `eng/`
   - For each **release phase** in the PRD (Alpha, Beta, GA, Fast Follow), create `eng/<phase>/` with folder names: `alpha`, `beta`, `ga`, `fast-follow`
   - If the PRD does not specify phases yet, create at least `eng/alpha/` (or ask the user which phases to create)
3. **Move the PRD file** from `_inbox/` into the project folder (e.g. `product/` or `product/brief/`)
4. **Output location for epics:** Each phase’s epic and stories go into `workspace/projects/<slug>/eng/<phase>/` (e.g. `eng/alpha/`, `eng/beta/`)

If the PRD is already in a project folder with existing phase folders, use that layout. If it uses a single `epics/` or `eng/epic/` folder (legacy), you may keep it or migrate to phase folders per user preference.

```bash
mkdir -p workspace/projects/{YYYY-MM-DD}-{slug}/product/brief workspace/projects/{YYYY-MM-DD}-{slug}/eng/alpha workspace/projects/{YYYY-MM-DD}-{slug}/eng/beta workspace/projects/{YYYY-MM-DD}-{slug}/eng/ga workspace/projects/{YYYY-MM-DD}-{slug}/eng/fast-follow
# Add only the phase folders the PRD defines; then move PRD into product/ or product/brief/
```

---

## Step 1: Read Reference Materials

Read these files to understand the expected formats and quality bar:

1. **Shared conventions:**
   - `standards/conventions.md` — Cross-referencing rules, naming conventions, quality bar

2. **Skills (evaluation criteria):**
   - `skills/engineering-management/definition_of_ready/SKILL.md` — The 12-dimension "Full-Baked" test for PRD readiness
   - `skills/engineering-management/jira_architect/SKILL.md` — The "Required 14" story types and decomposition rules
   - `skills/engineering-management/qa_test_planner/SKILL.md` — The QA test plan structure for [QA] stories
   - `skills/engineering-management/cursor_prompt_builder/SKILL.md` — Template and rules for generating Cursor IDE prompts

3. **Story examples (output format):**
   - Read ALL files in `workspace/_references/story-examples/` to understand the exact structure, level of detail, and tone expected in each story

4. **Project overview:**
   - `docs/PIPELINE-PRD-TO-JIRA.md` — The pipeline overview and "Full-Baked" component checklist

---

## Step 2: Ingest and Analyze the PRD

1. Read the provided PRD file completely
2. **Use the project folder** from Step 0; each **phase** gets its own output folder: `workspace/projects/<slug>/eng/<phase>/` (e.g. `eng/alpha/`, `eng/beta/`, `eng/ga/`, `eng/fast-follow/`).
3. Identify the following from the PRD:
   - **Product phases** (Alpha, Beta, GA, Fast Follow) and which requirements map to which phase (staged acceptance criteria, milestone tables, or phase labels in the requirements table)
   - **Personas** and their core jobs-to-be-done
   - **Requirements table(s)** — Extract each requirement ID, user story, acceptance criteria, priority, and **phase** (if stated)
   - **Non-goals** — What is explicitly out of scope
   - **Metrics & instrumentation** — What analytics events are needed
   - **Staged acceptance criteria** — Milestone-specific requirements; use these to assign requirements to phases

---

## Step 3: Validate PRD Readiness (Definition of Ready)

Apply the `definition_of_ready` skill against the PRD. Evaluate all 12 dimensions:

| Category | Dimensions |
|----------|-----------|
| **Functional Clarity** | User Stories & AC, Edge Cases, Permissions/RBAC |
| **Technical & Data** | Data Model Impact, API Contracts, Backward Compatibility |
| **Observability & Support** | Instrumentation/Analytics, Logging & Alerting, Reporting |
| **Safety & Rollout** | Feature Flagging, Security, Performance |

**Output:** A readiness assessment with:
- Score (0-100%)
- Gap analysis table (Category / Status: MISSING, VAGUE, COMPLETE / Required Action)
- Go/No-Go recommendation (Green / Yellow / Red)

> [!IMPORTANT]
> If the PRD scores **Red**, stop here and report the gaps to the user. The PRD needs more baking before decomposition.
>
> If **Yellow**, proceed but flag items that will need **[RESEARCH] Technical Spike** stories.

---

## Step 3b: Codebase search and current state (before defining epics)

Before defining epics and stories, **search the codebase** (`ti/`, `ti/v3/`) for the areas the PRD touches (modules, endpoints, patterns). **Surface current state to the user**: what exists today, how it works, and what patterns/rules apply. Stories generated in Step 5 must **respect existing patterns and architecture**. If **scope or priorities** (e.g. which phase first, which requirements are P0) are unclear from the PRD, **ask the user** before generating. Do not assume—ask. See `standards/conventions.md` (Codebase-first, Ask before deciding).

---

## Step 4: Define Epics (one per phase)

**Phases map to epics:** For each **release phase** (Alpha, Beta, GA, Fast Follow) that has scope in the PRD, define **one epic**. Group the PRD requirements that belong to that phase into that epic.

**Epic naming convention:** `[Product Area] - [Capability] — [Phase]`
Examples: `Conversational Search — Alpha`, `Conversational Search — Beta`, `Conversational Search — GA`, `Conversational Search — Fast Follow`

For each phase epic, define:
- **Phase** (Alpha | Beta | GA | Fast Follow)
- **Title** (include the phase in the title)
- **Summary** (2-3 sentences: business objective for this phase, what “done” means for this phase)
- **Key PRD requirements covered** (requirement IDs that are in scope for this phase)
- **Output folder** — `workspace/projects/<slug>/eng/<phase>/` with `<phase>` = `alpha`, `beta`, `ga`, or `fast-follow`

---

## Step 5: Decompose Epics into Stories

**For each phase epic** (each folder `eng/<phase>/`), generate stories using the **"Required 14"** story type framework from the `jira_architect` skill. Stories in a phase folder belong to that phase’s epic only. Apply the appropriate category tags:

| Tag | Story Type | When to Include |
|-----|-----------|-----------------|
| `[RESEARCH]` | Technical Spike | Unknown tech, libraries, or API limitations |
| `[DESIGN]` | HLD & API Contract | Architecture changes or new patterns |
| `[DB]` | Schema & Migrations | Database changes needed |
| `[BE]` | Core Logic & API | Server-side implementation |
| `[FE]` | UI/UX Implementation | Frontend components |
| `[SEC]` | Security & Auth | RBAC, PII, rate limiting |
| `[QA]` | Integration & E2E | **Always include.** Centralized test plan for the entire epic — see [QA Story Generation Rules](#qa-story-generation-rules) below |
| `[ANALYTICS]` | Instrumentation | Tracking events |
| `[LOG]` | Observability | Logging, traces |
| `[ALERT]` | Monitoring & Reporting | Dashboards, alerts |
| `[FF]` | Feature Flag & Rollout | Toggle logic, phased rollout |
| `[DOCS]` | Documentation | Wiki, README, help docs |
| `[PERF]` | Optimization | Load testing, caching |
| `[OPS]` | Infrastructure | Env vars, CI/CD, cloud resources |

**Rules:**
- Every story type must be present OR explicitly marked N/A with justification
- If a backend story covers more than 3 endpoints, split into `[BE-1]`, `[BE-2]`, etc.
- Every story must link back to its parent Epic
- Mark stories as **DONE/Deferred** if the PRD or context indicates existing coverage (see story-4 and story-6 examples)
- **Cross-references:** See `standards/conventions.md` for cross-referencing rules. In short: use Jira ticket IDs when they exist, story titles when they don't. Never use local file names or story numbers.

---

## Step 6: Write Each Story

For each story, create a markdown file following **exactly** this structure (derived from the story examples):

```markdown
# Story N: [Tag] Story Title

**Depends on:** (list dependencies by Jira ticket ID if they exist, e.g., `TI-3516`, or by story title if not yet created, e.g., "Instance-Level Feature Toggle". Never use local story numbers.)

## User Story

**As a** [persona],
**I want** [capability],
**so that** [benefit].

## Context & Current State

[2-5 paragraphs explaining:]
- What exists today (code, infrastructure, patterns)
- What's missing or broken (the gap this story fills)
- Architecture notes if relevant (e.g., hexagonal patterns, DI tokens)
- References to specific files/modules in the codebase

## Technical Details

### [BE] Backend Changes
- [Specific implementation steps with file paths]

### [FE] Frontend Changes
- [Specific implementation steps with component names]

### [SEC] Security
- [Auth, access control, rate limiting considerations]

### [DB] Data Changes
- [Schema changes if any]

### [LOG] Observability
- [Logging requirements]

(Include only relevant subsections — omit those that are N/A)

## Acceptance Criteria

- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [...]

## Story Points: N

**Justification:** [1-2 sentences explaining the estimate]

---

## Cursor Prompt

Generate a Cursor Prompt for this story following the `skills/engineering-management/cursor_prompt_builder/SKILL.md` skill.
The prompt must include: Role, Task, CRITICAL docs, CODEBASE CONTEXT, WHAT TO IMPLEMENT (Parts), ARCHITECTURE RULES, DO NOT, and TESTING sections.
Refer to the skill for story-type-specific variations (e.g., [QA] stories use the `qa_test_planner` prompt instead).
```

---

## QA Story Generation Rules

Every epic **must** include exactly one `[QA]` story. This story is the **centralized test plan** for the entire epic — it does not test individual stories in isolation, it tests the integrated system.

### Rules

1. **The [QA] story depends on ALL other stories** — it is always the last story in the dependency chain
2. **It must reference every other story in the epic** by Jira ticket ID (or title if not yet created) — never by story number
3. **Test scenarios are organized by functional area**, not by story number. This makes the test plan read as a coherent verification of the feature.
4. **Follow the `qa_test_planner` skill** (`skills/engineering-management/qa_test_planner/SKILL.md`) for:
   - Test scenario format (ID, title, type, preconditions, steps, expected result, failure criteria)
   - Required test categories (happy path, negative, edge case, security, integration, regression)
   - Coverage matrix (story × AC × test scenario)
5. **The Cursor Prompt must list all stories** with their key ACs and implementation file paths, so Cursor can generate tests that cover the entire epic
6. **Story points** are typically 5-8 depending on the number of stories and ACs in the epic

## Step 7: Handle Special Story States

Some stories may be **already done** or **deferred**. Follow these patterns from the examples:

### Done/Deferred Story (short form)
```markdown
# Story N: [Tag] Story Title

## Status: DONE — [Reason, e.g., "Sufficient for Alpha"]

[Brief explanation of what's covered and what's deferred]

## What's Covered
[Table or list of covered items]

## What's Deferred (Post-[Milestone])
[Table or list with priority and impact]

## Key Documentation
[Links to relevant docs]
```

### Deferred Story (with future notes)
```markdown
# Story N: [Tag] Story Title

## Status: DONE — Deferred to Post-[Milestone]

[Explanation of why this is deferred and why it's safe to defer]

## Original User Story (For Reference)
[The As a/I want/So that block]

## Future Implementation Notes
[Bullet points on where to hook in, what to reference]
```

---

## Step 8: Output the Results (per phase)

Write output **per phase** into `workspace/projects/<slug>/eng/<phase>/` (e.g. `eng/alpha/`, `eng/beta/`). After push to Jira, the sync-local-to-jira workflow renames the **phase folder** and files with Jira key prefix (see `standards/conventions.md`). PRD-level artifacts (e.g. readiness report) can go in `workspace/projects/<slug>/product/` or `eng/`.

**No timestamp prefix required** — the repo is versioned with Git; use stable filenames.

**For each phase folder** (e.g. `eng/alpha/`):

1. **Epic summary document** — `epic-summary.md` containing:
   - **Phase** (Alpha | Beta | GA | Fast Follow) — must match the folder name
   - Epic title and description
   - List of all stories for this phase with title, tag, status, story points, and dependencies
   - Total story points for this phase
   - Dependency graph (which stories block which within this phase)

2. **Individual story files** — One file per story for this phase:
   - Naming: `story-N-short-description.md` (e.g. `story-1-feature-toggle.md`)

3. **PRD readiness report** (once per project) — `prd-readiness-report.md` (from Step 3); place in `workspace/projects/<slug>/product/` or at project root under `eng/`

---

## Quality Checklist

Before finalizing, verify each story against the "Full-Baked" checklist from `docs/PIPELINE-PRD-TO-JIRA.md`:

- [ ] Every requirement from the PRD is mapped to at least one story
- [ ] Every story has concrete acceptance criteria (not vague language)
- [ ] Every story has a Cursor prompt with specific file paths and code patterns
- [ ] Story points are justified
- [ ] Dependencies between stories are explicitly stated
- [ ] Security, analytics, observability, and feature flags are covered (or marked N/A)
- [ ] No "TBD", "Later", or "Fast" without specific follow-up tickets
- [ ] Done/Deferred stories explain what's covered and what gaps remain
