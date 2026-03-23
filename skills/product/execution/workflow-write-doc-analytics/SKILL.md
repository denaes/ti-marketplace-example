---
name: workflow-write-doc-analytics
description: >
  Document analytics and events for a specific feature or area. Product-facing "when does event X
  fire and with what properties?" Use when a feature ships new instrumentation or product needs a
  single reference for events.
metadata:
  type: workflow
  department: product
  source: ti-rd-playbook
  version: "1.0"
---
# Document analytics and events (feature-specific)

Produce **product-facing documentation** that describes when each analytics event is fired and what properties it sends. Use for a **specific feature or area** (e.g. AI search, checkout, manager actions). Output can extend the platform-wide `ti/docs/ANALYTICS_EVENTS.md` or live as a feature-specific doc.

## Prerequisites

- **Scope:** Feature or area name (e.g. "AI search", "C2 conversational search", "checkout funnel")
- **Optional:** Code paths or file hints (e.g. `ti/assets/javascripts/lms/react/src/hooks/use-ga-tracking.ts`, or "last 2 months in ti/")
- **Audience:** Product, PM, analytics; may be shared with customers for their GA4/Segment setup

---

## Step 1: Clarify scope (ask if needed)

If the **feature boundary** or **event set** is unclear, ask:

- Which feature or product area? (e.g. learner search, manager layout, embed)
- Existing doc to extend (e.g. `ti/docs/ANALYTICS_EVENTS.md`) or net-new feature doc?
- Time window for code search (e.g. "last 2 months") if you need to limit to recent changes

Do not assume—ask. See `standards/conventions.md` (Ask before deciding).

---

## Step 2: Locate instrumentation in code

1. **Search** the TI codebase (`ti/`, `ti/v3/`) for the feature area:
   - GA/gtag calls, `trackInternalGA`, Segment `track`, custom script hooks
   - Event names (e.g. `ai_search_query_submitted`, `search`, `content_view`)
2. **Extract** for each event:
   - **Event name** (exact string)
   - **When it fires** (user action or system trigger in plain language)
   - **Properties** (payload keys and types: ids, counts, timing, categorical)
   - **Delivery** (internal GA4, customer GA4, Segment, custom scripts, feature flags that disable)

If the user provided file paths or a time window (e.g. git log last 2 months), use those to focus the search.

---

## Step 3: Choose output location and format

| Output type | Location | Use when |
|-------------|----------|----------|
| **Feature section** in platform doc | `ti/docs/ANALYTICS_EVENTS.md` | Feature is part of the main platform; add a new H2 section (e.g. "3. Feature X events") |
| **Standalone feature doc** | `ti/docs/analytics/ANALYTICS_EVENTS_<feature-slug>.md` or project `workspace/projects/<slug>/product/` | Feature has its own release or doc owner; keep platform doc lean |

Use the same **table format** as the existing analytics doc:

- **When** (one short sentence)
- **Event** (exact name)
- **Properties** (list or table row)

Include a short **Delivery** note at the top (internal GA, customer GA, Segment, custom scripts, and any `googleAnalyticsDisabled` or feature-flag behavior).

---

## Step 4: Write the doc

1. **Header:** Title, one-line purpose, and delivery note (where events go, any flags).
2. **Sections:** Group by lifecycle or flow (e.g. session lifecycle, query/answer, results/engagement).
3. **Tables:** For each event: When | Event | Properties. Use consistent property names (e.g. `correlation_id`, `instance_id`, `user_id`, `subdomain`).
4. **Quick reference (optional):** Short "When user does X → event Y with properties Z" examples for product.

---

## Step 5: Confirm

Tell the user where the doc was written and give a one-sentence summary. If you extended `ti/docs/ANALYTICS_EVENTS.md`, note the new section. If product wants this in Confluence or a wiki, say they can copy the markdown.

---

## Reference

- **Example:** `ti/docs/ANALYTICS_EVENTS.md` — platform events and AI search events with When/Event/Properties tables and delivery note.
