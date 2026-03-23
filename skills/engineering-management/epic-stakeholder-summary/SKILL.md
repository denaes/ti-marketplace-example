---
name: epic-stakeholder-summary
description: >
  One-pager format for product/leadership—epic scope, story count, risks, timeline. Use when
  communicating epic status or scope outside the backlog.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Epic Stakeholder Summary

## Purpose

Define a **one-pager format** for product and leadership: epic scope, story count, risks, and timeline. Not the full epic-summary or backlog; a short narrative for prioritization and roadmap.

## When to Use

- When communicating epic status or scope to **stakeholders outside the backlog** (product, leadership, other teams)
- When preparing a **roadmap slot** or release note
- When answering "what's in this epic?" in a meeting or email

## Required Content (one page max)

| Section | Content |
|---------|---------|
| **Epic name** | Same as epic-summary title. |
| **Objective** | 1–2 sentences: what we ship and why (business outcome). |
| **Scope** | Bullets: main capabilities or themes (3–5). No full story list. |
| **Story count** | Total stories; optional breakdown (e.g. 8 backend, 3 frontend, 2 QA). |
| **Story points** | Total (non-deferred). Optional: "~2 sprints" if velocity is known. |
| **Risks / blockers** | 1–3 bullets: technical risk, dependency on another team, open decision. |
| **Timeline** | Phase (Alpha/Beta/GA) and target date or quarter if set. |

## Optional

- **Out of scope:** What we are not doing in this epic (reduces scope creep).
- **Dependencies on other epics:** "Blocked by TI-3xxx (Auth v2) until …"

## Format

Use markdown or a short doc. Keep to **one page**; link to full epic-summary or Jira epic for details.

```markdown
# Epic: [Name] — Stakeholder summary

**Objective:** [1–2 sentences]

**Scope**
- [Capability 1]
- [Capability 2]
- …

**Size:** [N] stories, [X] story points. Target: [Phase] [date/quarter].

**Risks / blockers**
- [Risk 1]
- …

**Timeline:** [Phase], [date or TBD]
```

## References

- **Epic summary (full):** `skills/engineering-management/epic-summary-writer/SKILL.md`
- **Epic folder:** `workspace/projects/<slug>/epics/`
