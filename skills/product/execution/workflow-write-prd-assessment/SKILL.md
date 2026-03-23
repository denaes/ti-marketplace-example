---
name: workflow-write-prd-assessment
description: Assess a PRD against the template, Definition of Ready, codebase reality, risks, and cross-PRD overlap
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Assess a PRD

This workflow produces a single comprehensive assessment report for a Product Requirements Document (PRD). It evaluates template compliance, engineering readiness, codebase impact, risks, and cross-PRD overlap — giving PM and Engineering a shared understanding of gaps before decomposition begins.

## Prerequisites

- A PRD markdown file (the document being assessed)
- The PRD template: `templates/product/Product Brief [TEMPLATE].md` - The Definition of Ready skill: `skills/engineering-management/definition_of_ready/SKILL.md`
- Access to the TI codebase (for deep codebase impact analysis)
- Existing PRD folders in `workspace/projects/` (for cross-PRD comparison)

---

## Step 0a: Clarify scope (ask before assessing)

If the **scope or feature boundaries** of the PRD are unclear (e.g. user dropped a draft, or key sections are vague), **ask the user clarifying questions first**: what is in scope, what phase/milestone, which user segments, and what is explicitly out of scope. Do not proceed with a full assessment on an ambiguous PRD without giving the user a chance to clarify. See `standards/conventions.md` (Ask before deciding).

---

## Step 0: Organize the PRD Input

If the PRD file is located in `workspace/_inbox/`:

1. **Create a dated subfolder** in `workspace/projects/` using the format `{YYYY-MM-DD}-{slugified-prd-name}/epics/`
   - Derive the slug from the PRD filename: lowercase, spaces → hyphens, drop the `.md` extension
   - Example: `SEO PRD.md` dropped on 2026-03-06 → `workspace/projects/2026-03-06-seo-prd/epics/`
2. **Move the PRD file** from `_inbox/` into the new subfolder
3. Use this new subfolder as the **output location** for all subsequent steps

If the PRD is already in a `prds/` subfolder (e.g., from a previous workflow run), use that existing folder.

// turbo
```bash
mkdir -p workspace/projects/{YYYY-MM-DD}-{slug}/epics/
mv workspace/_inbox/{filename}.md workspace/projects/{YYYY-MM-DD}-{slug}/epics/
```

---

## Step 1: Read Reference Materials

Read these files to understand the evaluation criteria:

1. **Shared conventions** — `standards/conventions.md`
   - Cross-referencing rules, naming conventions, quality bar

2. **PRD Template** — `templates/product/Product Brief [TEMPLATE].md`
   - This is the gold standard. Every PRD should follow this structure.
   - Note all sections, their purpose, and expected contents.

3. **Definition of Ready Skill** — `skills/engineering-management/definition_of_ready/SKILL.md`
   - The 12-dimension "Full-Baked" test
   - Red flag word list
   - Scoring methodology

4. **Jira Architect Skill** — `skills/engineering-management/jira_architect/SKILL.md`
   - The "Required 14" story types — useful for estimating decomposability

5. **Cursor Prompt Builder Skill** — `skills/engineering-management/cursor_prompt_builder/SKILL.md`
   - Template for Cursor IDE prompts — useful for assessing whether the PRD has enough technical detail

6. **Project Overview** — `docs/PIPELINE-PRD-TO-JIRA.md`
   - Pipeline overview and Full-Baked component checklist

---

## Step 2: Ingest the PRD

1. Read the provided PRD file completely
2. Take note of:
   - **What product/feature** is being described
   - **What phase/milestone** it targets (Alpha, Beta, GA, etc.)
   - **Key technical signals** — mentions of specific technologies, services, databases, APIs, events
   - **Personas** — who are the users?
   - **Explicit scope** — what's in and out
   - **Customer evidence** — if the PRD cites call notes, Gong, tickets, or surveys, suggest storing raw files in `workspace/_evidence/raw/` and adding a mapping row to `workspace/_evidence/evidence-to-artifacts.md` (see `workspace/_evidence/README.md`)

---

## Step 3: Deep Codebase Analysis

This is the codebase-aware layer that makes this assessment uniquely valuable. The goal is to understand how the existing application works **for real** — not from documentation, but from actual code.

### 3.1 Identify Affected Domains

From the PRD's requirements, identify which areas of the codebase will be impacted. Search for:

```
# Search for relevant modules, services, controllers
grep_search for keywords from the PRD (feature names, content types, domain terms)
find_by_name for related files (controllers, services, entities, migrations)
view_file and view_code_item to understand existing patterns
```

For each requirement in the PRD, answer:
- **Which module(s)** in the codebase does this touch?
- **Which files** will need modification vs. creation?
- **What existing patterns** can be reused? (e.g., event outbox, feature flags, guards, adapters)

### 3.2 Existing Pattern Inventory

Scan the codebase for established patterns that the PRD's feature could leverage:

- **Feature Flags** — How are they implemented? (`FeatureFlag` enum, `FeatureFlagAdapter`, Redis cache)
- **Event System** — How are events emitted and consumed? (Postgres outbox, EventsProcessor, listeners)
- **Auth & Guards** — How is access controlled? (SuperAdminGuard, CompanyGuard, optional-auth)
- **Data Layer** — What ORM is used? Migration patterns? Repository patterns?
- **API Patterns** — REST controllers, GraphQL resolvers, request/response DTOs
- **Frontend Patterns** — Component architecture, state management, styling approach
- **Testing Patterns** — Unit test framework, E2E tools, test utilities

Document which patterns the PRD's feature can reuse vs. which require new infrastructure.

### 3.3 Schema Impact Analysis

Search the database layer:
- `grep_search` for existing entities/tables mentioned or implied by the PRD
- Check if proposed changes conflict with existing schema
- Identify migration complexity (new tables vs. altering existing ones with data)

### 3.4 API Surface Analysis

- List existing endpoints that will be affected
- Identify if any **public/partner APIs** change (breaking change risk)
- Check if the PRD introduces new endpoint patterns not yet in the codebase

### 3.5 Surface current state to the user

In the assessment report, **explicitly surface current state** to the user: what exists in the codebase for the areas the PRD touches (modules, patterns, constraints), and what the architecture and rules (e.g. `ti/v3/docs/ARCHITECTURE_VALIDATOR.md`, conventions) allow. When proposing options or recommendations, **respect existing patterns and conventions** so the user and engineering can choose better or aligned solutions. See `standards/conventions.md` (Codebase-first).

---

## Step 4: Cross-PRD Comparison

List all existing PRD folders in `workspace/projects/` and compare:

```
list_dir workspace/projects/  — find all PRD folders
For each folder: read epic-summary.md (if exists) to understand scope
```

For each existing PRD, assess:
- **Overlap** — Do any requirements overlap with the new PRD?
- **Shared Infrastructure** — Does the new PRD need the same infra (e.g., event outbox, indexing pipeline, feature flags)?
- **Dependency** — Should the new PRD be sequenced before/after an existing one?
- **Conflict** — Could the new PRD's changes break or conflict with in-flight work?

---

## Step 5: Run the Assessment

Evaluate the PRD across all 6 layers. For each layer, assign a status:

- ✅ **COMPLETE** — Fully addressed, no gaps
- ⚠️ **VAGUE** — Addressed but lacks specifics or uses red flag language
- ❌ **MISSING** — Not addressed at all
- 🔍 **NEEDS SPIKE** — Requires a research ticket before estimation

### Layer 1: Template Compliance

Compare the PRD section-by-section against `templates/product/Product Brief [TEMPLATE].md`:

| Template Section | Status | Finding |
|-----------------|--------|---------|
| 1. Customer Problem | | |
| 2. Motivation & Business Case | | |
| 3. Success Metrics & Analytics | | |
| 4. Requirements & Constraints | | |
| 4.1 Scope (In/Out) | | |
| 4.2 Performance | | |
| 4.3 Security | | |
| 4.4 Privacy | | |
| 4.5 Monitoring & Alarms | | |
| 4.6 Cost | | |
| 5. High-level Experience | | |
| 5.1 Experiment & Rollout | | |
| 6. Risks & Uncertainties | | |
| 7. Phased Improvements / Roadmap | | |
| 8. Appendix (Alternatives, Benchmarks, Timeline, Glossary) | | |

**Template Compliance Score:** X/15 sections

### Layer 2: Definition of Ready (12 Dimensions)

Apply the `definition_of_ready` skill:

| # | Category | Dimension | Status | Gap / Finding | Required Action |
|---|----------|-----------|--------|---------------|-----------------|
| 1 | Functional Clarity | User Stories & AC | | | |
| 2 | Functional Clarity | Edge Cases | | | |
| 3 | Functional Clarity | Permissions/RBAC | | | |
| 4 | Technical & Data | Data Model Impact | | | |
| 5 | Technical & Data | API Contracts | | | |
| 6 | Technical & Data | Backward Compatibility | | | |
| 7 | Observability & Support | Instrumentation/Analytics | | | |
| 8 | Observability & Support | Logging & Alerting | | | |
| 9 | Observability & Support | Reporting | | | |
| 10 | Safety & Rollout | Feature Flagging | | | |
| 11 | Safety & Rollout | Security | | | |
| 12 | Safety & Rollout | Performance | | | |

**DoR Score:** X/12 dimensions (X%)

### Layer 3: Codebase Impact Analysis

From the deep codebase scan in Step 3, produce:

#### Affected Modules
| Module / Service | Files Impacted | Change Type | Complexity |
|-----------------|---------------|-------------|------------|
| | | New / Modify / Delete | Low / Med / High |

#### Reusable Patterns
| Pattern | Exists in Codebase | Can Reuse? | Notes |
|---------|-------------------|-----------|-------|
| Feature Flags | | Yes / No / Partial | |
| Event Outbox | | Yes / No / Partial | |
| Auth Guards | | Yes / No / Partial | |
| ... | | | |

#### Schema Impact
| Change | Type | Risk | Notes |
|--------|------|------|-------|
| | New Table / Alter Table / New Column | Low / Med / High | |

#### API Surface Changes
| Endpoint | Change | Breaking? | Public/Internal |
|----------|--------|-----------|-----------------|
| | New / Modify / Remove | Yes / No | |

### Layer 4: Risk Assessment

#### Vague Language Scan
Scan the PRD for red flag words used without specific definitions:

| Location | Red Flag Word/Phrase | Context | Risk Level |
|----------|---------------------|---------|------------|
| | | | HIGH / MEDIUM / LOW |

#### Risk Matrix

| Risk Category | Risk | Likelihood | Impact | Mitigation |
|--------------|------|-----------|--------|------------|
| Security | | Low/Med/High | Low/Med/High | |
| Performance | | | | |
| Data Privacy | | | | |
| Customer Impact | | | | |
| Operational | | | | |
| Staffing | | | | |

### Layer 5: Estimation Readiness

| Dimension | Status | Notes |
|-----------|--------|-------|
| Can requirements be decomposed into stories without ambiguity? | | |
| Are all dependencies identified (internal and external)? | | |
| Are there requirements that need research spikes first? | | |
| Are there external dependencies (3rd-party APIs, vendor decisions, legal)? | | |
| Does this require specialized skills not on the team? | | |
| Is the scope clear enough to estimate story points? | | |

#### Spike Candidates
List specific requirements that need a [RESEARCH] story before implementation can begin.

### Layer 6: Cross-PRD Awareness

| Existing PRD | Overlap | Shared Infra | Dependency | Conflict |
|-------------|---------|-------------|-----------|---------|
| | None / Partial / Significant | | Before / After / None | Yes / No |

---

## Step 6: Produce the Verdict

### Overall Scores

| Layer | Score | Status |
|-------|-------|--------|
| Template Compliance | X/15 | 🟢🟡🔴 |
| Definition of Ready | X% | 🟢🟡🔴 |
| Codebase Impact | — | Low / Med / High |
| Risk Level | — | Low / Med / High |
| Estimation Readiness | — | Ready / Needs Spikes / Not Ready |
| Cross-PRD Conflicts | — | None / Minor / Blocking |

### Go/No-Go Recommendation

- 🟢 **GREEN** — PRD is ready for story decomposition. Proceed to `/generate-epics-and-stories`.
- 🟡 **YELLOW** — PRD can proceed but has gaps. Include [RESEARCH] spikes in decomposition. List the gaps.
- 🔴 **RED** — PRD is not ready. Return to Product with a specific list of items to address.

### Top Priority Actions

Numbered list of the highest-priority items the PM should address, ordered by impact:

1. [Most critical gap]
2. [Second most critical]
3. ...

### Recommended Next Steps

Based on the verdict, recommend:
- If GREEN: "Run `/generate-epics-and-stories` with this PRD"
- If YELLOW: "Address items 1-3 above, then proceed with decomposition including spike stories"
- If RED: "Return to Product. Schedule a review meeting to address the gaps below."

---

## Step 7: Questions for the Product Team

For **every gap** found across all 6 layers, generate a specific, actionable question for the Product team. These are not generic — they must reference the exact gap, the PRD section, and what Engineering needs to unblock.

### Question Generation Rules

1. **One question per gap** — Don't bundle. Each gap gets its own question so PM can address them independently.
2. **Tag each question** with a type:
   - `[CLARIFY]` — The PRD says something but it's ambiguous. "Did you mean X or Y?"
   - `[MISSING]` — The PRD doesn't address this at all. "We need a decision on X."
   - `[VALIDATE]` — Engineering found something in the codebase that contradicts or complicates the PRD. "The codebase currently does X — does the PRD intend to change this?"
   - `[SCOPE]` — Unclear whether something is in or out. "Is X in scope for Alpha or deferred?"
   - `[DECISION]` — A trade-off that PM needs to weigh in on. "Should we do X (faster, riskier) or Y (slower, safer)?"
3. **Priority each question** — P0 (blocks story decomposition), P1 (blocks estimation), P2 (should be answered before dev starts)
4. **Group by layer** so PM can see where the concentration of gaps is

### Output Format

```markdown
### Questions for the Product Team

#### Layer 1: Template Compliance
| # | Priority | Type | Question | PRD Section | Why It Matters |
|---|----------|------|----------|-------------|----------------|
| 1 | P0 | [MISSING] | The Security section (4.3) is empty. What is the threat model for publicly exposing customer content? | §4.3 | Without this, Engineering must make security assumptions that could lead to a content leak incident. |

#### Layer 2: Definition of Ready
| # | Priority | Type | Question | PRD Section | Why It Matters |
|---|----------|------|----------|-------------|----------------|
| 2 | P1 | [CLARIFY] | ... | | |

#### Layer 3: Codebase Reality
| # | Priority | Type | Question | PRD Section | Why It Matters |
|---|----------|------|----------|-------------|----------------|
| 3 | P1 | [VALIDATE] | The PRD assumes content change events exist, but the codebase currently only emits events for sections and course metadata. Does the feature need events for ALL content types? | §4.1 AC 6 | Engineering would need to add event emission to 4+ content type update paths. This is a significant scope expansion. |

#### Layer 4: Risks
...

#### Layer 5: Estimation Readiness
...

#### Layer 6: Cross-PRD
...
```

### Question Count Summary

At the end of the questions section, add:

| Priority | Count | Blocks |
|----------|-------|--------|
| P0 | X | Story decomposition — must answer before `/generate-epics-and-stories` |
| P1 | X | Estimation — must answer before sprint planning |
| P2 | X | Development — should answer before coding starts |
| **Total** | **X** | |

---

## Step 8: Score Improvement Playbook

For each gap found, provide a **concrete, actionable recommendation** on how to improve the assessment score. The goal: give PM a clear path from 🔴/🟡 to 🟢.

### Playbook Generation Rules

1. **Tie every recommendation to a specific gap** — Reference the layer, dimension, and gap ID
2. **Estimate effort** for each recommendation:
   - ⚡ **Quick Win** (< 1 hour) — Add a sentence, fill a placeholder, make a decision
   - 📝 **Half-Day** (2-4 hours) — Write a section, consult a stakeholder, draft a spec
   - 🔬 **Research Needed** (1-3 days) — Requires investigation, prototyping, or cross-team alignment
   - 🏗️ **Significant Work** (1+ week) — Requires design sessions, vendor evaluation, or architectural decisions
3. **Show expected score impact** — What does fixing this do to the overall score?
4. **Order by ROI** — Quick wins that move the score the most go first

### Output Format

```markdown
### Score Improvement Playbook

**Current Score: 62% YELLOW 🟡 → Target: 85%+ GREEN 🟢**

#### Quick Wins (< 1 hour each) — Get to 70%

| # | Action | Layer | Gap | Effort | Score Impact |
|---|--------|-------|-----|--------|-------------|
| 1 | Add acceptance criteria to P0-2 and P0-5 (currently empty) | L2: DoR | User Stories & AC | ⚡ 15 min | +4% |
| 2 | Replace "Security concerns??" with a 2-paragraph threat summary | L1: Template / L2: DoR | Security | ⚡ 30 min | +6% |
| 3 | Define the feature flag name and on/off behavior | L2: DoR | Feature Flagging | ⚡ 15 min | +3% |

#### Half-Day Work — Get to 80%

| # | Action | Layer | Gap | Effort | Score Impact |
|---|--------|-------|-----|--------|-------------|
| 4 | Write the API contract for robots.txt, sitemap.xml, and JSON-LD | L2: DoR | API Contracts | 📝 3 hrs | +5% |
| 5 | Define error states and monitoring strategy | L2: DoR | Logging & Alerting | 📝 2 hrs | +4% |
| 6 | Add edge case section (failures, race conditions, flag toggle mid-indexing) | L2: DoR | Edge Cases | 📝 2 hrs | +4% |

#### Research Needed — Get to 85%+

| # | Action | Layer | Gap | Effort | Score Impact |
|---|--------|-------|-----|--------|-------------|
| 7 | Conduct security review for public content exposure | L4: Risk | Security Risk | 🔬 2 days | +3% |
| 8 | Measure unit economics on staging | L1: Template | Cost | 🔬 1 day | +2% |

#### Significant Work (if aiming for 95%+)

| # | Action | Layer | Gap | Effort | Score Impact |
|---|--------|-------|-----|--------|-------------|
| 9 | Create Figma mocks for admin AEO dashboard | L1: Template | High-level Experience | 🏗️ 1 week | +3% |
| 10 | Build working prototype and benchmark performance | L1: Template | Performance Benchmarks | 🏗️ 1 week | +2% |
```

### Score Projection

Show a waterfall of how the score improves as recommendations are addressed:

```
Current:          ████████████░░░░░░░░  62% 🟡
After Quick Wins: ██████████████░░░░░░  75% 🟡
After Half-Day:   █████████████████░░░  83% 🟢
After Research:   ██████████████████░░  88% 🟢
After Sig. Work:  ████████████████████  95% 🟢
```

---

## Step 9: Write the Report

Write the complete assessment as a **single markdown file**:

- **File name:** `prd-assessment.md` (no timestamp prefix; Git versions the file)
- **Location:** `workspace/projects/{prd-folder-name}/product/prd-assessment.md` (or `epics/` if using legacy layout)
  - The PRD folder should already exist from Step 0
- Include all 8 sections:
  1. Layers 1-6 assessment tables
  2. Verdict and Go/No-Go
  3. Questions for the Product Team (grouped by layer, tagged, prioritized)
  4. Score Improvement Playbook (ordered by ROI, with score projection)
- Use GitHub alerts (`> [!WARNING]`, `> [!IMPORTANT]`, `> [!TIP]`) for critical findings and quick wins
- Present to the user for review via `notify_user` with `PathsToReview`
