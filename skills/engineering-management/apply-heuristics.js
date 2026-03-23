#!/usr/bin/env node
/**
 * Apply reporting-epic-categories heuristics to epic names.
 * Input: JSON array of { key, name } (one per line or single JSON array).
 * Output: Markdown table rows.
 */
function propose(name) {
  if (!name || typeof name !== 'string') return { tag: 'REVIEW', reason: 'No name' };
  const n = name.trim();
  const lower = n.toLowerCase();
  // 1. Minor / Phase 1 / Q1 -
  if (/^(minor|phase\s*1|q1\s*-)/i.test(n) || /\bq1\s+-\s+/.test(n)) return { tag: 'maintenance:enhancement', reason: 'Minor/Phase 1/Q1 prefix' };
  // 2. Improvements to
  if (/improvements?\s+to\s+/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Improvements to existing' };
  // 3. Regression / Observability / Monitoring
  if (/regression|observability|monitoring/i.test(n) && !/new\s+platform|v3|nestjs/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'Regression/Observability/Monitoring' };
  // 4. Usability / UX debt
  if (/usability|ux\s*debt|papercuts/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Usability/UX debt' };
  // 5. Data uplift / tool migration
  if (/data\s*(uplift|systems?|engineering)|tool\s*migration|backfill|etl/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'Data/tool migration' };
  // 6. V3 / NestJS / AI / Conversational Search / Omni-channel / Learning Agent / Starter SKU
  if (/v3|nestjs|conversational\s*search|omni[- ]?channel|learning\s*(value\s*)?agent|starter\s*sku|aeo\s*pilot|lvа|lva\s+platform/i.test(n)) return { tag: n.match(/platform|architecture|foundation|service/i) ? 'innovation:new-platform' : 'innovation:new-feature', reason: 'V3/AI/Omni-channel/Starter SKU/LVA' };
  // 7. AWS cost / InfoSec / Compliance / Component upgrades
  if (/aws\s*cost|infosec|compliance|component\s*upgrades|eks\s*\d|redshift|rds\s*mysql|deprecation|end\s*of\s*(life|standard)/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'AWS/InfoSec/Compliance/Upgrade' };
  // 8. Design spikes for new products
  if (/\[?design\]?\s*spike|\[?research\]?/i.test(n) && /alpha|beta|pilot|aeo|product/i.test(n)) return { tag: 'innovation:new-feature', reason: 'Design spike for new product' };
  // 9. Panorama enhancements
  if (/panorama/i.test(n) && !/new\s+capability|prd|hld/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Panorama enhancement' };
  // 10. Consistent experience / fixing inconsistencies
  if (/consistent\s+experience|fixing\s+inconsistencies/i.test(n)) return { tag: 'maintenance:enhancement', reason: 'Consistent experience' };
  // 11. new, alpha, beta, GA, pilot
  if (/\[?(alpha|beta|ga|pilot)\]?|new\s+(product|feature|platform)/i.test(n)) return { tag: 'innovation:new-feature', reason: 'Alpha/Beta/GA/Pilot' };
  // 12. architecture, service, platform, foundation
  if (/architecture|service|platform|foundation/i.test(n) && /v3|nestjs|establish|build/i.test(n)) return { tag: 'innovation:new-platform', reason: 'Architecture/platform/foundation' };
  // 13. upgrade, deprecation, end of life, cost
  if (/upgrade|deprecation|end\s*of\s*life|cost\s*cutting|sunset/i.test(n)) return { tag: 'maintenance:keep-the-lights-on', reason: 'Upgrade/deprecation/cost' };
  // 14. bug, regression, fix, incident
  if (/bug|regression|fix|incident|sev\s*[1-4]/i.test(n) || /bucket.*bug/i.test(n)) return { tag: 'maintenance:bug-fix', reason: 'Bug/regression/fix' };
  // 15. Otherwise
  return { tag: 'REVIEW', reason: 'No heuristic matched' };
}

const input = process.argv[2];
if (input === '--help' || !input) {
  console.error('Usage: node apply-heuristics.js <json-array-of-{key,name}>');
  process.exit(1);
}
const rows = JSON.parse(input);
console.log('| Key | Name | Proposed Reporting Category | Reason |');
console.log('|-----|------|-----------------------------|--------|');
for (const r of rows) {
  const { tag, reason } = propose(r.name);
  const nameEsc = (r.name || '').replace(/\|/g, '\\|').slice(0, 60);
  console.log(`| ${r.key} | ${nameEsc} | ${tag} | ${reason} |`);
}
