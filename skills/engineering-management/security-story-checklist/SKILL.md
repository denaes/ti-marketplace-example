---
name: security-story-checklist
description: >
  Structured checklist for [SEC] stories (auth, RBAC, PII, rate limiting, compliance). Use when
  writing or reviewing security scope. References ti/v3 patterns.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# Security Story Checklist

## Purpose

Provide a **structured checklist** for [SEC] stories and for security-related scope in any story so the DoR "Security" dimension is concrete and nothing is missed. Aligns with TI V3 guards and patterns.

## When to Use

- When writing or reviewing a [SEC] story
- When any story touches auth, permissions, PII, or compliance
- When assessing PRD or epic for security coverage (definition_of_ready)

## Checklist (per story or feature)

| Area | Questions to answer |
|------|---------------------|
| **AuthN** | Who can call this? JWT, session, API key? Optional vs required auth? See `ti/v3/docs/` for auth guards. |
| **AuthZ / RBAC** | What roles or permissions are required? SuperAdmin, company admin, learner? Scope (company, sublicense, user)? |
| **Data access** | Does the code filter by companyId, userId, or hierarchy? Can one tenant see another's data? |
| **PII** | Does the story touch PII? Logging, storage, or transmission; encryption at rest and in transit. |
| **Rate limiting** | Are there new endpoints or expensive operations? Rate limit per company/user? See existing V3 rate-limit patterns. |
| **Input validation** | Request validation (class-validator), sanitization, injection prevention. |
| **Compliance** | GDPR, SOC2, or other: data retention, right to deletion, audit trail. |

## TI V3 References

- **Guards:** `ti/v3/src/common/` (e.g. auth guards, company context, permission guards). Search for `*Guard` and `*guard`.
- **Auth flow:** `ti/v3/docs/ARCHITECTURE.md` (Authentication Flow). Same JWT/session as legacy.
- **Feature flags:** Access to a feature may be gated by company feature flags (e.g. `FeatureFlag.SEARCH`); document in [SEC] or [FF] story as appropriate.

## Story Description

When writing a [SEC] story, include in the acceptance criteria:

- [ ] AuthN: [how caller is identified]
- [ ] AuthZ: [who is allowed; what is forbidden]
- [ ] Data scope: [what data is visible; no cross-tenant leakage]
- [ ] PII / compliance: [if applicable; or "N/A - no PII"]
- [ ] Rate limiting: [if applicable; or "N/A"]

## References

- **DoR:** `skills/engineering-management/definition_of_ready/SKILL.md` (Security dimension)
- **Jira Architect [SEC]:** `skills/engineering-management/jira_architect/SKILL.md`
- **V3 architecture:** `ti/v3/docs/ARCHITECTURE.md`
