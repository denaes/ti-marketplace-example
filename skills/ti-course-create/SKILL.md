---
name: ti-course-create
description: >
  Create Thought Industries courses via the Incoming REST API (course groups, micro-courses,
  articles, SCORM/xAPI). Use when the user wants to programmatically create TI content from
  structured data or scripts.
metadata:
  type: skill
  department: ti-skills
  source: thought-industries-api
  version: "1.0"
---
# Thought Industries — Create course (Incoming API)

## Purpose

Call **`POST /incoming/v2/content/course/create`** to create one or more courses (up to API limits), including optional hierarchy (sections → lessons → topics) depending on `kind`. Official contract and examples: [Thought Industries API — Course APIs](https://api.thoughtindustries.com/#course-apis).

## When to Use

- User wants to **create** a TI course (or multiple) from JSON they or the agent assembled
- Automating content setup after the user provides **title**, **`kind`**, and **structure** (or a micro-course / article / SCORM payload)
- Pair with **`ti-course-update`** after IDs exist for follow-up edits

## Instructions (agent)

1. **Confirm access** — User has a Thought Industries **school base URL** (e.g. `https://{subdomain}.thoughtindustries.com`) and an **API key** from **Settings › Security** (Bearer token). Never store the key in the repo, logs, or generated markdown.

2. **Elicit content (do not invent IDs)**  
   Ask for everything needed to build a valid `courseAttributes` entry:
   - **`kind`**: `courseGroup` | `microCourse` | `article` | `shareableContentObject` | `xApiObject`
   - **`title`** (required)
   - Optional catalog/session fields the API supports today (`sku`, dates, `discussionsEnabled`, SCORM dimensions/URL, etc.)
   - **Structure**:
     - **`courseGroup`**: `sections[]` → `lessons[]` (each lesson needs `title`, **`openType`** e.g. `studentsOnly`, `topics[]`)
     - **`microCourse`**: top-level `topics[]` (no sections)
     - **`article`**: `articleVariant.body` (HTML)
     - **SCORM/xAPI**: `scormUrl`, optional `width` / `height` / `embeddedEnabled`

3. **Translate messy input** — If the user gives an outline (bullets, headings), map it to the API tree: sections = top-level headings, lessons = sub-headings, topics = pages. Prefer supported topic types for create (`text`, `article`, `embed`, `pdfViewer`, `shareableContentObject`, `xApiObject`, `discussionBoard`). Shell-only types (`quiz`, `test`, …) create **placeholders**; say so explicitly.

4. **Produce JSON** — Build either:
   - One course object `{ "title", "kind", ... }`, or
   - The full API shape `{ "courseAttributes": [ ... ] }`

5. **Run the script** from the repository root (requires **Node.js 18+**):

   ```bash
   export TI_BASE_URL="https://YOUR_SCHOOL.thoughtindustries.com"
   export TI_API_KEY="YOUR_BEARER_TOKEN"
   node skills/ti-course-create/create-course.js --file=path/to/course.json
   ```

   Validate payload shape without calling the API:

   ```bash
   node skills/ti-course-create/create-course.js --dry-run --file=path/to/course.json
   ```

   **API key pattern (pick one; prefer env):**

   | Method | Notes |
   |--------|--------|
   | `TI_API_KEY` or `THOUGHT_INDUSTRIES_API_KEY` | Recommended for agents and CI |
   | `--api-key-file=/abs/path/secret.txt` | File contains the token only |
   | `--api-key=…` | Avoid when shell history is a concern |
   | Interactive paste | Only if no JSON is read from stdin; TTY prompts when env is missing |

   Pipe JSON (stdin is the **body**, not the key — set `TI_API_KEY` when piping):

   ```bash
   node skills/ti-course-create/create-course.js --base-url="$TI_BASE_URL" < course.json
   ```

6. **Handle responses** — Create may return an array of new IDs, or an object with `courseIds` and `backgroundJob` for SCORM/xAPI uploads; point the user to job polling in the API docs if applicable.

7. **Failures** — Non-success HTTP exits `1` with a short message. Rate limits may return `429` (retry per docs).

## Normalization (script)

The bundled `create-course.js` accepts:

- `{ "courseAttributes": [ … ] }` — unchanged
- A **single course** with `"title"` + `"kind"` — wrapped as one `courseAttributes` element
- An **array** of course objects — wrapped as `courseAttributes`

## Quality checklist

- [ ] User supplied **base URL** and **Bearer token** through a secure channel; not committed
- [ ] `kind` and structure match (sections for `courseGroup`, `topics` for `microCourse`, etc.)
- [ ] Lessons include **`openType`** where the API requires it
- [ ] User told when topic types are placeholders (quiz/test/survey/…)

## References

- [Thought Industries API documentation](https://api.thoughtindustries.com/#course-apis)
- Authentication: `Authorization: Bearer <API_KEY>` on every request
