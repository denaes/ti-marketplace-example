#!/usr/bin/env python3
"""
Fix skills with empty descriptions by extracting from body content.

Handles the case where `description: >` was written with no content
below it (metadata block intercepted the multiline block).
"""

import re
import sys
from pathlib import Path


def fix_skill(skill_md: Path, dry_run: bool = False) -> bool:
    """Fix empty description in a SKILL.md. Returns True if fixed."""
    content = skill_md.read_text(encoding='utf-8')

    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', content, re.DOTALL)
    if not match:
        return False

    fm_text = match.group(1)
    body = match.group(2)

    has_empty_indicator = ('description: >' in fm_text or 'description: |' in fm_text or
                           'description:\n' in fm_text or 'description: \n' in fm_text)
    has_empty_line = bool(re.search(r'^description:\s*$', fm_text, re.MULTILINE))
    if not has_empty_indicator and not has_empty_line:
        return False

    fm_lines = fm_text.split('\n')
    has_real_desc = False
    for i, line in enumerate(fm_lines):
        if line.startswith('description:'):
            value = line.split(':', 1)[1].strip()
            if value and value != '>' and value != '|':
                has_real_desc = True
                break
            # Check if the next line is indented content (not a key)
            if i + 1 < len(fm_lines):
                next_line = fm_lines[i + 1]
                if next_line.startswith('  ') and not re.match(r'^\s+\w+:', next_line):
                    has_real_desc = True
                    break
            break

    if has_real_desc:
        return False

    # Extract description from body
    desc = ''
    for line in body.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            heading = re.sub(r'^#+\s*', '', line).strip()
            if len(heading) > 10:
                desc = heading
                break
            continue
        if line.startswith('---'):
            continue
        if len(line) > 20:
            desc = line
            if len(desc) > 200:
                desc = desc[:197] + '...'
            break

    if not desc:
        return False

    # Replace the empty description in frontmatter
    new_fm_text = re.sub(
        r'description:\s*[>|]?\s*\n',
        f'description: {desc}\n',
        fm_text
    )

    if new_fm_text == fm_text:
        return False

    new_content = f'---\n{new_fm_text}\n---\n{body}'

    if not dry_run:
        skill_md.write_text(new_content, encoding='utf-8')

    return True


def main():
    dry_run = '--dry-run' in sys.argv

    script_dir = Path(__file__).parent
    skills_dir = script_dir.parent / 'skills'

    if dry_run:
        print("DRY RUN\n")

    fixed = 0
    for skill_md in sorted(skills_dir.rglob('SKILL.md')):
        if fix_skill(skill_md, dry_run):
            rel = skill_md.relative_to(skills_dir.parent)
            print(f"  Fixed: {rel}")
            fixed += 1

    print(f"\nFixed {fixed} skills")


if __name__ == '__main__':
    main()
