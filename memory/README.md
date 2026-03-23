# Orbit Memory System

File-based persistent memory combining Tiago Forte's PARA method with session-aware
state management. Designed for AI agents that need to retain knowledge across sessions.

## Architecture

Three layers of memory, each serving a different purpose:

1. **Knowledge Graph** (`~/.orbit/life/`) -- PARA-organized entity storage with atomic YAML facts
2. **Daily Notes** (`~/.orbit/memory/`) -- Raw timeline of events
3. **Tacit Knowledge** (`~/.orbit/MEMORY.md`) -- User patterns and preferences

Plus two operational components:

4. **Session Tracking** (`~/.orbit/sessions/`) -- Active session awareness
5. **Per-Project State** (`~/.orbit/projects/`) -- Cross-session project data

## Sources

This system combines patterns from:

- **paperclip** -- PARA method, atomic fact schema, memory decay algorithm
- **gstack** -- Session tracking, per-project state, cross-skill data flow

## Usage

Load the `orbit-memory` skill to get the full specification. The skill covers when to
create entities, how to manage facts, session tracking, and memory recall patterns.
