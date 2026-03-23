# Conventions

Shared rules for stories, epic summaries, PRD artifacts, and all skill-generated output.

## Codebase-first (current-state awareness)

Whenever a **product feature** is worked on -- by product (PRD, assessment, scope) or by engineering (implementation, stories, audits):

1. **Search the existing codebase** for the area the feature touches: relevant modules, endpoints, patterns, and constraints.
2. **Surface current state to the user** before proposing or writing: what exists today, how it works, and what the architecture allows.
3. **Propose options that respect the rules** -- architecture, DoR, and existing patterns. The agent should offer better or aligned options, not assume in place of the user.

## Ask before deciding

When users are **creating** or **interacting** (e.g. writing a PRD, defining scope, creating a story, choosing recommendations):

1. **Ask as many clarifying questions as possible** before writing or proposing. Cover: problem, users, success metrics, scope, constraints, priorities, and prior art.
2. **Do not make decisions in place of the user.** If something is ambiguous or could go multiple ways, ask rather than assume.
3. **Do not write substantial output until** the user has answered key questions or explicitly asked for a draft (in which case ask at least the most critical questions first).

## Cross-referencing

When referencing other stories (in dependencies, test plans, ACs, or any narrative):

1. **Use issue tracker IDs** when they exist (e.g. Jira ticket IDs).
2. **Use story titles** when tickets have not been created yet.
3. **Never** reference by local file name or story number alone.

## Naming

**No timestamp prefix required.** The repo is versioned with Git; history and ordering come from version control. Use stable, descriptive filenames.

| Artifact | Convention | Example |
|----------|------------|---------|
| Epic folder | `eng/<phase>/epic-<ID>/` | `eng/beta/epic-TI-3613/` |
| Story files | `story-N-short-description.md`; `<ID>-story-N-....md` after push | `story-1-feature.md` |
| Epic summary | `epic-summary.md` (one per epic folder) | `epic-summary.md` |
| PRD assessment | `prd-assessment.md` | `prd-assessment.md` |

## Story quality bar

Every generated story must meet the "Full-Baked" standard:

- Concrete acceptance criteria (no "TBD", "Later", or vague language).
- A prompt with specific file paths and code patterns.
- Story point estimate with justification.
- Dependencies listed by ticket ID or title.
- Security, analytics, observability, and feature flags addressed or explicitly marked N/A.

## Soft delete (no hard deletes)

Do **not** delete files from the workspace. If content is superseded or deprecated:

1. Move the file to a `_archive/` folder or rename with a `.deprecated` suffix.
2. Add a note at the top explaining why and linking to the replacement.

## Output locations

When skills generate output files, use the workspace directory structure:

| Output type | Location |
|-------------|----------|
| PRD / Product Brief | `workspace/projects/<slug>/prd/` |
| Strategy docs | `workspace/_notes/strategy/` |
| General notes | `workspace/_notes/` |
| Inbox (drafts) | `workspace/_inbox/` |
| Evidence | `workspace/_evidence/` |
