#!/usr/bin/env node
/**
 * Fetches comments from JSONPlaceholder (fake REST API).
 * https://jsonplaceholder.typicode.com/comments
 *
 * Usage:
 *   node fetch-jsonplaceholder-comments.js
 *   node fetch-jsonplaceholder-comments.js --postId=1
 */

const BASE = "https://jsonplaceholder.typicode.com/comments";

function parseArgs(argv) {
  let postId = null;
  for (const arg of argv.slice(2)) {
    if (arg.startsWith("--postId=")) {
      const v = arg.slice("--postId=".length);
      postId = Number.parseInt(v, 10);
      if (Number.isNaN(postId)) {
        console.error(`Invalid --postId: ${v}`);
        process.exit(1);
      }
    }
  }
  return { postId };
}

async function main() {
  const { postId } = parseArgs(process.argv);
  const url = postId != null ? `${BASE}/{postId}` : BASE;

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
