---
name: interactive-api
description: >
  Fetch sample JSON from the live JSONPlaceholder comments API for demos, fixtures, or agent
  exercises. Use when the user asks for fake API data, jsonplaceholder comments, or to run the
  interactive-api fetch script.
metadata:
  type: skill
  department: engineering
  source: original
  version: "1.0"
---
# Interactive API (JSONPlaceholder comments)

## Purpose

Load **fake but realistic** comment objects from the public demo API **[JSONPlaceholder](https://jsonplaceholder.typicode.com/)** — endpoint [`/comments`](https://jsonplaceholder.typicode.com/comments). Each item includes `postId`, `id`, `name`, `email`, and `body`.

## When to Use

- User wants sample API JSON without standing up a backend
- Prototyping clients, skills, or tests that consume a list endpoint
- Teaching or verifying `fetch` / HTTP client behavior against a live URL

## Instructions

1. **Run the bundled script** from the repository root (requires **Node.js 18+** for global `fetch`):

   ```bash
   node skills/interactive-api/fetch-jsonplaceholder-comments.js
   ```

2. **Optional query** — limit by post:

   ```bash
   node skills/interactive-api/fetch-jsonplaceholder-comments.js --postId=1
   ```

3. **Pipe or save** — stdout is JSON (array). Example:

   ```bash
   node skills/interactive-api/fetch-jsonplaceholder-comments.js --postId=1 | head -c 2000
   ```

4. **Failures** — non-2xx responses or network errors exit with code `1` and print a message to stderr.

## Data shape (per comment)

| Field    | Type   | Notes        |
|----------|--------|--------------|
| `postId` | number | Parent post  |
| `id`     | number | Comment id   |
| `name`   | string | Title-ish    |
| `email`  | string | Fake email   |
| `body`   | string | Multiline text |

## References

- API docs / playground: [https://jsonplaceholder.typicode.com/](https://jsonplaceholder.typicode.com/)
- Comments collection: [https://jsonplaceholder.typicode.com/comments](https://jsonplaceholder.typicode.com/comments)

## Quality checklist

- [ ] Node 18+ available (`node -v`)
- [ ] Network allowed to `jsonplaceholder.typicode.com`
- [ ] Output parsed as JSON array before assuming structure
