---
name: workflow-guide-me-to-audit-and-implement-recommendations
description: >
  Audit a product brief, bug report, or root cause analysis (MD), assess recommendations, then
  produce precise code changes and QA scope for selected recommendations
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Audit Document and Implement Recommendations

This workflow takes a **single markdown document** (product brief, bug report, or root cause analysis) and runs a three-phase exercise: (1) audit the document against the codebase, (2) critically assess any proposed recommendations, and (3) produce precise code changes and full QA scope for the recommendations the user selects.

Use this when you have an MD file that describes a problem or feature and possibly suggests fixes — and you want a rigorous, code-anchored implementation plan with test coverage.

**Codebase-first:** When tracing claims to code (Step 1), **surface current state to the user** in the audit summary: what exists today, how it works, and what the architecture allows. Proposals must respect existing patterns and rules. See `standards/conventions.md` (Codebase-first). **Ask before deciding:** If the user has not yet **selected which recommendations** to implement, **ask** — do not assume. Present the list and ask which rec(s) they want implementation details for. See `standards/conventions.md` (Ask before deciding).

## Prerequisites

- **Input:** One markdown file (e.g. product brief, bug write-up, root cause analysis, or code audit). The user must provide the path or content.
- **Codebase:** Access to the repository (e.g. `ti/` or project root) so the agent can trace claims to code and propose concrete edits.
- **Output location:** A folder to write outputs (e.g. `workspace/projects/<topic-folder>/epics/` or a path the user specifies). If none is given, use a folder derived from the document name (lowercase, hyphenated).

---

## Step 0: Organize the Input Document

If the input MD file is located in `workspace/_inbox/`:

1. **Create a dated subfolder** in `workspace/projects/` using the format `{YYYY-MM-DD}-{slugified-doc-name}/epics/`
   - Derive the slug from the filename: lowercase, spaces → hyphens, drop the `.md` extension
   - Example: `Scorm replacement & Rustici Registration - POB.md` → `workspace/projects/2026-03-06-scorm-replacement-rustici-registration-pob/epics/`
2. **Move the file** from `_inbox/` into the new subfolder
3. Use this new subfolder as the **output location** for all artifacts

If the input doc is already in a `prds/` subfolder, use that existing folder.

// turbo
```bash
mkdir -p workspace/projects/{YYYY-MM-DD}-{slug}/epics/
mv workspace/_inbox/{filename}.md workspace/projects/{YYYY-MM-DD}-{slug}/epics/
```

---

## Step 1: Audit the Document Against the Codebase

**Goal:** Verify that the document’s description of behavior, root causes, and code references are accurate. Produce a short audit section that either confirms the document or corrects it.

### 1.1 Ingest the Document

1. Read the full markdown file.
2. Identify:
   - **Type of document:** Product brief / bug report / root cause analysis / code audit / other.
   - **Claimed behavior or problem:** What does the doc say is happening (or should happen)?
   - **Root causes or “key files”:** Any listed files, functions, line ranges, or code paths.
   - **Recommendations:** Any suggested fixes, options, or next steps (numbered or named).

### 1.2 Trace Claims to Code

For each **root cause**, **key file**, or **code path** mentioned in the document:

1. **Resolve references** — Open the cited files and line ranges. If the doc uses relative paths (e.g. `ti/lib/rustici_api.ts`), resolve against the repo root.
2. **Verify accuracy** — Check that:
   - The described logic (branches, guards, disabled code, API usage) matches the actual code.
   - CourseIds, IDs, and data flow are correctly explained.
3. **Note gaps** — If the doc says “X is disabled” or “Y is never called”, confirm in code. If the doc is wrong or outdated, record the correction.

Produce a short **Audit summary** (can be appended to the doc or written as a separate section):

| Claim in document | Code location | Verified? | Correction (if any) |
|-------------------|---------------|-----------|----------------------|
| e.g. "deleteAllRegistrationsForCourse is disabled" | rustici_api.ts:274-346 | Yes | — |
| e.g. "updateSettings is skipped when isCentralLibraryItem" | topics.ts:226 | Yes | — |

- If everything checks out: state that the document is **accurate** for the cited code.
- If something is wrong: state the **correction** and where in the doc it should be updated.

### 1.3 Optional: Expand into a Code Audit Artifact

If the input is a product brief or bug report **without** a full code audit, you may produce a **code audit markdown** that includes:

- Architecture overview (flow of the feature or bug path).
- Key files and functions table (file, function, line range, role).
- How key identifiers are resolved (e.g. courseId, registrationId).
- Scenario-by-scenario or scenario-to-code mapping.
- Root cause summary and, if applicable, a small diagram (e.g. mermaid).

Save this as `code-audit.md` in the output folder (or a name the user specifies). No timestamp prefix; Git versions the file. If the input is already a detailed code audit, this step can be a brief “validation” addendum instead of a full new document.

---

## Step 2: Challenging Assessment of Proposed Recommendations

**Goal:** Stress-test every recommendation in the document. Do not accept them at face value; evaluate trade-offs, risks, alternatives, and implementation cost.

### 2.1 List All Recommendations

Extract every **recommendation** or **option** from the document (e.g. “Recommendation 1: Re-import under same courseId”, “Option B: Rate-limited bulk delete”). Give each a stable ID (e.g. Rec1, Rec2, Option A).

### 2.2 Assess Each Recommendation

For each recommendation, fill a **challenging assessment** table:

| Dimension | Questions to answer | Your assessment |
|-----------|---------------------|------------------|
| **Correctness** | Does it actually fix the root cause? Any missed edge cases? | |
| **Scope** | What code paths and callers are affected? Blast radius? | |
| **Risk** | What can go wrong in prod? Performance, data loss, backward compatibility? | |
| **Complexity** | New concepts? New infra? Learning curve for the team? | |
| **Alternatives** | Is there a simpler or safer alternative? Why was it not chosen? | |
| **Dependencies** | Does it depend on another rec or on external systems? | |
| **Reversibility** | Can we roll back or feature-flag easily? | |

**Output:** For each recommendation, write 2–4 sentences that summarize: (a) whether it holds up under scrutiny, (b) the main trade-off or risk, and (c) any condition under which you’d advise against it.

### 2.3 Compare and Rank

- If the document proposes **multiple** recommendations (e.g. “Option 1 vs Option 2”):
  - Compare them side-by-side on: effectiveness, risk, implementation cost, operational burden.
  - Suggest a **preferred** ordering or “primary vs fallback” if applicable.
- If a recommendation has **sub-options** (e.g. “with or without rate limiting”), call out the impact of each variant.

### 2.4 Document the Assessment

Write the assessment as a structured section (e.g. **Recommendation assessment**) that can live in the same folder as the audit. Include:

- Table of recommendations with IDs and one-line summary.
- Per-recommendation table (dimensions above) and the 2–4 sentence verdict.
- Optional: comparison table and recommended ordering.
- Any **new** alternatives you suggest that are not in the original document.

---

## Step 3: Precise Code Changes and QA Scope (for Selected Recommendations)

**Goal:** Only for the recommendations the **user has selected**, produce a precise implementation plan: exact files, functions, line-level edits, and a full QA test suite scope.

### 3.1 Get User Selection

**Before writing code-level detail:**

1. Present the list of recommendations (by ID and title) to the user.
2. Ask the user to **select which recommendation(s)** they want implementation details for (e.g. “Rec 1 and Rec 3 only”, or “all”).
3. If the user has already specified selections in the chat, use those and skip the prompt.

### 3.2 For Each Selected Recommendation: Code-Level Plan

For each selected recommendation, produce:

#### A. Files and change type

| File | Change type | Approx. lines | Description |
|------|-------------|---------------|-------------|
| e.g. `ti/lib/rustici_api.ts` | Add function, export | +60–80 | New `importAsNewVersionUnderCourseId` |
| e.g. `ti/lms/controllers/manager/topics.ts` | Replace branch, remove guard | ~+20 net | Source-switch logic + always updateSettings |

- **Change type:** Add / Modify / Delete; be specific (e.g. “Replace disabled body of X with batched implementation”).
- **Approx. lines:** New lines added, lines removed, or net change so the user can gauge size.

#### B. Concrete code changes

- **New functions:** Full signature and 1–2 sentence contract; key logic in pseudocode or real code snippets (e.g. “call Rustici with `courseId=${targetCourseId}&mayCreateNewVersion=true`”).
- **Modified functions:** Quote the **exact** current code (file, line range) that changes, then show the **replacement** or diff-style edit. Be precise enough that an engineer can apply the edit without guessing.
- **New constants or config:** Name, value, and where they live.
- **Dependencies:** New imports (e.g. `chunker`, `dbBatch`) and any callers that must be updated.

#### C. Behavior and edge cases

- What happens in the “happy path” (1–2 sentences).
- What happens when input is missing or invalid (e.g. “no directoryEntryPoint → return early”).
- Any logging, metrics, or error reporting to add.

### 3.3 For Each Selected Recommendation: QA Scope

For each selected recommendation, define the **full QA test suite** scope:

| Test layer | What to cover | Estimated count / type |
|------------|----------------|-------------------------|
| **Unit** | New or modified functions; stub external deps; assert calls and state | e.g. 2–4 tests for rustici_api |
| **Integration** | Controllers or services that call the changed code; DB/Rustici stubbed or test DB | e.g. 3–5 tests for topicUpdate SCORM branch |
| **E2E / manual** | User-visible scenarios from the doc (e.g. “Learner sees new SCORM after admin replace”) | List scenarios; count as test plan items |

- **Existing tests:** Note if there are existing specs (e.g. `test/gql/rustici.spec.ts`) and whether they need to be updated or extended.
- **New test files:** Suggest paths (e.g. `test/lib/rustici_api.spec.ts`, `test/lms/controllers/manager/topics.spec.ts`) if new files are needed.
- **Test data and mocks:** What to stub (e.g. `rusticiApiRequest`, `r.assets.findById`) and what fixtures or DB state are required.

Produce a **QA scope summary** table:

| Recommendation | Unit | Integration | E2E / manual | New files? |
|----------------|------|-------------|--------------|------------|
| Rec 1 | 2–4 | 3–5 | 5 scenarios | Optional |
| Rec 2 | 2–3 | 0–2 | Optional | No |

### 3.4 Write the Implementation Plan

Produce a **single implementation plan** document that includes:

1. **Summary** — Selected recommendations and overall effort (files, lines, test count).
2. **Per-recommendation sections** — Each with: (A) files and change type, (B) concrete code changes, (C) behavior and edge cases, (D) QA scope table and test-layer notes.
3. **Dependency and ordering** — If implementing multiple recommendations, can they be done independently? Suggested order? Any “additional required changes” (e.g. remove guard, add UI) that apply across recs.

Save the plan as `implementation-plan.md` in the output folder. Optionally add a short **Summary table** at the top (total files, total lines, total new tests) for quick reference.

---

## Step 4: Deliverables and Handoff

1. **Audit result** — Either inline in the original doc or as an addendum; plus optional `code-audit.md` if you generated one.
2. **Recommendation assessment** — `recommendation-assessment.md` with the challenging assessment and ranking.
3. **Implementation plan** — `implementation-plan.md` for the **selected** recommendations only, with precise code changes and full QA scope.

Tell the user where each artifact was written and what to do next (e.g. “Review the assessment, then confirm which recommendations you want; I’ll generate the implementation plan for those.” or “Implementation plan is ready; you can hand it to the team for estimation and QA planning.”).

---

## Optional: Updating the Rules Table

If this workflow is added to the project’s workflow list (e.g. in `.cursor/rules/prd-jira-workflows.mdc`), add a row:

| Task | Workflow file | Use when |
|------|----------------|----------|
| Audit doc and implement recommendations | `audit-and-implement-recommendations.md` | User has a product brief, bug report, or root cause analysis (MD) and wants an audit, recommendation assessment, and precise code + QA plan for selected fixes |
