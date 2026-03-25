#!/usr/bin/env node
/**
 * Thought Industries Incoming API — update course content (partial updates).
 *
 * PUT {base}/incoming/v2/content/course/update
 *
 * @see https://api.thoughtindustries.com/#course-apis
 */

import { readFile } from "node:fs/promises";
import { createInterface } from "node:readline";

/** Relative to …/incoming/v2 (see toApiRoot). */
const PATH = "/content/course/update";

/** @typedef {Record<string, unknown>} JsonObject */

const UPDATE_ENTITY_KEYS = ["courseGroups", "courses", "sections", "lessons", "topics"];

/**
 * @param {string[]} argv
 * @returns {{
 *   file: string | null;
 *   json: string | null;
 *   baseUrl: string | null;
 *   apiKey: string | null;
 *   apiKeyFile: string | null;
 *   dryRun: boolean;
 *   help: boolean;
 * }}
 */
function parseArgs(argv) {
  const out = {
    file: null,
    json: null,
    baseUrl: null,
    apiKey: null,
    apiKeyFile: null,
    dryRun: false,
    help: false,
  };
  for (const arg of argv.slice(2)) {
    if (arg === "--help" || arg === "-h") out.help = true;
    else if (arg === "--dry-run") out.dryRun = true;
    else if (arg.startsWith("--file=")) out.file = arg.slice("--file=".length);
    else if (arg.startsWith("--json=")) out.json = arg.slice("--json=".length);
    else if (arg.startsWith("--base-url=")) out.baseUrl = arg.slice("--base-url=".length);
    else if (arg.startsWith("--api-key=")) out.apiKey = arg.slice("--api-key=".length);
    else if (arg.startsWith("--api-key-file=")) out.apiKeyFile = arg.slice("--api-key-file=".length);
    else if (!arg.startsWith("-") && out.file == null) out.file = arg;
  }
  return out;
}

function printHelp() {
  process.stdout.write(`Usage:
  node update-course.js [--base-url=URL] [--api-key=KEY | --api-key-file=PATH] [--file=PATH | --json='...' | -]

Environment (preferred for secrets):
  TI_BASE_URL          e.g. https://your-school.thoughtindustries.com
  TI_API_KEY           Bearer token (Settings › Security)
  THOUGHT_INDUSTRIES_API_KEY  (alias for TI_API_KEY)

Options:
  --dry-run            Print normalized JSON body only; do not call the API.
  -                    Read JSON from stdin

Input JSON normalization:
  • Full API shape: { "courseAttributes": { "topics"?: [], "sections"?: [], ... } }
  • Shorthand: { "topics": [...] } or any subset of courseGroups/courses/sections/lessons/topics
    → wrapped under courseAttributes

`);
}

/** @param {string} base */
function toApiRoot(base) {
  const trimmed = base.trim().replace(/\/+$/, "");
  if (!/^https?:\/\//i.test(trimmed)) {
    throw new Error(`TI_BASE_URL must be absolute (https://...), got: ${base}`);
  }
  return `${trimmed}/incoming/v2`;
}

/**
 * @param {unknown} raw
 * @returns {{ courseAttributes: JsonObject }}
 */
function normalizeUpdateBody(raw) {
  if (raw == null || typeof raw !== "object" || Array.isArray(raw)) {
    throw new Error("Body must be a JSON object (not an array).");
  }
  /** @type {JsonObject} */
  const obj = /** @type {JsonObject} */ (raw);

  if ("courseAttributes" in obj) {
    const ca = obj.courseAttributes;
    if (ca == null || typeof ca !== "object" || Array.isArray(ca)) {
      throw new Error('update: "courseAttributes" must be an object with entity arrays (not a create-style array).');
    }
    return { courseAttributes: /** @type {JsonObject} */ (ca) };
  }

  const hasEntity = UPDATE_ENTITY_KEYS.some((k) => k in obj && Array.isArray(obj[k]));
  if (!hasEntity) {
    throw new Error(
      `update: expected "courseAttributes" or at least one of: ${UPDATE_ENTITY_KEYS.join(", ")} (e.g. { "topics": [...] }).`,
    );
  }

  /** @type {JsonObject} */
  const inner = {};
  for (const k of UPDATE_ENTITY_KEYS) {
    if (k in obj) inner[k] = obj[k];
  }
  return { courseAttributes: inner };
}

/**
 * @param {string | null} path
 * @param {string | null} inlineJson
 */
async function loadJsonRaw(path, inlineJson) {
  if (inlineJson != null) {
    return inlineJson;
  }
  if (path === "-") {
    return readStdinUtf8();
  }
  if (path == null) {
    if (process.stdin.isTTY) {
      throw new Error("Provide update JSON via --file=path.json, --json='{...}', or pipe JSON on stdin (not a TTY).");
    }
    return readStdinUtf8();
  }
  return readFile(path, "utf8");
}

function readStdinUtf8() {
  return new Promise((resolve, reject) => {
    const chunks = [];
    process.stdin.on("data", (c) => chunks.push(c));
    process.stdin.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    process.stdin.on("error", reject);
  });
}

/**
 * @param {string | null} explicit
 * @param {string | null} filePath
 */
async function resolveBearerToken(explicit, filePath) {
  if (explicit?.length) return explicit;
  const env = process.env.TI_API_KEY ?? process.env.THOUGHT_INDUSTRIES_API_KEY ?? "";
  if (env.length) return env;
  if (filePath?.length) {
    const t = (await readFile(filePath, "utf8")).trim();
    if (!t) throw new Error("API key file is empty.");
    return t;
  }
  if (process.stdin.isTTY && process.stdout.isTTY) {
    process.stderr.write(
      "TI_API_KEY is not set. Paste your Thought Industries API key (Bearer token; input echoed).\nKey: ",
    );
    const key = await promptLine();
    if (!key) throw new Error("No API key provided.");
    return key;
  }
  throw new Error(
    "Missing API key: set TI_API_KEY (or THOUGHT_INDUSTRIES_API_KEY), use --api-key-file, or run in a TTY to paste interactively.",
  );
}

function promptLine() {
  const rl = createInterface({ input: process.stdin, output: process.stderr });
  return new Promise((resolve) => {
    rl.question("", (line) => {
      rl.close();
      resolve(line.trim());
    });
  });
}

/**
 * @param {string | null} explicit
 */
function resolveBaseUrl(explicit) {
  const fromEnv = process.env.TI_BASE_URL ?? "";
  const base = (explicit?.length ? explicit : fromEnv).trim();
  if (!base) {
    throw new Error(
      "Missing base URL: pass --base-url=https://your-school.thoughtindustries.com or set TI_BASE_URL.",
    );
  }
  return toApiRoot(base);
}

/**
 * @param {string} apiRoot
 * @param {string} token
 * @param {unknown} body
 */
async function putUpdate(apiRoot, token, body) {
  const url = `${apiRoot}${PATH}`;
  const res = await fetch(url, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const text = await res.text();
  let data;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = text;
  }

  if (!res.ok) {
    const msg = typeof data === "object" && data && "message" in data ? JSON.stringify(data) : text;
    throw new Error(`HTTP ${res.status} ${res.statusText} — ${msg || "(empty body)"}`);
  }

  process.stdout.write(`${JSON.stringify(data, null, 2)}\n`);
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    return;
  }

  const rawText = await loadJsonRaw(args.file, args.json);
  let parsed;
  try {
    parsed = JSON.parse(rawText);
  } catch (e) {
    throw new Error(`Invalid JSON: ${/** @type {Error} */ (e).message}`);
  }

  const body = normalizeUpdateBody(parsed);

  if (args.dryRun) {
    process.stdout.write(`${JSON.stringify(body, null, 2)}\n`);
    return;
  }

  const apiRoot = resolveBaseUrl(args.baseUrl);
  const token = await resolveBearerToken(args.apiKey, args.apiKeyFile);
  await putUpdate(apiRoot, token, body);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
});
