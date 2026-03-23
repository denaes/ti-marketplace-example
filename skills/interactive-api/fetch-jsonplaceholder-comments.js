#!/usr/bin/env node
/**
 * Fetches comments from JSONPlaceholder (fake REST API).
 * https://jsonplaceholder.typicode.com/comments
 *
 * Usage:
 *   node fetch-jsonplaceholder-comments.js
 *   node fetch-jsonplaceholder-comments.js --postId=1
 *   node fetch-jsonplaceholder-comments.js --id=3
 *   (same as GET https://jsonplaceholder.typicode.com/comments/3)
 */

const BASE = "https://jsonplaceholder.typicode.com/comments";

function parseArgs(argv) {
  let postId = null;
  let commentId = null;
  for (const arg of argv.slice(2)) {
    if (arg.startsWith("--postId=")) {
      const v = arg.slice("--postId=".length);
      postId = Number.parseInt(v, 10);
      if (Number.isNaN(postId)) {
        console.error(`Invalid --postId: ${v}`);
        process.exit(1);
      }
    } else if (arg.startsWith("--id=")) {
      const v = arg.slice("--id=".length);
      commentId = Number.parseInt(v, 10);
      if (Number.isNaN(commentId)) {
        console.error(`Invalid --id: ${v}`);
        process.exit(1);
      }
    }
  }
  return { postId, commentId };
}

function buildUrl({ postId, commentId }) {
  if (commentId != null) {
    return `${BASE}/${commentId}`;
  }
  if (postId != null) {
    return `${BASE}?postId=${postId}`;
  }
  return BASE;
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.commentId != null && args.postId != null) {
    console.error("Use only one of --id or --postId (not both).");
    process.exit(1);
  }

  const url = buildUrl(args);

  const res = await fetch(url, {
    headers: { Accept: "application/json" },
  });

  if (!res.ok) {
    console.error(`HTTP ${res.status} ${res.statusText} for ${url}`);
    process.exit(1);
  }

  const data = await res.json();
  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
