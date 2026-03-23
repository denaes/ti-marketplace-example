#!/usr/bin/env python3
"""
Fix broken ti-rd-playbook path references in orbit SKILL.md files.

Rewrites:
  ti-pm/skills/<name>/SKILL.md   → skills/product/.../<name>/SKILL.md (orbit path)
  ti-em/skills/<name>/SKILL.md   → skills/engineering-management/<name>/SKILL.md
  ti-eng/skills/<name>/SKILL.md  → skills/engineering/<name>/SKILL.md
  ti-pm/.agents/workflows/<x>.md → skills/product/product-execution/workflow-<x>/SKILL.md
  ti-em/.agents/workflows/<x>.md → skills/engineering-management/workflow-<x>/SKILL.md
  ti-pm/commands/<x>.md          → skills/product/product-execution/command-<x>/SKILL.md
  docs/CONVENTIONS.md            → standards/conventions.md
  docs/templates/<x>             → templates/product/<x>
"""

import re
import sys
from pathlib import Path


WORKFLOW_ALIASES = {
    'workflow-write-prd-product-brief': 'workflow-write-prd',
    'workflow-roadmap-and-release-planning': 'workflow-guide-me-to-roadmap-and-release-planning',
    'workflow-create-story': 'workflow-write-story',
    'workflow-generate-epics-and-stories': 'workflow-write-epics-and-stories-from-prd',
    'workflow-sprint-capacity-plan': 'workflow-write-sprint-capacity-plan',
    'workflow-push-to-jira': 'workflow-sync-local-to-jira',
    'workflow-compare-prd-to-jira': 'workflow-sync-compare-local-to-jira',
}


def build_skill_lookup(skills_dir: Path) -> dict[str, str]:
    """Build mapping from skill directory name to orbit-relative path."""
    lookup = {}
    for skill_md in skills_dir.rglob('SKILL.md'):
        skill_dir = skill_md.parent
        dir_name = skill_dir.name
        rel_path = str(skill_md.relative_to(skills_dir.parent))
        if dir_name not in lookup:
            lookup[dir_name] = rel_path

    for alias, target in WORKFLOW_ALIASES.items():
        if target in lookup and alias not in lookup:
            lookup[alias] = lookup[target]

    return lookup


def fix_file(filepath: Path, lookup: dict[str, str], dry_run: bool = False) -> list[str]:
    """Fix references in a single file. Returns list of changes made."""
    content = filepath.read_text(encoding='utf-8')
    original = content
    changes = []

    # ti-pm/skills/<name>/SKILL.md → orbit path
    def replace_ti_pm_skill(m):
        name = m.group(1)
        orbit_path = lookup.get(name)
        if orbit_path:
            changes.append(f"  ti-pm/skills/{name}/SKILL.md → {orbit_path}")
            return orbit_path
        return m.group(0)

    content = re.sub(r'ti-pm/skills/([\w-]+)/SKILL\.md', replace_ti_pm_skill, content)

    # ti-em/skills/<name>/SKILL.md → orbit path
    def replace_ti_em_skill(m):
        name = m.group(1)
        orbit_path = lookup.get(name)
        if orbit_path:
            changes.append(f"  ti-em/skills/{name}/SKILL.md → {orbit_path}")
            return orbit_path
        return m.group(0)

    content = re.sub(r'ti-em/skills/([\w-]+)/SKILL\.md', replace_ti_em_skill, content)

    # ti-eng/skills/<name>/SKILL.md → orbit path
    def replace_ti_eng_skill(m):
        name = m.group(1)
        orbit_path = lookup.get(name)
        if orbit_path:
            changes.append(f"  ti-eng/skills/{name}/SKILL.md → {orbit_path}")
            return orbit_path
        return m.group(0)

    content = re.sub(r'ti-eng/skills/([\w-]+)/SKILL\.md', replace_ti_eng_skill, content)

    # ti-pm/.agents/workflows/<x>.md → orbit workflow skill
    def replace_ti_pm_workflow(m):
        name = m.group(1)
        wf_name = f"workflow-{name}"
        orbit_path = lookup.get(wf_name)
        if orbit_path:
            changes.append(f"  ti-pm/.agents/workflows/{name}.md → {orbit_path}")
            return orbit_path
        return m.group(0)

    content = re.sub(r'ti-pm/\.agents/workflows/([\w-]+)\.md', replace_ti_pm_workflow, content)

    # ti-em/.agents/workflows/<x>.md → orbit workflow skill
    def replace_ti_em_workflow(m):
        name = m.group(1)
        wf_name = f"workflow-{name}"
        orbit_path = lookup.get(wf_name)
        if orbit_path:
            changes.append(f"  ti-em/.agents/workflows/{name}.md → {orbit_path}")
            return orbit_path
        return m.group(0)

    content = re.sub(r'ti-em/\.agents/workflows/([\w-]+)\.md', replace_ti_em_workflow, content)

    # ti-pm/commands/<x>.md → orbit command skill
    def replace_ti_pm_command(m):
        name = m.group(1)
        cmd_name = f"command-{name}"
        orbit_path = lookup.get(cmd_name)
        if orbit_path:
            changes.append(f"  ti-pm/commands/{name}.md → {orbit_path}")
            return orbit_path
        return m.group(0)

    content = re.sub(r'ti-pm/commands/([\w-]+)\.md', replace_ti_pm_command, content)

    # docs/CONVENTIONS.md → standards/conventions.md
    if 'docs/CONVENTIONS.md' in content:
        content = content.replace('docs/CONVENTIONS.md', 'standards/conventions.md')
        changes.append("  docs/CONVENTIONS.md → standards/conventions.md")

    # docs/templates/ references → templates/product/
    # These names often contain spaces and brackets, e.g. "Product Brief [TEMPLATE].md"
    def replace_docs_template(m):
        template_name = m.group(1)
        changes.append(f"  docs/templates/{template_name} → templates/product/{template_name}")
        return f'templates/product/{template_name}'

    content = re.sub(r'docs/templates/((?:[^`\n])+?)(?=`|\n|$)', replace_docs_template, content)

    # ti-pm/skills/ (bare directory reference without specific skill)
    if 'ti-pm/skills/' in content:
        content = content.replace('ti-pm/skills/', 'skills/product/')
        changes.append("  ti-pm/skills/ → skills/product/")

    if 'ti-em/skills/' in content:
        content = content.replace('ti-em/skills/', 'skills/engineering-management/')
        changes.append("  ti-em/skills/ → skills/engineering-management/")

    if 'ti-eng/skills/' in content:
        content = content.replace('ti-eng/skills/', 'skills/engineering/')
        changes.append("  ti-eng/skills/ → skills/engineering/")

    if content != original and not dry_run:
        filepath.write_text(content, encoding='utf-8')

    return changes


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / 'skills'

    if not skills_dir.exists():
        print(f"Error: skills directory not found at {skills_dir}", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print("DRY RUN - no files will be modified\n")

    lookup = build_skill_lookup(skills_dir)
    print(f"Built lookup: {len(lookup)} skill paths\n")

    total_files = 0
    total_changes = 0
    files_changed = 0

    for md_file in sorted(skills_dir.rglob('*.md')):
        changes = fix_file(md_file, lookup, dry_run)
        if changes:
            total_files += 1
            files_changed += 1
            total_changes += len(changes)
            rel = md_file.relative_to(repo_root)
            if verbose:
                print(f"{rel}:")
                for c in changes:
                    print(c)
                print()

    print(f"Summary:")
    print(f"  Files changed: {files_changed}")
    print(f"  Total replacements: {total_changes}")


if __name__ == '__main__':
    main()
