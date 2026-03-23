---
name: orbit-memory
description: >
  File-based memory system using PARA method with session tracking. Use when you need
  to store, retrieve, update, or organize knowledge across sessions. Covers three
  memory layers: knowledge graph in PARA folders, daily notes, and tacit knowledge.
  Also handles session tracking, per-project state, and memory decay. Trigger on any
  memory operation: saving facts, writing daily notes, recalling context, or managing plans.
metadata:
  version: 1.0.0
  department: meta
  type: rigid
  source: paperclip+gstack
---

# Orbit Memory System

Persistent, file-based memory combining PARA organization with session-aware state management. All paths are relative to `~/.orbit/`.

## Three Memory Layers

### Layer 1: Knowledge Graph (`~/.orbit/life/` -- PARA)

Entity-based storage. Each entity gets a folder with two tiers:

1. `summary.md` -- quick context, load first.
2. `items.yaml` -- atomic facts, load on demand.

```text
~/.orbit/life/
  projects/          # Active work with clear goals/deadlines
    <name>/
      summary.md
      items.yaml
  areas/             # Ongoing responsibilities, no end date
    people/<name>/
    companies/<name>/
  resources/         # Reference material, topics of interest
    <topic>/
  archives/          # Inactive items from the other three
  index.md
```

**PARA rules:**

- **Projects** -- active work with a goal or deadline. Move to archives when complete.
- **Areas** -- ongoing (people, companies, responsibilities). No end date.
- **Resources** -- reference material, topics of interest.
- **Archives** -- inactive items from any category.

**Fact rules:**

- Save durable facts immediately to `items.yaml`.
- Weekly: rewrite `summary.md` from active facts.
- Never delete facts. Supersede instead (`status: superseded`, add `superseded_by`).
- When an entity goes inactive, move its folder to `~/.orbit/life/archives/`.

**When to create an entity:**

- Mentioned 3+ times, OR
- Direct relationship to the user (family, coworker, partner, client), OR
- Significant project or company in the user's life.
- Otherwise, note it in daily notes.

For the atomic fact YAML schema and memory decay rules, see [references/schemas.md](references/schemas.md).

### Layer 2: Daily Notes (`~/.orbit/memory/YYYY-MM-DD.md`)

Raw timeline of events -- the "when" layer.

- Write continuously during conversations.
- Extract durable facts to Layer 1 during heartbeats.

### Layer 3: Tacit Knowledge (`~/.orbit/MEMORY.md`)

How the user operates -- patterns, preferences, lessons learned.

- Not facts about the world; facts about the user.
- Update whenever you learn new operating patterns.

## Session Tracking

Track active sessions for context awareness:

```text
~/.orbit/sessions/$PPID    # Touch file to mark active session
```

- Files modified within the last 2 hours are active sessions.
- When 3+ concurrent sessions exist, provide fuller context in every response.
- Session tracking enables cross-session awareness without shared state.

## Per-Project State

Store project-specific data that persists across sessions:

```text
~/.orbit/projects/{repo-slug}/
  plans/            # CEO plans, engineering plans
  reviews/          # Review logs and gate overrides
  reports/          # QA reports, design reports
  test-plans/       # Test plan artifacts from engineering review
```

- Use `git remote` to derive the repo slug.
- Cross-skill data flows through these directories (e.g., engineering review writes test plans that QA reads).

## Write It Down -- No Mental Notes

Memory does not survive session restarts. Files do.

- Want to remember something -> WRITE IT TO A FILE.
- "Remember this" -> update `~/.orbit/memory/YYYY-MM-DD.md` or the relevant entity file.
- Learn a lesson -> update AGENTS.md, TOOLS.md, or the relevant skill file.
- Make a mistake -> document it so future-you does not repeat it.
- On-disk text files are always better than holding it in temporary context.

## Memory Recall

Search memory files using your platform's search tools:

```bash
grep -r "search term" ~/.orbit/life/
grep -r "search term" ~/.orbit/memory/
```

Or use `qmd` if available:

```bash
qmd query "what happened at Christmas"   # Semantic search with reranking
qmd search "specific phrase"              # BM25 keyword search
qmd index ~/.orbit                        # Index your memory folder
```

## Planning

Keep plans in timestamped files in `~/.orbit/projects/{repo}/plans/`. Plans go stale -- if a newer plan exists, do not confuse yourself with an older version. If you notice staleness, update the file to note what it is superseded by.
