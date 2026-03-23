#!/usr/bin/env node
/**
 * Read spreadsheet JSON from file or stdin, find rows with empty Reporting Category (index 6),
 * apply heuristics, output markdown table.
 * Usage: node run-propose.js [path/to/sheet.json]
 *        node run-propose.js < spreadsheet.json
 */
const fs = require('fs');
const path = process.argv[2];
let raw = '';
if (path && path !== '-') {
  try {
    raw = fs.readFileSync(path, 'utf8');
  } catch (e) {
    process.stderr.write('File not found: ' + path + '\n');
    process.exit(1);
  }
} else {
  try {
    raw = fs.readFileSync(0, 'utf8');
  } catch (e) {
    process.stderr.write('Pass spreadsheet JSON (with "values" array) as first arg or stdin.\n');
    process.exit(1);
  }
}
let data;
try {
  data = JSON.parse(raw);
} catch (e) {
  process.stderr.write('Invalid JSON\n');
  process.exit(1);
}
let empty = [];
if (Array.isArray(data)) {
  empty = data.filter((r) => r && (r.key || r.name));
} else {
  const values = data.values || [];
  for (let i = 1; i < values.length; i++) {
    const row = values[i];
    const key = (row[0] || '').trim();
    if (!key) continue;
    const cat = row[6] != null ? String(row[6]).trim() : '';
    if (cat === '' || cat === '—') {
      empty.push({ key, name: (row[1] || '').trim() || key });
    }
  }
}

function propose(name) {
  if (!name || typeof name !== 'string') return { tag: 'REVIEW', reason: 'No name' };
  const n = name.trim();
  if (/^(minor|phase\s*1|q1\s*-)/i.test(n) || /\bq1\s+-\s+/.test(n)) return { tag: 'maintenance:enhancement', reason: 'Minor/Phase 1/Q1 prefix' };
  if (/improvements?\s+to\s+/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Improvements to existing' };
  if (/regression|observability|monitoring/i.test(n) && !/new\s+platform|v3|nestjs/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'Regression/Observability/Monitoring' };
  if (/usability|ux\s*debt|papercuts/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Usability/UX debt' };
  if (/data\s*(uplift|systems?|engineering)|tool\s*migration|backfill|etl|looker/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'Data/tool migration' };
  if (/v3|nestjs|conversational\s*search|omni[- ]?channel|learning\s*(value\s*)?agent|starter\s*sku|aeo\s*pilot|lva\s+platform|learning\s+value\s+agent/i.test(n)) return { tag: /platform|architecture|foundation|service/i.test(n) ? 'innovation:new-platform' : 'innovation:new-feature', reason: 'V3/AI/Omni-channel/Starter SKU/LVA' };
  if (/aws\s*cost|infosec|compliance|component\s*upgrades|eks\s*\d|redshift|rds\s*mysql|deprecation|end\s*of\s*(life|standard)/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'AWS/InfoSec/Compliance/Upgrade' };
  if (/\[?design\]?\s*spike|\[?research\]?/i.test(n) && /alpha|beta|pilot|aeo|product/i.test(n)) return { tag: 'innovation:new-feature', reason: 'Design spike' };
  if (/panorama/i.test(n) && !/new\s+capability|prd|hld/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Panorama enhancement' };
  if (/consistent\s+experience|fixing\s+inconsistencies/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Consistent experience' };
  if (/\[?(alpha|beta|ga|pilot)\]?|new\s+(product|feature|platform)/i.test(n)) return { tag: 'innovation:new-feature', reason: 'Alpha/Beta/GA/Pilot' };
  if (/architecture|service|platform|foundation/i.test(n) && /v3|nestjs|establish|build/i.test(n)) return { tag: 'innovation:new-platform', reason: 'Architecture/platform' };
  if (/upgrade|deprecation|end\s*of\s*life|cost\s*cutting|sunset/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'Upgrade/deprecation/cost' };
  if (/bug|regression|fix|incident|sev\s*[1-4]/i.test(n) || /bucket.*bug/i.test(n)) return { tag: 'maintenance:bug-fix', reason: 'Bug/regression/fix' };
  return { tag: 'REVIEW', reason: 'No heuristic matched' };
}

console.log('# Proposed Reporting Category (empty rows only)\n');
console.log('| Key | Name | Proposed Reporting Category | Reason |');
console.log('|-----|------|-----------------------------|--------|');
let reviewCount = 0;
for (const r of empty) {
  const { tag, reason } = propose(r.name);
  if (tag === 'REVIEW') reviewCount++;
  const nameEsc = (r.name || '').replace(/\|/g, '\\|').slice(0, 55);
  console.log(`| ${r.key} | ${nameEsc}${r.name && r.name.length > 55 ? '…' : ''} | ${tag} | ${reason} |`);
}
console.log('\n## Summary');
console.log(`- **Rows with empty Reporting Category:** ${empty.length}`);
console.log(`- **Proposed (auto):** ${empty.length - reviewCount}`);
console.log(`- **Flagged for REVIEW:** ${reviewCount}`);
console.log('\nPaste the proposed values into the sheet, then run **sync-reporting-category-from-sheet** to push to Jira (TI project).');
