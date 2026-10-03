// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import remarkCallouts from './src/lib/remark-callouts.mjs';
import rehypeBaseLinks from './src/lib/rehype-base-links.mjs';
import rehypeExternalLinks from './src/lib/rehype-external-links.mjs';

// GitHub Pages: https://drferhatu.github.io/discrete-mathematics/
// For a custom domain, build with SITE_URL and BASE_PATH=/ environment variables.
const site = process.env.SITE_URL ?? 'https://drferhatu.github.io';
const base = process.env.BASE_PATH ?? '/discrete-mathematics';

export default defineConfig({
  site,
  base,
  trailingSlash: 'ignore',
  // Inline CSS into each page: GitHub Pages caches HTML for ~10 minutes, and a cached page pointing at a
  // renamed (hashed) stylesheet would otherwise render unstyled right after every deploy.
  build: { inlineStylesheets: 'always' },
  integrations: [mdx(), sitemap()],
  markdown: {
    remarkPlugins: [remarkMath, remarkCallouts],
    rehypePlugins: [[rehypeKatex, { strict: false }], [rehypeBaseLinks, { base }], [rehypeExternalLinks, { site: site + base }]],
    shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' }, wrap: true },
  },
  vite: { plugins: [tailwindcss()] },
});
