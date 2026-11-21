// The World in One Day — 21 November 2026
// make.fun entry for competition "news-image-20261121".
//
// The entry image is drawn by tools/generate.py (Pillow) and committed to
// this repo as entry.png. This program simply copies that image to
// /output/entry.png, deterministically and without any network access.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const source = join(repoRoot, "entry.png");
const outDir = "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error(`missing source image: ${source}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// Verify the copy is a whole, intact PNG before reporting success.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const copied = readFileSync(target);
if (!copied.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error("copied file is not a PNG");
  process.exit(1);
}
if (copied.length !== statSync(source).size) {
  console.error("copied file size does not match the source");
  process.exit(1);
}
console.log(`wrote ${target} (${copied.length} bytes)`);
