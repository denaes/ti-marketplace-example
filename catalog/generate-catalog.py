#!/usr/bin/env python3
"""
Orbit Catalog Generator

Scans all skills under skills/, parses YAML frontmatter from SKILL.md files,
and generates:
  - skills-index.yaml (machine-readable full index)
  - skills-by-department.md (human-readable by department)
  - skills-by-type.md (by type: skill, workflow, command)

Usage:
  python3 catalog/generate-catalog.py            # generate catalog
  python3 catalog/generate-catalog.py --validate  # validate frontmatter only
"""

import os
import re
import sys
from collections import defaultdict
from pathlib import Path


REQUIRED_FIELDS = {'name', 'description'}
EXPECTED_METADATA = {'type', 'department', 'source', 'version'}
VALID_TYPES = {'skill', 'workflow', 'command', 'agent'}
VALID_DEPARTMENTS = {
    'engineering', 'engineering-management', 'product', 'design',
    'marketing', 'sales', 'data-analytics', 'hr-people', 'finance',
    'executive', 'operations', 'compliance', 'project-management', 'meta',
    'ti-skills',
}


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown content."""
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}

    fm = {}
    current_key = None
    current_value = []
    in_multiline = False
    in_metadata = False

    for line in match.group(1).split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        indent = len(line) - len(line.lstrip())

        if in_multiline:
            if indent >= 2 and not re.match(r'^[\w][\w.-]*\s*:', stripped):
                current_value.append(stripped)
                continue
            else:
                fm[current_key] = ' '.join(current_value).strip()
                in_multiline = False

        kv = re.match(r'^([\w][\w.-]*)\s*:\s*(.*)', stripped)
        if not kv:
            continue

        key = kv.group(1)
        value = kv.group(2).strip().strip('"').strip("'")

        if indent == 0:
            in_metadata = False
            if key == 'metadata' and not value:
                in_metadata = True
                if 'metadata' not in fm:
                    fm['metadata'] = {}
            elif value == '>' or value == '|':
                current_key = key
                current_value = []
                in_multiline = True
            elif value.startswith('[') and value.endswith(']'):
                fm[key] = value
            else:
                fm[key] = value
        elif indent >= 2 and in_metadata:
            if 'metadata' not in fm:
                fm['metadata'] = {}
            fm['metadata'][key] = value

    if in_multiline and current_key:
        fm[current_key] = ' '.join(current_value).strip()

    return fm


def find_skills(skills_dir: Path) -> list[dict]:
    """Recursively find all SKILL.md files and extract metadata."""
    skills = []

    for skill_md in sorted(skills_dir.rglob('SKILL.md')):
        rel_path = skill_md.relative_to(skills_dir)
        parts = list(rel_path.parts)

        if len(parts) < 2:
            continue

        department = parts[0]
        if department == '_bootstrap':
            department = 'meta'

        skill_dir_name = parts[-2] if len(parts) >= 2 else parts[0]
        subdomain = '/'.join(parts[1:-2]) if len(parts) > 3 else (parts[1] if len(parts) == 3 else None)
        skill_path = str(rel_path.parent)

        try:
            content = skill_md.read_text(encoding='utf-8')
        except Exception:
            continue

        fm = parse_frontmatter(content)
        name = fm.get('name', skill_dir_name)
        description = fm.get('description', '')
        if not description:
            for line in content.split('\n'):
                if line.startswith('# '):
                    description = line[2:].strip()
                    break

        metadata = fm.get('metadata', {})
        if not isinstance(metadata, dict):
            metadata = {}

        skill_type = metadata.get('type', '')
        source = metadata.get('source', '')
        version = metadata.get('version', '')

        skills.append({
            'name': name,
            'department': department,
            'subdomain': subdomain,
            'path': f'skills/{skill_path}',
            'description': description,
            'type': skill_type,
            'source': source,
            'version': version,
            '_frontmatter': fm,
            '_file': str(skill_md),
        })

    return skills


def validate_skills(skills: list[dict]) -> list[str]:
    """Validate frontmatter conformance. Returns list of issues."""
    issues = []

    for s in skills:
        fm = s['_frontmatter']
        path = s['path']

        if not fm.get('name'):
            issues.append(f"{path}: missing 'name' in frontmatter")
        if not fm.get('description'):
            issues.append(f"{path}: missing 'description' in frontmatter")

        metadata = fm.get('metadata', {})
        if not isinstance(metadata, dict):
            issues.append(f"{path}: 'metadata' is not a mapping")
            continue

        if not metadata.get('type'):
            issues.append(f"{path}: missing 'metadata.type'")
        elif metadata['type'] not in VALID_TYPES:
            issues.append(f"{path}: invalid type '{metadata['type']}' (expected: {', '.join(sorted(VALID_TYPES))})")

        if not metadata.get('department'):
            issues.append(f"{path}: missing 'metadata.department'")
        elif metadata['department'] not in VALID_DEPARTMENTS:
            issues.append(f"{path}: invalid department '{metadata['department']}'")

        if not metadata.get('source'):
            issues.append(f"{path}: missing 'metadata.source'")

    return issues


def generate_yaml_index(skills: list[dict], output_path: Path):
    """Generate skills-index.yaml."""
    lines = ['# Orbit Skills Index', f'# Generated automatically - {len(skills)} skills', '']
    lines.append('skills:')

    for s in skills:
        lines.append(f'  - name: "{s["name"]}"')
        lines.append(f'    department: "{s["department"]}"')
        if s['subdomain']:
            lines.append(f'    subdomain: "{s["subdomain"]}"')
        lines.append(f'    path: "{s["path"]}"')
        if s['type']:
            lines.append(f'    type: "{s["type"]}"')
        if s['source']:
            lines.append(f'    source: "{s["source"]}"')
        desc = s['description'].replace('"', '\\"')
        lines.append(f'    description: "{desc}"')
        lines.append('')

    output_path.write_text('\n'.join(lines), encoding='utf-8')


def generate_by_department(skills: list[dict], output_path: Path):
    """Generate skills-by-department.md."""
    by_dept = defaultdict(list)
    for s in skills:
        by_dept[s['department']].append(s)

    lines = ['# Orbit Skills by Department', '', f'Total: **{len(skills)} skills** across **{len(by_dept)} departments**', '']

    dept_order = [
        'engineering', 'engineering-management', 'product', 'design',
        'marketing', 'sales', 'data-analytics', 'hr-people', 'finance',
        'executive', 'operations', 'compliance', 'project-management', 'meta'
    ]
    for dept in dept_order:
        if dept not in by_dept:
            continue
        dept_skills = by_dept[dept]
        lines.append(f'## {dept.replace("-", " ").title()} ({len(dept_skills)} skills)')
        lines.append('')
        lines.append('| Skill | Type | Path | Description |')
        lines.append('|-------|------|------|-------------|')
        for s in sorted(dept_skills, key=lambda x: x['name']):
            desc = s['description'][:150].replace('|', '\\|')
            stype = s['type'] or '-'
            lines.append(f'| {s["name"]} | {stype} | `{s["path"]}` | {desc} |')
        lines.append('')

    for dept in sorted(by_dept.keys()):
        if dept not in dept_order:
            dept_skills = by_dept[dept]
            lines.append(f'## {dept.replace("-", " ").title()} ({len(dept_skills)} skills)')
            lines.append('')
            lines.append('| Skill | Type | Path | Description |')
            lines.append('|-------|------|------|-------------|')
            for s in sorted(dept_skills, key=lambda x: x['name']):
                desc = s['description'][:150].replace('|', '\\|')
                stype = s['type'] or '-'
                lines.append(f'| {s["name"]} | {stype} | `{s["path"]}` | {desc} |')
            lines.append('')

    output_path.write_text('\n'.join(lines), encoding='utf-8')


def generate_by_type(skills: list[dict], output_path: Path):
    """Generate skills-by-type.md."""
    by_type = defaultdict(list)
    for s in skills:
        t = s['type'] if s['type'] else 'unclassified'
        by_type[t].append(s)

    type_order = ['skill', 'workflow', 'command', 'agent', 'unclassified']
    lines = ['# Orbit Skills by Type', '', f'Total: **{len(skills)} skills**', '']

    for t in type_order:
        if t not in by_type:
            continue
        type_skills = by_type[t]
        lines.append(f'## {t.title()} ({len(type_skills)})')
        lines.append('')
        lines.append('| Skill | Department | Source | Description |')
        lines.append('|-------|-----------|--------|-------------|')
        for s in sorted(type_skills, key=lambda x: (x['department'], x['name'])):
            desc = s['description'][:120].replace('|', '\\|')
            source = s['source'] or '-'
            lines.append(f'| {s["name"]} | {s["department"]} | {source} | {desc} |')
        lines.append('')

    for t in sorted(by_type.keys()):
        if t not in type_order:
            type_skills = by_type[t]
            lines.append(f'## {t.title()} ({len(type_skills)})')
            lines.append('')
            lines.append('| Skill | Department | Source | Description |')
            lines.append('|-------|-----------|--------|-------------|')
            for s in sorted(type_skills, key=lambda x: (x['department'], x['name'])):
                desc = s['description'][:120].replace('|', '\\|')
                source = s['source'] or '-'
                lines.append(f'| {s["name"]} | {s["department"]} | {source} | {desc} |')
            lines.append('')

    output_path.write_text('\n'.join(lines), encoding='utf-8')


def main():
    validate_only = '--validate' in sys.argv

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / 'skills'

    if not skills_dir.exists():
        print(f"Error: skills directory not found at {skills_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Scanning {skills_dir}...")
    skills = find_skills(skills_dir)
    print(f"Found {len(skills)} skills")

    by_dept = defaultdict(int)
    by_type = defaultdict(int)
    for s in skills:
        by_dept[s['department']] += 1
        by_type[s['type'] or 'unclassified'] += 1

    print(f"\nBy department:")
    for dept, count in sorted(by_dept.items()):
        print(f"  {dept}: {count}")

    print(f"\nBy type:")
    for t, count in sorted(by_type.items()):
        print(f"  {t}: {count}")

    if validate_only:
        print(f"\nValidating frontmatter...")
        issues = validate_skills(skills)
        if issues:
            print(f"\n{len(issues)} issues found:")
            for issue in issues:
                print(f"  - {issue}")
            sys.exit(1)
        else:
            print(f"\nAll {len(skills)} skills pass validation.")
            sys.exit(0)

    generate_yaml_index(skills, script_dir / 'skills-index.yaml')
    print(f"\nGenerated skills-index.yaml")

    generate_by_department(skills, script_dir / 'skills-by-department.md')
    print(f"Generated skills-by-department.md")

    generate_by_type(skills, script_dir / 'skills-by-type.md')
    print(f"Generated skills-by-type.md")


if __name__ == '__main__':
    main()
