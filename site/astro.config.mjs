import { defineConfig } from 'astro/config';
import { normalizeCityLinks } from './rehype-normalize-links.mjs';

// Canonical domain is a placeholder until the site is deployed to its real host.
const SITE = process.env.SITE_URL || 'https://chinamanufacturingintel.example';

export default defineConfig({
  site: SITE,
  output: 'static',
  trailingSlash: 'always',
  markdown: {
    rehypePlugins: [normalizeCityLinks],
  },
});
