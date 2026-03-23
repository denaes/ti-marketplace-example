---
name: api-contract-spec
description: >
  Checklist and format for API contracts (OpenAPI snippet, request/response, errors) when [DESIGN] or
  HLD defines new APIs. Use for TI V3 and legacy compatibility.
metadata:
  type: skill
  department: engineering-management
  source: ti-rd-playbook
  version: "1.0"
---
# API Contract Spec

## Purpose

Provide a **checklist and format** for API contracts when a [DESIGN] story or an HLD introduces **new or changed endpoints**. Ensures contract-first thinking and alignment with TI V3 and legacy compatibility.

## When to Use

- When writing a [DESIGN] story that defines new APIs
- When an HLD (e.g. from `ti-write-hld`) proposes new REST or GraphQL surface
- When documenting the contract between new React FE and NestJS BE

## Contract Checklist

For each **new or changed** endpoint, specify:

| Item | Description |
|------|-------------|
| **Method and path** | e.g. `GET /v3/catalog/aeo-pages`, `POST /v3/chat` |
| **Request** | Query params, body schema (DTO), headers (auth, idempotency, etc.) |
| **Response** | Status codes (200, 400, 403, 404, 500), body schema, headers |
| **Errors** | Structured error shape (e.g. `{ error: string, code?: string }`) |
| **Auth** | Required: company context, user, optional auth; see `ti/v3/docs/` for guards |
| **Rate limiting** | If applicable; align with existing V3 patterns |
| **Versioning** | Path prefix (e.g. `/v3/`) or header; backward compatibility notes |

## Format (OpenAPI snippet)

When the epic or HLD expects an OpenAPI/Swagger artifact, include at least:

- `paths.<path>.<method>` with summary, parameters, requestBody, responses
- Reusable `components.schemas` for DTOs
- Reference to existing TI patterns (e.g. `ti/v3/src/modules/` controllers) for style

Example (conceptual):

```yaml
paths:
  /v3/catalog/aeo-pages:
    get:
      summary: List AEO-eligible pages
      parameters:
        - name: companyId
          in: header
          required: true
        - name: page
          in: query
          schema: { type: integer, default: 1 }
      responses:
        '200':
          description: OK
          content:
            application/json:
              schema: { $ref: '#/components/schemas/AeoPageList' }
        '403':
          description: Feature not enabled or forbidden
```

## TI Context

- **V3:** NestJS controllers under `ti/v3/src/modules/`; use existing DTOs and guards as reference. See `ti/v3/docs/ARCHITECTURE.md`, `INTERNAL_RPC.md`.
- **Legacy:** If the new API is called from legacy Node/Ember or proxied, document the proxy path and any request/response transformation. See `ti/v3/docs/SERVICE_BRIDGE.md`.
- **Compatibility:** Note any impact on existing clients or mobile; document deprecation if replacing an endpoint.

## References

- **HLD:** `skills/engineering-management/ti-write-hld/SKILL.md`, `templates/product/[TEMPLATE] HLD.md`
- **V3 architecture:** `ti/v3/docs/ARCHITECTURE.md`
- **Jira Architect [DESIGN]:** `skills/engineering-management/jira_architect/SKILL.md`
