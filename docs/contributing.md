# Contributing to Orbit

## Adding a New Skill

1. **Choose the right department** -- use `catalog/skills-by-department.md` and `scripts/validate-skills.py` (`VALID_DEPARTMENTS`). In this repo, product work lives under **`skills/product/<product-*-subdomain>/<skill-name>/`**. Thought Industries **positioning** skills use **`metadata.department: ti-skills`** and typically live at **`skills/ti-<skill-name>/`** (one folder per skill under `skills/`, not under `ti-skills/`).
2. **Create the skill directory** -- `skills/product/product-execution/my-skill/` or `skills/ti-my-positioning-skill/` (follow existing naming patterns).
3. **Write SKILL.md** with proper frontmatter (must match `scripts/validate-skills.py`):

```yaml
---
name: your-skill-name
description: >
  Use when [trigger conditions]. [What it does in one sentence].
metadata:
  type: skill
  department: engineering
  source: original
  version: "1.0"
---
```

4. **Follow the body structure:**
   - Overview (1-2 sentences)
   - When to Use (trigger conditions, symptoms)
   - The Process (step-by-step, with DOT flowcharts if complex)
   - Common Mistakes / Red Flags (optional)
   - Integration Notes (related skills)

5. **Add supporting files** as needed:
   - `references/` -- knowledge bases, frameworks
   - `scripts/` -- Python CLI tools (standard library only, no pip deps)
   - `assets/` -- templates, sample data

6. **Validate and regenerate the catalog:**
   ```bash
   python3 scripts/validate-skills.py --quick
   python3 catalog/generate-catalog.py
   ```

## Skill Design Principles

- **Description = trigger conditions only.** Don't summarize the workflow in the description. The description tells the agent *when* to load the skill, not *what* it does.
- **Rigid skills** (TDD, debugging, compliance) use absolute language and rationalizations tables.
- **Flexible skills** (advisory, patterns) provide principles to adapt.
- **No inter-skill dependencies** -- each skill stands alone.
- **Standard library Python only** -- scripts must work without pip install.

## Updating the Catalog

After adding or modifying skills, validate frontmatter then regenerate:

```bash
python3 scripts/validate-skills.py --quick
python3 catalog/generate-catalog.py
```

This updates:
- `catalog/skills-index.yaml`
- `catalog/skills-by-department.md`
- `catalog/skills-by-type.md`
