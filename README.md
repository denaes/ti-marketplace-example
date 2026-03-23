# Orbit

Unified AI skills library with **459 production-ready skills** across **14 departments**. Engineering, product, marketing, design, sales, operations, compliance, and more -- all in one plugin, installable on any AI coding platform.

## Installation

**Note:** Installation differs by platform. Claude Code or Cursor have built-in plugin marketplaces. Codex and OpenCode require manual setup.

### Claude Code Official Marketplace

Orbit is not yet available via the [official Claude plugin marketplace](https://claude.com/plugins/superpowers) as it's really specific to Ti.
In a near future we could be working on a similar public repository. 

### Claude Code (via Plugin Marketplace)

In Claude Code, register the marketplace first:

```bash
/plugin marketplace add denaes/ti-marketplace-example
```

Then install the plugin from this marketplace:

```bash
/plugin install denaes/ti-marketplace-example
```
### Claude Cowork (Desktop)

1. Open **Settings > Plugins**
2. Click **Add Plugin** and paste: `https://github.com/denaes/ti-marketplace-example`
3. Restart the session

The plugin uses the same `.claude-plugin/` manifests as Claude Code.

### Gemini CLI

```bash
gemini extensions install https://github.com/denaes/ti-marketplace-example
```

Gemini reads `gemini-extension.json` and the `GEMINI.md` context file, which bootstraps the `using-orbit` skill.

### VS Code (with Copilot / Continue / other extensions)

Clone the repo and reference the skills directory:

```bash
git clone https://github.com/denaes/ti-marketplace-example.git ~/.vscode/orbit
```

Then configure your AI extension to load skills from `~/.vscode/orbit/skills/`. The exact setup depends on your extension:

- **GitHub Copilot**: Add the skills directory to your workspace, or reference skills in your `.github/copilot-instructions.md`
- **Continue**: Add orbit's skills directory to your Continue config

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md) for clone-and-symlink instructions.

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md) for `opencode.json` configuration.

## Departments

| Department | Skills | Focus |
|------------|--------|-------|
| **engineering** | 82 | TDD, debugging, code review, architecture, DevOps, security, AI/ML, databases |
| **engineering-management** | 48 | Epics, stories, capacity planning, releases, Jira workflows |
| **product** | 172 | Discovery, strategy, execution, GTM, market research, analytics, PRDs, OKRs |
| **design** | 3 | Design consultation, review, design systems |
| **marketing** | 36 | Content, SEO, email, social media, copywriting, brand strategy |
| **sales** | 6 | Account executive, solutions architect, customer success |
| **data-analytics** | 6 | Data analysis, BI, ML ops |
| **hr-people** | 5 | Talent acquisition, people analytics, people management |
| **finance** | 2 | Financial analysis, DCF, budgeting |
| **executive** | 28 | CEO, CTO, CFO, CMO, COO, CISO, CPO, CRO advisory |
| **operations** | 35 | EOS framework (18 skills), business growth, CRO |
| **compliance** | 22 | GDPR, SOC 2, ISO 13485, FDA, EU AI Act, NIS2, PCI-DSS |
| **project-management** | 11 | Scrum, release management, QA, sprint planning |
| **meta** | 3 | Writing skills, verification |

## Skill Types

| Type | Count | Purpose |
|------|-------|---------|
| `skill` | 427 | Atomic domain knowledge and procedures |
| `workflow` | 27 | Multi-skill orchestration recipes |
| `command` | 5 | User-invokable entry points with argument hints |

## Skill Format

Every skill lives in `skills/<department>/<skill-name>/SKILL.md` with canonical frontmatter:

```yaml
---
name: skill-name
description: When to use this skill and what it does
metadata:
  type: skill
  department: engineering
  source: superpowers
  version: "1.0"
---
```

## Project Structure

```
ti-marketplace-example/
├── skills/               # 459 skills organized by department
├── agents/               # Agent definitions that orchestrate skills
├── catalog/              # Auto-generated indexes (YAML + markdown)
├── hooks/                # Session-start hooks for each platform
├── memory/               # PARA + session tracking memory system
├── standards/            # Conventions, communication, git, quality, security
├── templates/            # Product, data, and workflow templates
├── scripts/              # normalize, fix-references, validate
├── .claude-plugin/       # Claude Code/Cowork plugin manifest
├── .cursor-plugin/       # Cursor plugin manifest
├── .cursor/rules/        # Cursor routing rules (.mdc)
├── .github/workflows/    # CI: frontmatter validation + catalog freshness
├── CLAUDE.md             # Claude Code developer guide
├── AGENTS.md             # Codex/general agent guide
└── GEMINI.md             # Gemini CLI context
```

## Development

```bash
# Validate all skill frontmatter (fast)
python3 scripts/validate-skills.py --quick

# Full validation (frontmatter + broken references)
python3 scripts/validate-skills.py

# Regenerate catalog
python3 catalog/generate-catalog.py

# Normalize frontmatter across all skills
python3 scripts/normalize-frontmatter.py --dry-run   # preview
python3 scripts/normalize-frontmatter.py              # apply

# Fix internal path references
python3 scripts/fix-references.py --dry-run
```

## Sources

Orbit consolidates skills from:

- **superpowers** (14 skills) -- Plugin architecture, TDD, debugging, collaboration workflows
- **Claude-Skills** (200 skills) -- Marketing, sales, executive, compliance, engineering
- **gstack** (12 skills) -- Code review, shipping, QA, design review, retros
- **ti-rd-playbook** (215 skills) -- PM workflows, engineering management, product discovery
- **ceos** (18 skills) -- EOS business framework (rocks, scorecard, L10, VTO)

## License

MIT
