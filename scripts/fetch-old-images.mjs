// Downloads the kit diagram images from the old WordPress site into public/images/products/.
// Map lives in old-image-map.json (model -> { url, file }), generated from the research scrapes.
// Usage: node scripts/fetch-old-images.mjs [--force]
import { readFile, writeFile, mkdir, access } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const map = JSON.parse(await readFile(path.join(root, 'scripts/old-image-map.json'), 'utf8'));
const force = process.argv.includes('--force');

await mkdir(path.join(root, 'public/images/products'), { recursive: true });

let ok = 0, skipped = 0, failed = [];
for (const [model, { url, file }] of Object.entries(map)) {
  const dest = path.join(root, file);
  if (!force) {
    try { await access(dest); skipped++; continue; } catch {}
  }
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    await writeFile(dest, Buffer.from(await res.arrayBuffer()));
    ok++;
  } catch (err) {
    failed.push(`${model}: ${err.message}`);
  }
}
console.log(`downloaded ${ok}, skipped ${skipped}, failed ${failed.length}`);
if (failed.length) console.log(failed.join('\n'));
