# Orbit -- Agent Guide

Read this file first when contributing to or working within this repository.

## What is Orbit?

A unified AI skills library with 459 skills across 14 departments (engineering, product, marketing, design, operations, etc.). Skills are organized under `skills/<department>/` and use a standardized SKILL.md format with YAML frontmatter.

## Repo Map

| Path | Purpose |
|------|---------|
| `skills/` | All skills organized by department and subdomain |
| `skills/_bootstrap/using-orbit/` | Bootstrap skill -- read this to understand how to navigate and use skills |
| `agents/` | Agent definitions that orchestrate multiple skills |
| `catalog/` | Auto-generated indexes: `skills-index.yaml`, `skills-by-department.md`, `skills-by-type.md` |
| `standards/` | Shared conventions for output, naming, quality |
| `templates/` | Reusable templates (product briefs, HLDs, workflows, data) |
| `memory/` | Memory system combining PARA method and session tracking |
| `scripts/` | Maintenance scripts: normalize frontmatter, fix references, validate |
| `hooks/` | Session-start hooks for each supported platform |
| `docs/` | Architecture, contributing guide, skill mapping from source repos |

## Skill Format

Every skill is a `SKILL.md` file with this canonical frontmatter:

```yaml
---
name: skill-name
description: When to use this skill and what it does
metadata:
  type: skill | workflow | command
  department: engineering | product | marketing | ...
  source: superpowers | gstack | ti-rd-playbook | claude-skills | ceos
  version: "1.0"
---
```

The body contains: overview, "When to Use" triggers, step-by-step instructions, and examples.

## Working in This Repo

### Before making changes

1. Read `standards/conventions.md` for naming, formatting, and quality rules
2. Read `docs/contributing.md` for the full contribution guide
3. Run `python3 scripts/validate-skills.py` to check current state

### Adding a skill

1. Create `skills/<department>/<skill-name>/SKILL.md`
2. Use canonical frontmatter (see format above)
3. Include "When to Use" section with trigger phrases
4. Run validate + catalog regeneration:
   ```bash
   python3 scripts/validate-skills.py
   python3 catalog/generate-catalog.py
   ```

### Testing

- Validate frontmatter: `python3 scripts/validate-skills.py`
- Regenerate catalog: `python3 catalog/generate-catalog.py`
- Normalize frontmatter: `python3 scripts/normalize-frontmatter.py --dry-run`

## Conventions

- **Ask before deciding**: When creating output for users, ask clarifying questions first
- **Codebase-first**: Search existing code before proposing solutions
- **No hard deletes**: Archive or deprecate, never delete
- **Skill-before-action**: Check if a relevant skill exists before taking action
- **Cross-reference by ID**: Use ticket IDs, not file names
