import { test, expect } from '@playwright/test';
import { readdirSync } from 'node:fs';
import { useLocalFonts } from './local-fonts.js';

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
      await useLocalFonts(page);
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
