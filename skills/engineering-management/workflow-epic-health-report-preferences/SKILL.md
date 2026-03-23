---
name: workflow-epic-health-report-preferences
description: Epic Health Report — Persistent Preferences
metadata:
  type: workflow
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Epic Health Report — Persistent Preferences

> **Last updated:** 2026-03-05 · **Last run:** 2026-03-05
> This file is read and updated automatically by the `/epic-health-report` workflow. Do not delete.

---

## Jira Configuration

- **Cloud ID:** `a0491fd7-7605-437a-bf79-b508a7c60f3b`
- **Project:** `TI`
- **Issue Type Filter:** `Epic`
- **Lookback Period:** `6 months`
- **Exclude Canceled:** `true`

---

## KPI Targets

| KPI | Target |
|-----|--------|
| Innovation Ratio | ≥ 80% |
| Maintenance Ratio | ≤ 20% |
| Technical Debt Ratio | < 50% |

---

## Classification Rules

### Work-Type → Target Mapping

| Tag | Target |
|-----|--------|
| `innovation:new-platform` | 🟢 Innovation |
| `innovation:new-feature` | 🟢 Innovation |
| `innovation:new-product` | 🟢 Innovation |
| `innovation:enhancement` | 🟢 Innovation |
| `maintenance:bug-fix` | 🔴 Maintenance |
| `maintenance:keep-the-lights-on` | 🔴 Maintenance |
| `maintenance:enhancement` | 🔴 Maintenance |

### Debt-Type → Target Mapping

| Tag | Target |
|-----|--------|
| `debt:legacy-modernization` | Depends on context |
| `debt:infra-upgrade` | 🔴 Maintenance |
| `debt:ux-debt` | 🔴 Maintenance |
| `debt:code-quality` | 🟢 Innovation |
| `debt:test-automation` | Depends on context |
| `debt:none` | 🟢 Innovation |

### Strategic Initiative → Target Mapping

| Initiative | Default Target |
|------------|---------------|
| `initiative:v3-platform` | 🟢 Innovation |
| `initiative:conversational-search` | 🟢 Innovation |
| `initiative:omni-channel` | 🟢 Innovation |
| `initiative:learning-agent` | 🟢 Innovation |
| `initiative:starter-sku` | 🟢 Innovation |
| `initiative:aeo` | 🟢 Innovation |
| `initiative:panorama` | 🟢 Innovation (unless minor/maintenance enhancement) |
| `initiative:churn-reduction` | 🔴 Maintenance |
| `initiative:infra-cost` | 🔴 Maintenance |
| `initiative:ci-cd` | 🟢 Innovation (pipeline rewrite) |
| `initiative:infosec-compliance` | 🔴 Maintenance |
| `initiative:dx-tooling` | 🟢 Innovation |
| `initiative:qa-automation` | Depends on context |

---

## User Overrides (Sticky per Epic Key)

These are manual corrections from previous sessions. When the same epic key appears in future runs, apply these overrides automatically.

| Epic Key | Forced Target | Work-Type | Reason |
|----------|--------------|-----------|--------|
| TI-3729 | 🔴 Maintenance | maintenance:enhancement | Minor improvement to existing reporting |
| TI-3596 | 🔴 Maintenance | maintenance:keep-the-lights-on | Monitoring for existing system |
| TI-3588 | 🔴 Maintenance | maintenance:keep-the-lights-on | Generic test maintenance |
| TI-3550 | 🔴 Maintenance | maintenance:enhancement | UX debt — maintaining existing experience |
| TI-3514 | 🔴 Maintenance | maintenance:enhancement | Minor improvement to existing reporting |
| TI-3505 | 🔴 Maintenance | maintenance:enhancement | Minor tweaks to existing features |
| TI-3504 | 🔴 Maintenance | maintenance:enhancement | Minor tweaks to existing ecommerce |
| TI-3496 | 🔴 Maintenance | maintenance:enhancement | Minor API maintenance |
| TI-3495 | 🔴 Maintenance | maintenance:enhancement | Routine design maintenance |
| TI-3494 | 🔴 Maintenance | maintenance:enhancement | Compliance-driven accessibility fixes |
| TI-3492 | 🔴 Maintenance | maintenance:enhancement | Minor reporting tweaks |
| TI-3490 | 🔴 Maintenance | maintenance:enhancement | Admin workflow maintenance |
| TI-3489 | 🔴 Maintenance | maintenance:enhancement | Design for existing feature maintenance |
| TI-3418 | 🔴 Maintenance | maintenance:enhancement | Incremental data system fixes/debt |
| TI-3076 | 🔴 Maintenance | maintenance:keep-the-lights-on | Tooling migration (operational) |
| TI-3061 | 🔴 Maintenance | maintenance:enhancement | Fixing inconsistencies in existing system |
| TI-3649 | 🟢 Innovation | innovation:new-feature | JIT modernization — ShadCN migration |
| TI-3125 | ⛔ Canceled | — | User marked as canceled |
| TI-3124 | ⛔ Canceled | — | User marked as canceled |

---

## Classification Heuristics (Learned from User Feedback)

These patterns guide automatic classification for NEW epics:

1. **"Minor" / "Phase 1" / "Q1 -" prefix → likely Maintenance.** Minor enhancements, targeted churn items, and quarterly design/accessibility tasks are maintenance, not innovation.
2. **"Improvements to" existing system → Maintenance** unless it's a net-new integration or architecture shift.
3. **Regression / Observability / Monitoring for existing systems → Maintenance.** Only new-build test infra for new platforms counts as innovation.
4. **Usability / UX debt → Maintenance.** Even though it improves product quality, the user classifies it as maintaining existing experience.
5. **Data systems "uplift" / "migration" between tools (Jenkins→Airflow) → Maintenance.** Same function, different tool. Not innovation.
6. **V3 / NestJS / AI pipeline / Conversational Search / Omni-channel / Learning Agent / Starter SKU → Innovation.** These are always net-new.
7. **AWS cost cutting / InfoSec / Compliance / Component upgrades → Maintenance.** Always keep-the-lights-on.
8. **Design spikes for new products (AEO, Conversational Search, Starter SKU) → Innovation.**
9. **Panorama enhancements → Likely Maintenance** unless clearly building net-new capability (e.g., user migration enhancements with PRD/HLD = Innovation).
10. **"Consistent experience" / fixing inconsistencies → Maintenance.** Bringing existing features to parity is not innovation.

---

## Previous Run History

### Run 1 — 2026-03-05
- **Period:** Sep 2025 – Mar 2026
- **Active Epics:** 59 (12 canceled)
- **Innovation:** 30 (50.8%)
- **Maintenance:** 29 (49.2%)
- **Debt Ratio:** 25.4% (15/59)
- **Gap to 80/20 target:** -29.2%
- **Report:** `~/.gemini/antigravity/brain/30c693cd-b3b1-4907-af19-ea03c7955c21/epic_classification_report.md`
