# Changelog

All notable changes to Orbit will be documented in this file.

## [1.0.0] - 2026-03-18

### Added
- 459 skills across 14 departments (engineering, product, marketing, design, operations, compliance, etc.)
- Multi-platform support: Claude Code, Cursor, Gemini CLI, Codex, OpenCode
- Session-start hooks for automatic bootstrap skill injection
- Canonical frontmatter schema with `metadata.type`, `metadata.department`, `metadata.source`
- Catalog generator with YAML index, by-department, and by-type views
- Validation scripts for frontmatter conformance and broken reference detection
- Memory system combining PARA method and session tracking
- Standards for conventions, communication, git, quality, security
- Product templates (PRD, HLD, impact estimation)
- Cursor routing rules (`.cursor/rules/`) for department-based skill discovery
- Root CLAUDE.md and AGENTS.md for developer onboarding

### Sources
- superpowers (14 skills) -- plugin structure, TDD, debugging
- Claude-Skills (200 skills) -- marketing, sales, executive, compliance
- gstack (12 skills) -- code review, shipping, QA, design review
- ti-rd-playbook (215 skills) -- PM workflows, engineering management
- ceos (18 skills) -- EOS business framework
