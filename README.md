# miannebenchwork.com

Astro 5 static site for Mianne Benchwork (Mianne Foley Woodworking Inc., Attleboro MA).
Built by Live Web Studios.

## Commands

```bash
npm install
npm run dev        # local dev server
npm run build      # astro build + LWS QA guard (fails on root-relative paths, em dashes, forbidden copy, H1 count)
npx serve dist     # preview the built site
```

## Where things live

- `src/data/products.json`: the catalog. Source of truth for every model, size, price and use-case line. Edit here, rebuild, done.
- `src/data/categoryPages.ts`: H1, intro copy, title and meta for each catalog category page.
- `src/data/blog.json`: blog posts, written by Decap CMS (`/admin/`).
- `public/images/products/`: one diagram per model, named to match `products.json`.
  - `scripts/fetch-old-images.mjs` re-downloads the kit diagrams from the old WordPress site.
  - `scripts/make-diagrams.py` resizes those and draws the plan diagrams for models that never had one (needs Pillow).
- `netlify.toml`: build settings, the 301 map from the old WordPress URLs, cache and security headers.

## Placeholders to fill before launch

- `GA4_PLACEHOLDER` in `src/layouts/Base.astro`
- `GSC_PLACEHOLDER` in `src/layouts/Base.astro` (or verify by DNS)
- `FORMSPREE_PLACEHOLDER` in `src/components/ContactForm.astro`

## Rules this codebase follows

- Every internal link and asset path is relative (`src/lib/rel.ts`). Canonicals, og:image and JSON-LD are the only absolute URLs.
- CSS is inlined and all scripts are `is:inline`, so the build never emits root-relative `/_astro/` files.
- The 404 page carries `<base href="/">` because Netlify serves it at arbitrary URLs.
- Decap CMS is pinned to exactly 3.1.2 in `public/admin/index.html`. Do not loosen it.
