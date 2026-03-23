#!/usr/bin/env python3
"""
Normalize SKILL.md frontmatter across all orbit skills to the canonical schema.

Canonical schema:
  name: skill-name
  description: One-line description
  metadata:
    type: skill | workflow | command | agent
    department: engineering | product | ...
    source: superpowers | gstack | ti-rd-playbook | claude-skills | ceos
    version: "1.0"

Preserves existing name, description, file-access, tools-used, argument-hint.
Infers department from path, type from naming convention, source from heuristics.
"""

import os
import re
import sys
from pathlib import Path

SUPERPOWERS_SKILLS = {
    'brainstorming', 'dispatching-parallel-agents', 'executing-plans',
    'finishing-a-development-branch', 'receiving-code-review',
    'requesting-code-review', 'subagent-driven-development',
    'systematic-debugging', 'test-driven-development', 'using-git-worktrees',
    'using-orbit', 'verification-before-completion', 'writing-plans',
    'writing-skills',
}

GSTACK_SKILLS = {
    'design-consultation', 'design-review', 'document-release',
    'plan-ceo-review', 'plan-design-review', 'plan-eng-review',
    'qa', 'qa-only', 'retro', 'review', 'ship',
}

DEPARTMENTS = [
    'engineering', 'engineering-management', 'product', 'design',
    'marketing', 'sales', 'data-analytics', 'hr-people', 'finance',
    'executive', 'operations', 'compliance', 'project-management', 'meta',
]


def parse_frontmatter_raw(content: str) -> tuple[str, str, str]:
    """Split content into (pre-frontmatter, frontmatter-body, post-frontmatter).

    Returns ('', '', content) if no frontmatter found.
    """
    match = re.match(r'^(---\s*\n)(.*?\n)(---\s*\n)', content, re.DOTALL)
    if not match:
        return '', '', content
    return match.group(1), match.group(2), content[match.end():]


def parse_yaml_simple(text: str) -> dict:
    """Minimal YAML parser for flat and one-level-nested key-value pairs."""
    result = {}
    current_parent = None

    for line in text.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue

        indent = len(line) - len(line.lstrip())

        kv = re.match(r'^(\s*)([\w][\w.-]*)\s*:\s*(.*)', line)
        if not kv:
            continue

        key = kv.group(2)
        value = kv.group(3).strip().strip('"').strip("'")

        if indent == 0:
            if not value:
                current_parent = key
                if key not in result:
                    result[key] = {}
            else:
                current_parent = None
                if value.startswith('[') and value.endswith(']'):
                    result[key] = value
                else:
                    result[key] = value
        elif indent >= 2 and current_parent:
            if isinstance(result.get(current_parent), dict):
                if value.startswith('[') and value.endswith(']'):
                    result[current_parent][key] = value
                else:
                    result[current_parent][key] = value

    return result


def infer_department(skill_path: Path, skills_root: Path) -> str:
    """Infer department from the directory path."""
    rel = skill_path.relative_to(skills_root)
    parts = list(rel.parts)
    if not parts:
        return 'meta'
    dept = parts[0]
    if dept == '_bootstrap':
        return 'meta'
    return dept


def infer_type(dir_name: str, fm: dict) -> str:
    """Infer skill type from directory name and frontmatter hints."""
    if dir_name.startswith('workflow-'):
        return 'workflow'
    if dir_name.startswith('command-'):
        return 'command'
    if fm.get('argument-hint'):
        return 'command'
    if isinstance(fm.get('metadata'), dict) and fm['metadata'].get('type'):
        return fm['metadata']['type']
    return 'skill'


def infer_source(dir_name: str, department: str, fm: dict, skill_path: Path = None) -> str:
    """Infer the original source repository."""
    if dir_name in SUPERPOWERS_SKILLS:
        return 'superpowers'
    if dir_name in GSTACK_SKILLS:
        return 'gstack'
    if department == 'operations' and 'eos' in str(dir_name):
        return 'ceos'

    existing_meta = fm.get('metadata', {})
    if isinstance(existing_meta, dict):
        if existing_meta.get('source'):
            return existing_meta['source']
        if existing_meta.get('author') == 'borghei':
            return 'claude-skills'
        if existing_meta.get('category'):
            return 'claude-skills'

    if fm.get('license'):
        return 'claude-skills'
    if fm.get('file-access') or fm.get('tools-used'):
        return 'ceos'

    playbook_depts = {'engineering-management', 'product'}
    playbook_prefixes = ('ti-', 'workflow-', 'command-')
    if department in playbook_depts and any(dir_name.startswith(p) for p in playbook_prefixes):
        return 'ti-rd-playbook'

    playbook_product_skills = {
        'brainstorm-okrs', 'create-prd', 'define-jtbd-canvas',
        'define-problem-statement', 'deliver-edge-cases', 'deliver-launch-checklist',
        'deliver-prd', 'deliver-release-notes', 'deliver-user-stories',
        'develop-adr', 'develop-design-rationale', 'develop-solution-brief',
        'develop-spike-summary', 'discover-interview-synthesis',
        'discover-stakeholder-summary', 'dummy-dataset', 'eol-message',
        'epic-breakdown-advisor', 'epic-hypothesis', 'foundation-persona',
        'init-project', 'init-project-jpkb', 'iterate-lessons-log',
        'iterate-pivot-decision', 'iterate-refinement-notes',
        'iterate-retrospective', 'job-stories', 'outcome-roadmap',
        'prd-development', 'pre-mortem', 'press-release',
        'prioritization-frameworks', 'repo-self-update',
    }
    if dir_name in playbook_product_skills:
        return 'ti-rd-playbook'

    playbook_em_skills = {
        'api-contract-spec', 'bug-story-writer', 'capacity-planning',
        'cursor-prompt-builder', 'definition-of-ready', 'dependency-mapper',
        'epic-stakeholder-summary', 'epic-summary-writer',
        'jira-epic-folder-matcher', 'jira-labels-and-metadata',
        'propose-reporting-category-from-sheet', 'release-milestone-gates',
        'security-story-checklist', 'story-estimation', 'story-splitting',
        'sync-report-writer', 'sync-reporting-category-from-sheet',
        'workspace-epic-scanner',
    }
    if dir_name in playbook_em_skills:
        return 'ti-rd-playbook'

    playbook_eng_skills = {
        'code-review-checklist', 'codebase-navigation', 'e2e-playwright',
        'implementation-from-story', 'jira-ticket-context', 'spike-summary',
        'unit-testing-v3',
    }
    if dir_name in playbook_eng_skills:
        return 'ti-rd-playbook'

    if department == 'operations' and skill_path and 'business-growth' in str(skill_path):
        return 'claude-skills'

    if department == 'product':
        return 'ti-rd-playbook'

    if department == 'engineering-management':
        return 'ti-rd-playbook'

    if department in {'marketing', 'sales', 'data-analytics', 'hr-people',
                      'finance', 'executive', 'compliance', 'project-management'}:
        return 'claude-skills'

    if department == 'engineering':
        return 'claude-skills'

    return ''


def infer_subdomain(skill_path: Path, skills_root: Path) -> str:
    """Detect if the skill is in a subdomain (e.g., product/product-discovery)."""
    rel = skill_path.relative_to(skills_root)
    parts = list(rel.parts)
    if len(parts) >= 3:
        return parts[1]
    return ''


def build_frontmatter(fm: dict, department: str, skill_type: str, source: str,
                       dir_name: str) -> str:
    """Build the canonical frontmatter string."""
    lines = ['---']

    name = fm.get('name', dir_name)
    lines.append(f'name: {name}')

    desc = fm.get('description', '')
    if '\n' in desc or len(desc) > 120:
        lines.append(f'description: >')
        for chunk in _wrap_description(desc):
            lines.append(f'  {chunk}')
    else:
        lines.append(f'description: {desc}')

    if fm.get('argument-hint'):
        lines.append(f'argument-hint: "{fm["argument-hint"]}"')

    if fm.get('file-access'):
        lines.append(f'file-access: {fm["file-access"]}')
    if fm.get('tools-used'):
        lines.append(f'tools-used: {fm["tools-used"]}')

    lines.append('metadata:')
    lines.append(f'  type: {skill_type}')
    lines.append(f'  department: {department}')
    if source:
        lines.append(f'  source: {source}')
    lines.append(f'  version: "1.0"')

    lines.append('---')
    return '\n'.join(lines) + '\n'


def _wrap_description(text: str, width: int = 100) -> list[str]:
    """Wrap long description text."""
    text = text.replace('\n', ' ').strip()
    words = text.split()
    result_lines = []
    current = []
    length = 0
    for w in words:
        if length + len(w) + 1 > width and current:
            result_lines.append(' '.join(current))
            current = [w]
            length = len(w)
        else:
            current.append(w)
            length += len(w) + 1
    if current:
        result_lines.append(' '.join(current))
    return result_lines


def normalize_skill(skill_md: Path, skills_root: Path, dry_run: bool = False) -> dict:
    """Normalize a single SKILL.md. Returns a status dict."""
    content = skill_md.read_text(encoding='utf-8')
    opener, fm_body, body = parse_frontmatter_raw(content)

    dir_name = skill_md.parent.name
    department = infer_department(skill_md.parent, skills_root)

    if fm_body:
        fm = parse_yaml_simple(fm_body)
    else:
        fm = {}
        first_heading = ''
        for line in content.split('\n'):
            if line.startswith('# '):
                first_heading = line[2:].strip()
                break
        if first_heading:
            fm['name'] = dir_name
            fm['description'] = first_heading

    if not fm.get('name'):
        fm['name'] = dir_name

    skill_type = infer_type(dir_name, fm)
    source = infer_source(dir_name, department, fm, skill_md)

    new_fm = build_frontmatter(fm, department, skill_type, source, dir_name)
    new_content = new_fm + body

    status = {
        'path': str(skill_md.relative_to(skills_root.parent)),
        'name': fm.get('name', dir_name),
        'department': department,
        'type': skill_type,
        'source': source,
        'had_frontmatter': bool(fm_body),
        'changed': new_content != content,
    }

    if not dry_run and new_content != content:
        skill_md.write_text(new_content, encoding='utf-8')

    return status


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

    skill_files = sorted(skills_dir.rglob('SKILL.md'))
    print(f"Found {len(skill_files)} SKILL.md files\n")

    stats = {'total': 0, 'changed': 0, 'no_frontmatter': 0, 'by_type': {}, 'by_source': {}, 'by_dept': {}}

    for sf in skill_files:
        result = normalize_skill(sf, skills_dir, dry_run)
        stats['total'] += 1
        if result['changed']:
            stats['changed'] += 1
        if not result['had_frontmatter']:
            stats['no_frontmatter'] += 1

        stats['by_type'][result['type']] = stats['by_type'].get(result['type'], 0) + 1
        stats['by_source'][result['source'] or 'unknown'] = stats['by_source'].get(result['source'] or 'unknown', 0) + 1
        stats['by_dept'][result['department']] = stats['by_dept'].get(result['department'], 0) + 1

        if verbose:
            marker = '[CHANGED]' if result['changed'] else '[OK]'
            print(f"  {marker} {result['path']} -> type={result['type']}, source={result['source']}, dept={result['department']}")

    print(f"\nSummary:")
    print(f"  Total:   {stats['total']}")
    print(f"  Changed: {stats['changed']}")
    print(f"  Had no frontmatter: {stats['no_frontmatter']}")

    print(f"\nBy type:")
    for t, c in sorted(stats['by_type'].items()):
        print(f"  {t}: {c}")

    print(f"\nBy source:")
    for s, c in sorted(stats['by_source'].items()):
        print(f"  {s}: {c}")

    print(f"\nBy department:")
    for d, c in sorted(stats['by_dept'].items()):
        print(f"  {d}: {c}")


if __name__ == '__main__':
    main()
