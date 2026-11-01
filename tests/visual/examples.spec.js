import { test, expect } from '@playwright/test';
import { readFileSync, readdirSync } from 'node:fs';

// Preserve the site's family names and Martian Mono's width axis, but serve
// locked font files locally so Google Fonts availability cannot change a run.
const fonts = [
  ['instrument-sans', 'index.css'],
  ['m-plus-2', 'index.css'],
  ['martian-mono', 'standard.css'],
].map(([name, file]) => {
  const path = `node_modules/@fontsource-variable/${name}`;
  return readFileSync(`${path}/${file}`, 'utf8')
    .replaceAll(" Variable'", "'")
    .replaceAll('url(./files/', `url(http://127.0.0.1:4173/${path}/files/`);
}).join('\n');

const examples = readdirSync('examples').filter(name => name.endsWith('.html')).sort();

for (const example of examples) {
  for (const theme of ['tombo', 'hotaru']) {
    test(`${example} / ${theme}`, async ({ page }) => {
      const failures = [];
      page.on('pageerror', error => failures.push(error.message));
      page.on('requestfailed', request => failures.push(`Failed: ${request.url()}`));
      page.on('response', response => {
        if (response.status() >= 400) failures.push(`${response.status()}: ${response.url()}`);
      });
      await page.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.hostname === 'fonts.googleapis.com') {
          return route.fulfill({ contentType: 'text/css', body: fonts });
        }
        if (url.origin === 'http://127.0.0.1:4173') return route.continue();
        return route.abort();
      });
      await page.addInitScript(value => localStorage.setItem('tombo-theme', value), theme);
      await page.goto(`/examples/${example}`);
      await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
      await page.evaluate(async () => {
        await document.fonts.ready;
        for (const [font, text] of [
          ['600 16px "Instrument Sans"', 'TOMBO'],
          ['450 16px "M PLUS 2"', '日本語'],
          ['400 16px "Martian Mono"', '0123456789'],
        ]) {
          const loaded = await document.fonts.load(font, text);
          if (!loaded.length) throw new Error(`Missing font: ${font}`);
        }
      });
      const width = await page.evaluate(() => ({
        viewport: window.innerWidth,
        content: document.documentElement.scrollWidth,
      }));
      expect(width.viewport, 'layout viewport must match the configured width').toBe(page.viewportSize().width);
      expect(width.content, 'horizontal scrolling belongs inside overflow wrappers').toBeLessThanOrEqual(width.viewport);
      await expect(page).toHaveScreenshot(`${example.replace('.html', '')}-${theme}.png`, { fullPage: true });
      expect(failures).toEqual([]);
    });
  }
}
