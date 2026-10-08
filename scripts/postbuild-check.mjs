// LWS QA guard. Runs after astro build and fails the build on any hard-rule violation:
// root-relative or absolute internal asset paths, em dashes, forbidden copy, H1 count, logo markup.
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');

async function walk(dir, ext, out = []) {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) await walk(p, ext, out);
    else if (ext.some((x) => e.name.endsWith(x))) out.push(p);
  }
  return out;
}

const EM_DASH = String.fromCharCode(0x2014);
const problems = [];
const forbidden = [/\bsubmit\b/i, /click here/i, /learn more/i, /don'?t hesitate/i, /schedule a free consultation/i];

for (const file of await walk(dist, ['.html'])) {
  const rel = path.relative(dist, file);
  const html = await readFile(file, 'utf8');
  const isAdmin = rel.startsWith('admin');

  // Relative-path rule. The 404 page carries <base href="/"> on purpose.
  const rootRefs = [...html.matchAll(/\b(?:href|src|srcset|poster|data-mp4|data-webm|data-img|action)="(\/[^"]*)"/g)]
    .map((m) => m[1])
    .filter((u) => !(rel === '404.html' && u === '/'));
  if (rootRefs.length) problems.push(`${rel}: root-relative refs ${[...new Set(rootRefs)].slice(0, 5).join(', ')}`);
  if (/url\(\s*['"]?\//.test(html)) problems.push(`${rel}: root-relative url() in CSS`);
  const absInternal = [...html.matchAll(/\b(?:href|src|srcset)="https?:\/\/(?:www\.)?miannebenchwork\.com[^"]*"/g)]
    .map((m) => m[0])
    .filter((m) => !/rel="canonical"/.test(m));
  const canonCount = (html.match(/<link rel="canonical"/g) || []).length;
  if (absInternal.length > canonCount) problems.push(`${rel}: absolute internal URL outside canonical`);

  if (html.includes(EM_DASH)) problems.push(`${rel}: em dash`);

  if (!isAdmin) {
    const text = html
      .replace(/<script[\s\S]*?<\/script>/g, ' ')
      .replace(/<style[\s\S]*?<\/style>/g, ' ')
      .replace(/<[^>]+>/g, ' ');
    for (const re of forbidden) if (re.test(text)) problems.push(`${rel}: forbidden phrase ${re}`);
    const h1 = (html.match(/<h1[\s>]/g) || []).length;
    if (h1 !== 1) problems.push(`${rel}: ${h1} h1 tags`);
    if (!/<img[^>]+src="[^"]*images\/logoRGB\.png"[^>]*alt="Mianne Benchwork"/.test(html)) problems.push(`${rel}: logo img missing`);
    if (!/Powered by <a href="https:\/\/livewebstudios\.com"/.test(html)) problems.push(`${rel}: LWS credit missing`);
  }
}

for (const file of await walk(path.join(root, 'src'), ['.astro', '.ts', '.css', '.json', '.md'])) {
  const txt = await readFile(file, 'utf8');
  if (txt.includes(EM_DASH)) problems.push(`src/${path.relative(path.join(root, 'src'), file)}: em dash`);
}

if (problems.length) {
  console.error('\nLWS QA check FAILED:\n  ' + problems.join('\n  '));
  process.exit(1);
}
console.log('LWS QA check passed: relative paths, no em dashes, no forbidden copy, one H1 per page, logo + credit present.');
