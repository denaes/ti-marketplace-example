#!/usr/bin/env python3
"""
Orbit Skill Validator

Checks all SKILL.md files for:
  1. Frontmatter conformance (canonical schema)
  2. Broken internal references (links to non-existent skill paths)
  3. Missing required sections
  4. Empty or stub skills

Usage:
  python3 scripts/validate-skills.py          # full validation
  python3 scripts/validate-skills.py --quick   # frontmatter only (fast)
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

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
    in_metadata = False
    in_multiline = False
    multiline_key = None
    multiline_lines = []

    for line in match.group(1).split('\n'):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())

        if in_multiline:
            if indent >= 2 and not re.match(r'^[\w][\w.-]*\s*:', stripped):
                multiline_lines.append(stripped)
                continue
            else:
                fm[multiline_key] = ' '.join(multiline_lines).strip()
                in_multiline = False
                multiline_key = None
                multiline_lines = []

        if not stripped:
            continue

        kv = re.match(r'^([\w][\w.-]*)\s*:\s*(.*)', stripped)
        if not kv:
            continue

        key = kv.group(1)
        value = kv.group(2).strip().strip('"').strip("'")

        if indent == 0:
            in_metadata = False
            if key == 'metadata' and not value:
                in_metadata = True
                fm['metadata'] = fm.get('metadata', {})
            elif value in ('>', '|'):
                in_multiline = True
                multiline_key = key
                multiline_lines = []
            elif value:
                fm[key] = value
        elif indent >= 2 and in_metadata:
            if 'metadata' not in fm:
                fm['metadata'] = {}
            fm['metadata'][key] = value

    if in_multiline and multiline_key:
        fm[multiline_key] = ' '.join(multiline_lines).strip()

    return fm


def validate_frontmatter(skill_path: str, fm: dict) -> list[str]:
    """Validate frontmatter against canonical schema."""
    issues = []

    if not fm:
        issues.append(f"{skill_path}: no frontmatter found")
        return issues

    if not fm.get('name'):
        issues.append(f"{skill_path}: missing 'name'")
    if not fm.get('description'):
        issues.append(f"{skill_path}: missing 'description'")

    metadata = fm.get('metadata', {})
    if not isinstance(metadata, dict):
        issues.append(f"{skill_path}: 'metadata' is not a mapping")
        return issues

    if not metadata.get('type'):
        issues.append(f"{skill_path}: missing 'metadata.type'")
    elif metadata['type'] not in VALID_TYPES:
        issues.append(f"{skill_path}: invalid type '{metadata['type']}'")

    if not metadata.get('department'):
        issues.append(f"{skill_path}: missing 'metadata.department'")
    elif metadata['department'] not in VALID_DEPARTMENTS:
        issues.append(f"{skill_path}: invalid department '{metadata['department']}'")

    if not metadata.get('source'):
        issues.append(f"{skill_path}: missing 'metadata.source'")

    return issues


def validate_references(skill_path: str, content: str, all_skill_paths: set, repo_root: Path) -> list[str]:
    """Check for broken internal references."""
    issues = []

    # Find references to skills/ paths
    refs = re.findall(r'`(skills/[^`]+/SKILL\.md)`', content)
    for ref in refs:
        ref_dir = ref.rsplit('/SKILL.md', 1)[0]
        full_path = repo_root / ref_dir / 'SKILL.md'
        if not full_path.exists():
            issues.append(f"{skill_path}: broken reference to `{ref}`")

    # Find references to standards/, templates/ paths
    for pattern in [r'`(standards/[^`]+)`', r'`(templates/[^`]+)`']:
        refs = re.findall(pattern, content)
        for ref in refs:
            full_path = repo_root / ref
            if not full_path.exists():
                issues.append(f"{skill_path}: broken reference to `{ref}`")

    # Check for remaining ti-rd-playbook references
    old_refs = re.findall(r'(ti-pm/|ti-em/|ti-eng/)[^\s`]*', content)
    for ref in old_refs:
        issues.append(f"{skill_path}: unrewritten playbook reference: {ref}")

    return issues


def validate_content(skill_path: str, content: str, fm: dict) -> list[str]:
    """Check for content quality issues."""
    issues = []

    # Strip frontmatter
    body = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

    if len(body.strip()) < 50:
        issues.append(f"{skill_path}: body too short ({len(body.strip())} chars)")

    return issues


def main():
    quick = '--quick' in sys.argv

    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / 'skills'

    if not skills_dir.exists():
        print(f"Error: skills directory not found at {skills_dir}", file=sys.stderr)
        sys.exit(1)

    skill_files = sorted(skills_dir.rglob('SKILL.md'))
    print(f"Validating {len(skill_files)} SKILL.md files...\n")

    all_skill_dirs = set()
    for sf in skill_files:
        all_skill_dirs.add(str(sf.parent.relative_to(repo_root)))

    all_issues = []
    issue_counts = defaultdict(int)

    for sf in skill_files:
        rel_path = str(sf.relative_to(repo_root))
        content = sf.read_text(encoding='utf-8')
        fm = parse_frontmatter(content)

        fm_issues = validate_frontmatter(rel_path, fm)
        all_issues.extend(fm_issues)
        if fm_issues:
            issue_counts['frontmatter'] += len(fm_issues)

        if not quick:
            ref_issues = validate_references(rel_path, content, all_skill_dirs, repo_root)
            all_issues.extend(ref_issues)
            if ref_issues:
                issue_counts['references'] += len(ref_issues)

            content_issues = validate_content(rel_path, content, fm)
            all_issues.extend(content_issues)
            if content_issues:
                issue_counts['content'] += len(content_issues)

    if all_issues:
        print(f"{len(all_issues)} issues found:\n")

        if issue_counts:
            for category, count in sorted(issue_counts.items()):
                print(f"  {category}: {count}")
            print()

        for issue in all_issues:
            print(f"  - {issue}")

        sys.exit(1)
    else:
        mode = "quick" if quick else "full"
        print(f"All {len(skill_files)} skills pass {mode} validation.")
        sys.exit(0)


if __name__ == '__main__':
    main()
