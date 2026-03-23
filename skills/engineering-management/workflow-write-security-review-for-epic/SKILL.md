---
name: workflow-write-security-review-for-epic
description: >
  Ensure [SEC] coverage and DoR security dimension for an epic. Uses security-story-checklist,
  definition_of_ready; optionally jira_architect.
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Security review for epic

Review an epic for security coverage: ensure [SEC] stories exist where needed, and that every story touching auth, data, or compliance meets the security checklist. Produces a short report with gaps and recommendations.

## When to Use

- Before or after generating an epic, you want to verify security is not missed
- You are auditing an epic for Definition of Ready (Security dimension) or compliance
- The PRD or feature touches auth, PII, RBAC, or regulated data and you want a structured check

## Prerequisites

- An epic folder with `epic-summary.md` and story files. This is either a **phase folder** (`workspace/projects/<slug>/eng/<phase>/`) or a single epic folder (`eng/epic/`, `epics/`). See `docs/WORKSPACE-PHASES.md`.
- Skills: `skills/engineering-management/security-story-checklist/SKILL.md`, `skills/engineering-management/definition_of_ready/SKILL.md`; optionally `skills/engineering-management/jira_architect/SKILL.md` for [SEC] story type

## Step 1: Read the epic and security bar

1. **Read** `epic-summary.md` and list all story tags. Identify which stories are [SEC] or touch security (auth, data access, PII, rate limiting, compliance).
2. **Read** security-story-checklist: AuthN, AuthZ/RBAC, data access, PII, rate limiting, input validation, compliance. Read definition_of_ready for the Security dimension and red flags.

## Step 2: Check for [SEC] coverage

1. Does the epic have at least one [SEC] story where the feature introduces new endpoints, new data access, or new user-facing auth? If the feature has no new auth/data surface, [SEC] may be N/A — document that.
2. For each [SEC] story, verify the description includes the checklist items (auth method, who is allowed, data scope, PII/compliance, rate limiting as applicable). If not, list gaps.

## Step 3: Check non-[SEC] stories for security scope

1. For [BE], [FE], [DB], [FF] stories: does any of them touch auth, permissions, PII, or compliance? If yes, either they should reference a [SEC] story or include explicit security AC (per security-story-checklist). List any story that touches security but has no security AC or [SEC] dependency.

## Step 4: Produce report and recommendations

1. Write a short report: **Epic:** &lt;name&gt;, **Phase:** &lt;phase&gt;. Sections: [SEC] coverage (yes/no/N/A), Checklist gaps per [SEC] story, Non-[SEC] stories with security scope (and whether AC/SEC ref exists), Recommendations (add [SEC] story, add AC to story X, or "No gaps").
2. Save to the epic folder, e.g. `YYYY-MM-DD_security-review.md`.
3. If gaps exist, suggest concrete edits (new [SEC] story, or AC bullets to add to existing stories).

## References

- Security checklist: `skills/engineering-management/security-story-checklist/SKILL.md`
- DoR: `skills/engineering-management/definition_of_ready/SKILL.md`
- Jira Architect [SEC]: `skills/engineering-management/jira_architect/SKILL.md`
- Conventions: `standards/conventions.md`
