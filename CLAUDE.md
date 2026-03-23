# Orbit

Unified AI skills library with 459 skills across 14 departments. This file is your entry point when working in this repo.

Read `skills/_bootstrap/using-orbit/SKILL.md` at session start -- it teaches you how to navigate departments, find skills, and follow the skill-before-action rule.

## Navigation

```
ti-marketplace-example/
├── skills/                  # All skills by department
│   ├── _bootstrap/          # Session bootstrap (using-orbit)
│   ├── engineering/         # TDD, debugging, code review, architecture, DevOps
│   ├── engineering-management/ # Epics, stories, capacity, releases, Jira workflows
│   ├── product/             # PRDs, discovery, strategy, execution, GTM, analytics
│   ├── design/              # Design consultation, review, design systems
│   ├── marketing/           # Content, SEO, email, social, copywriting, brand
│   ├── sales/               # Account exec, solutions architect, customer success
│   ├── data-analytics/      # Data analysis, BI, ML ops
│   ├── hr-people/           # Talent, people analytics, management
│   ├── finance/             # Financial analysis, budgeting
│   ├── executive/           # C-suite advisory (CEO, CTO, CFO, CMO, COO, CISO)
│   ├── operations/          # EOS framework, business growth, CRO
│   ├── compliance/          # GDPR, SOC 2, ISO, FDA, EU AI Act, NIS2, PCI-DSS
│   ├── project-management/  # Scrum, QA, release management
│   └── meta/                # Writing skills, verification
├── agents/                  # Agent definitions (orchestrate skills)
├── catalog/                 # Auto-generated skill indexes
├── docs/                    # Architecture, contributing, skill mapping
├── hooks/                   # Session-start hooks for bootstrap injection
├── memory/                  # Memory system (PARA + session tracking)
├── scripts/                 # Normalize, fix-references, validate
├── standards/               # Conventions, communication, git, quality, security
└── templates/               # Product, data, and workflow templates
```

## Skill Types

Skills have a `metadata.type` field in their frontmatter:

| Type | Purpose | Example |
|------|---------|---------|
| `skill` | Atomic domain knowledge and procedures | `test-driven-development`, `ti-write-prd` |
| `workflow` | Multi-skill orchestration recipe | `workflow-write-prd`, `workflow-write-story` |
| `command` | User-invokable entry point with argument hints | `command-sprint`, `command-discover` |

## Conventions

- Follow `standards/conventions.md` for output formatting, naming, and the "ask before deciding" rule
- Every skill has canonical frontmatter: `name`, `description`, `metadata.type`, `metadata.department`, `metadata.source`
- Templates live in `templates/product/` (PRD, HLD, impact estimation)
- Output files go to the user's `workspace/` directory (see conventions for structure)

## Development

```bash
# Normalize all frontmatter
python3 scripts/normalize-frontmatter.py

# Fix internal references
python3 scripts/fix-references.py

# Validate skill conformance
python3 scripts/validate-skills.py

# Regenerate catalog
python3 catalog/generate-catalog.py
```

## Adding a Skill

1. Create `skills/<department>/<skill-name>/SKILL.md`
2. Add canonical frontmatter (name, description, metadata block)
3. Write skill body: "When to Use", instructions, examples
4. Run `python3 scripts/validate-skills.py` to check conformance
5. Run `python3 catalog/generate-catalog.py` to update indexes
