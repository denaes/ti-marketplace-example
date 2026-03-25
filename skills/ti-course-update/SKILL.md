---
name: ti-course-update
description: >
  Update Thought Industries course content via the Incoming REST API (partial updates to course
  groups, sessions, sections, lessons, topics). Use when the user wants to change titles, HTML
  bodies, SCORM URLs, or add hierarchy nodes using known UUIDs.
metadata:
  type: skill
  department: ti-skills
  source: thought-industries-api
  version: "1.0"
---
# Thought Industries — Update course (Incoming API)

## Purpose

Call **`PUT /incoming/v2/content/course/update`** for **partial** updates. Only fields present in the payload are applied; new sections, lessons, or topics can be created by **omitting** `id` where the API allows (and supplying parent IDs such as `courseId`, `sectionId`, or `lessonId`). Full schema and examples: [Thought Industries API — Course APIs](https://api.thoughtindustries.com/#course-apis).

## When to Use

- User wants to **change** existing TI content (metadata, topic HTML, SCORM package URL, etc.)
- User wants to **append** structure (e.g. new section on an existing course) using **`courseId`** / **`lessonId`**
- User already has **UUIDs** from the catalog, GET structure, or a prior create response

## Instructions (agent)

1. **Credentials** — Same as create: **base URL** + **Bearer API key** from **Settings › Security**. Never persist secrets in the workspace or transcripts.

2. **Elicit targets** — Updates need stable identifiers:
   - **Course group** changes: `courseGroups[].id`
   - **Session/course** changes: `courses[].id`
   - **Sections**: `sections[].id` or create with `courseId` + no `id`
   - **Lessons**: `lessons[].id` or create with `sectionId` + no `id`
   - **Topics**: **`topics[].id`** required to patch existing; omit `id` + set `lessonId` + `type` to add a topic

   If the user only has slugs, use **List Content** / **Get Course Structure** APIs from the same documentation to resolve IDs before updating.

3. **Build payload** — Prefer the shorthand the script understands:
   - `{ "topics": [ { "id": "…", "body": "<p>…</p>" } ] }`
   - `{ "courseGroups": [ { "id": "…", "title": "…" } ] }`
   - Or full `{ "courseAttributes": { … } }` matching the API (`courseGroups`, `courses`, `sections`, `lessons`, `topics` — arrays only inside `courseAttributes`)

4. **Run** from repository root (**Node.js 18+**):

   ```bash
   export TI_BASE_URL="https://YOUR_SCHOOL.thoughtindustries.com"
   export TI_API_KEY="YOUR_BEARER_TOKEN"
   node skills/ti-course-update/update-course.js --file=path/to/update.json
   ```

   Dry-run (print normalized body only):

   ```bash
   node skills/ti-course-update/update-course.js --dry-run --file=path/to/update.json
   ```

   **API key pattern** matches **`ti-course-create`**: prefer `TI_API_KEY` / `THOUGHT_INDUSTRIES_API_KEY`, then `--api-key-file`, then `--api-key`; interactive paste only when stdin is not used for JSON and the terminal is interactive.

   Piped JSON (must set `TI_API_KEY` in the environment):

   ```bash
   node skills/ti-course-update/update-course.js --base-url="$TI_BASE_URL" < update.json
   ```

5. **SCORM / PDF uploads** — Response may include `backgroundJob`; direct the user to job status endpoints in the official docs when `contentBulkUpload` appears.

6. **`restartProgress`** — When replacing SCORM on an existing topic, confirm with the user before sending `restartProgress: true`.

## Normalization (script)

- `{ "courseAttributes": { … } }` — passed through (`courseAttributes` must be an **object**, not a create-style array)
- An object with any of **`courseGroups`**, **`courses`**, **`sections`**, **`lessons`**, **`topics`** (array values) — wrapped as `{ "courseAttributes": { … } }`

## Quality checklist

- [ ] UUIDs verified or user accepts responsibility for wrong IDs
- [ ] Secrets only via env / key file / explicit flag — not in repo
- [ ] User aware of background jobs for binary/url upload flows
- [ ] Create vs update shape not confused (`courseAttributes` array on create vs object on update)

## References

- [Thought Industries API documentation](https://api.thoughtindustries.com/#course-apis)
- Companion create flow: **`ti-course-create`**
