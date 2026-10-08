import type { APIRoute } from 'astro';
import { categories } from '../lib/catalog';
import { posts } from '../lib/blog';
import { SITE } from '../lib/rel';

// URLs match the canonicals exactly (trailing slash, per seo.md).
export const GET: APIRoute = () => {
  const today = new Date().toISOString().slice(0, 10);
  const pages: [string, string, string][] = [
    ['/', '1.00', 'monthly'],
    ['/catalog/', '0.90', 'monthly'],
    ...categories.map((c) => [`/catalog/${c.slug}/`, '0.80', 'monthly'] as [string, string, string]),
    ['/assembly/', '0.80', 'monthly'],
    ['/about/', '0.80', 'monthly'],
    ['/reviews/', '0.80', 'monthly'],
    ['/reviews/railroad-model-craftsman-1997/', '0.60', 'yearly'],
    ['/reviews/benchwork-can-be-fun/', '0.60', 'yearly'],
    ['/faqs/', '0.80', 'monthly'],
    ['/contact/', '0.80', 'monthly'],
  ];
  if (posts.length) {
    pages.push(['/blog/', '0.80', 'weekly']);
    posts.forEach((p) => pages.push([`/blog/${p.slug}/`, '0.70', 'monthly']));
  }
  const body =
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    pages
      .map(([u, pr, cf]) => `  <url><loc>${SITE}${u}</loc><lastmod>${today}</lastmod><changefreq>${cf}</changefreq><priority>${pr}</priority></url>`)
      .join('\n') +
    '\n</urlset>\n';
  return new Response(body, { headers: { 'Content-Type': 'application/xml' } });
};
