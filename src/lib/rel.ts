// Relative path helper. Every internal link and asset goes through here so the
// built site works on any host or subfolder (LWS rule: no root-relative paths).
// Pages build to /section/page/index.html, so depth = number of path segments.
export function prefixFor(url: URL, forceRoot = false): string {
  if (forceRoot) return '';
  const depth = url.pathname.split('/').filter(Boolean).length;
  return depth ? '../'.repeat(depth) : '';
}

export function rel(url: URL, target = '', forceRoot = false): string {
  const p = prefixFor(url, forceRoot);
  if (!target) return p || './';
  return p + target.replace(/^\.?\//, '');
}

export const SITE = 'https://miannebenchwork.com';

export function canonical(url: URL): string {
  return SITE + url.pathname;
}
