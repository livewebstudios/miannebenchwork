import { defineConfig } from 'astro/config';

// Static output. CSS is inlined and all scripts are is:inline so the built HTML
// never references root-relative /_astro/ files (LWS relative-path rule).
export default defineConfig({
  site: 'https://miannebenchwork.com',
  trailingSlash: 'always',
  build: {
    format: 'directory',
    inlineStylesheets: 'always',
  },
  compressHTML: true,
  devToolbar: { enabled: false },
});
