import { test, expect } from '@playwright/test';
import { useLocalFonts } from './local-fonts.js';

test.beforeEach(async ({ page }) => {
  await useLocalFonts(page);
});

test('keyboard theme selection persists and system clears the override', async ({ page }) => {
  await page.goto('/examples/components.html');
  const hotaru = page.locator('[data-tombo-theme="hotaru"]');
  const system = page.locator('[data-tombo-theme="system"]');
  await expect(system).toHaveAttribute('aria-pressed', 'true');
  await hotaru.focus();
  await page.keyboard.press('Enter');
  await expect(hotaru).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('[data-tombo-theme][aria-pressed="true"]')).toHaveCount(1);
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'hotaru');
  expect(await page.evaluate(() => localStorage.getItem('tombo-theme'))).toBe('hotaru');
  await page.reload();
  await expect(hotaru).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'hotaru');
  await system.focus();
  await page.keyboard.press('Space');
  await expect(system).toHaveAttribute('aria-pressed', 'true');
  await expect(hotaru).toHaveAttribute('aria-pressed', 'false');
  await expect(page.locator('html')).not.toHaveAttribute('data-theme');
  expect(await page.evaluate(() => localStorage.getItem('tombo-theme'))).toBeNull();
  await page.reload();
  await expect(system).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('html')).not.toHaveAttribute('data-theme');
});

for (const mode of ['success', 'rejected', 'unavailable', 'throws']) {
  test(`keyboard copy: ${mode}`, async ({ page }) => {
    // Control the browser capability boundary, not TOMBO's DOM or event handlers.
    await page.addInitScript(mode => {
      Object.defineProperty(navigator, 'clipboard', {
        configurable: true,
        value: mode === 'unavailable' ? undefined : {
          writeText(text) {
            window.copiedText = text;
            if (mode === 'throws') throw new Error('Clipboard blocked');
            return mode === 'rejected'
              ? Promise.reject(new Error('Clipboard denied'))
              : Promise.resolve();
          },
        },
      });
    }, mode);
    await page.goto('/examples/components.html');
    const figure = page.locator('.tombo-code').first();
    const pre = figure.locator('pre');
    const button = figure.getByRole('button', { name: 'Copy code' });
    const source = await pre.textContent();
    await expect(button).toHaveCount(1);
    await button.focus();
    await page.keyboard.press('Enter');
    if (mode === 'success') {
      await expect(page.getByRole('status')).toHaveText('Copied');
      expect(await page.evaluate(() => window.copiedText)).toBe(source);
      await expect(button).toHaveText('COPIED ✓');
      await expect(button).toBeFocused();
      await expect(button).toHaveText('COPY ⧉');
    } else {
      await expect(page.getByRole('status')).toHaveText('Press Ctrl or Cmd + C to copy');
      await expect(pre).toBeFocused();
      expect(await page.evaluate(() => window.getSelection().toString())).toBe(source);
      await expect(button).toHaveText('COPY ⧉');
    }
  });
}
