# Skill Deduplication Notes

When skills from multiple sources cover similar ground, they are kept as complementary
alternatives. This document maps overlapping skills and explains which to prefer.

**ti-skills** (`skills/ti-skills/`) are not duplicates of `product/execution/ti-write-prd` and related TI playbook skills: *ti-skills* encode **public marketing / platform positioning**; playbook TI skills encode **internal product and delivery workflows** (PRDs, briefs, codebase patterns). Use both when the task spans positioning and implementation.

## Code Review

| Skill | Source | When to Use |
|-------|--------|-------------|
| `engineering/requesting-code-review` | superpowers | Dispatch a reviewer subagent with structured template |
| `engineering/receiving-code-review` | superpowers | Handle review feedback: technical evaluation, no performative agreement |
| `engineering/review` | gstack | Staff-engineer paranoid pre-landing PR review (2-pass) |
| `engineering/code-review-checklist` | playbook | Checklist-based review for story implementation |
| `engineering/code-reviewer` | Claude-Skills | General code quality, security, performance scoring |
| `engineering/pr-review-expert` | Claude-Skills | PR-specific review workflow |
| `engineering/api-design-reviewer` | Claude-Skills | API-specific design review |
| `design/design-review` | gstack | Visual audit on live site with fix loop |
| `design/plan-design-review` | gstack | Design review in plan mode (7 passes) |
| `engineering-management/plan-eng-review` | gstack | Eng manager architecture review |
| `executive/plan-ceo-review` | gstack | CEO/founder strategic review |

**Recommendation:** Use `engineering/review` (gstack) for comprehensive pre-landing reviews. Use
`engineering/requesting-code-review` (superpowers) for subagent-dispatched reviews. Use the
specialized variants for domain-specific reviews.

## Debugging

| Skill | Source | When to Use |
|-------|--------|-------------|
| `engineering/systematic-debugging` | superpowers | 4-phase root cause investigation (rigid process) |
| `engineering/debugging` | playbook | Practical debugging tied to Jira tickets |

**Recommendation:** Use `systematic-debugging` (superpowers) as the primary debugging skill -- it
is more rigorous and comprehensive. Use `debugging` (playbook) for quick Jira-linked bug fixes.

## Testing / TDD

| Skill | Source | When to Use |
|-------|--------|-------------|
| `engineering/test-driven-development` | superpowers | RED-GREEN-REFACTOR iron law (rigid) |
| `engineering/tdd-guide` | Claude-Skills | TDD best practices reference |
| `engineering/unit-testing-v3` | playbook | Jest/Sinon unit testing patterns |
| `engineering/e2e-playwright` | playbook | E2E Playwright test patterns |
| `engineering/qa` | gstack | QA lead: test + fix + verify loop |
| `engineering/qa-only` | gstack | QA reporter: report only, no fixes |
| `engineering/qa-browser-automation` | Claude-Skills | Browser automation for QA |
| `engineering/senior-qa` | Claude-Skills | Senior QA role persona |

**Recommendation:** Use `test-driven-development` (superpowers) for the TDD discipline. Use
`unit-testing-v3` / `e2e-playwright` (playbook) for specific testing tech. Use `qa` (gstack) for
full QA workflow.

## Brainstorming

| Skill | Source | When to Use |
|-------|--------|-------------|
| `product/discovery/brainstorming` | superpowers | Idea -> design through Socratic dialogue (general) |
| `product/discovery/brainstorm-ideas-existing` | playbook | Ideation for existing products |
| `product/discovery/brainstorm-ideas-new` | playbook | Ideation for new products |
| `product/discovery/brainstorm-experiments-existing` | playbook | Experiments for existing products |
| `product/discovery/brainstorm-experiments-new` | playbook | Pretotypes for new products |
| `product/execution/brainstorm-okrs` | playbook | Team-level OKR brainstorming |

**Recommendation:** Use `brainstorming` (superpowers) for general idea -> design flow. Use the
playbook variants for specific PM brainstorming contexts.

## Release Management

| Skill | Source | When to Use |
|-------|--------|-------------|
| `engineering-management/ship` | gstack | Full release engineer workflow (tests, bump, PR) |
| `engineering-management/document-release` | gstack | Post-ship documentation updates |
| `engineering/release-manager` | Claude-Skills | General release management |
| `engineering/release-orchestrator` | Claude-Skills | Release orchestration across teams |
| `engineering-management/release-milestone-gates` | playbook | Milestone gate checks |

**Recommendation:** Use `ship` (gstack) for actual shipping. Use `release-milestone-gates`
(playbook) for pre-release gate checks.

## Retro

| Skill | Source | When to Use |
|-------|--------|-------------|
| `engineering-management/retro` | gstack | Team-aware weekly retro with per-person breakdowns |
| `product/execution/retro` | playbook | Sprint retrospective facilitation |
| `project-management/sprint-retrospective` | Claude-Skills | General sprint retro framework |

**Recommendation:** Use `engineering-management/retro` (gstack) for team retros with history.
Use `product/execution/retro` (playbook) for sprint-focused retros.
