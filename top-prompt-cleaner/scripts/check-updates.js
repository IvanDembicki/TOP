#!/usr/bin/env node
import { readFileSync } from "fs";
import { resolve } from "path";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");

function parseArgs(argv) {
  const args = { manifest: null };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token === "--manifest") {
      args.manifest = argv[i + 1] || null;
      i++;
    }
  }
  return args;
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function splitVersion(version) {
  const [core, prerelease = ""] = String(version).split("-");
  const parts = core.split(".").map(part => Number.parseInt(part, 10) || 0);
  return { parts, prerelease };
}

function compareVersions(left, right) {
  const a = splitVersion(left);
  const b = splitVersion(right);
  const length = Math.max(a.parts.length, b.parts.length);
  for (let i = 0; i < length; i++) {
    const av = a.parts[i] || 0;
    const bv = b.parts[i] || 0;
    if (av > bv) return 1;
    if (av < bv) return -1;
  }
  if (a.prerelease === b.prerelease) return 0;
  if (!a.prerelease && b.prerelease) return 1;
  if (a.prerelease && !b.prerelease) return -1;
  return a.prerelease.localeCompare(b.prerelease);
}

const args = parseArgs(process.argv.slice(2));
const localPath = join(ROOT, "release-metadata.json");
const localManifest = readJson(localPath);

let result;
if (!args.manifest) {
  result = {
    status: "comparison_not_configured",
    product_name: localManifest.product_name,
    current_version: localManifest.current_version,
    compared_version: null,
    message: "No comparison manifest was provided."
  };
} else {
  const externalPath = resolve(process.cwd(), args.manifest);
  const externalManifest = readJson(externalPath);
  if (externalManifest.product_name !== localManifest.product_name) {
    result = {
      status: "mismatched_manifest",
      product_name: localManifest.product_name,
      current_version: localManifest.current_version,
      compared_version: externalManifest.current_version || null,
      message: "The comparison manifest belongs to a different product."
    };
  } else {
    const cmp = compareVersions(localManifest.current_version, externalManifest.current_version);
    let status = "unknown";
    if (cmp < 0) status = "update_available";
    if (cmp === 0) status = "up_to_date";
    if (cmp > 0) status = "local_ahead";
    result = {
      status,
      product_name: localManifest.product_name,
      current_version: localManifest.current_version,
      compared_version: externalManifest.current_version,
      message: "Startup update comparison completed."
    };
  }
}

console.log(JSON.stringify(result, null, 2));
