import { test, expect } from '@playwright/test';
import { useLocalFonts } from './local-fonts.js';

for (const theme of ['tombo', 'hotaru']) {
  test(`print remains legible and restores screen controls / ${theme}`, async ({ page }) => {
    await useLocalFonts(page);
    await page.addInitScript(theme => localStorage.setItem('tombo-theme', theme), theme);
    await page.goto('/examples/components.html');
    const root = page.locator('html');
    const code = page.locator('.tombo-code pre').first();
    const copy = page.getByRole('button', { name: 'Copy code' }).first();
    const themes = page.locator('.tombo-themes');
    await expect(root).toHaveAttribute('data-theme', theme);
    await expect(themes).toBeVisible();
    await expect(copy).toBeVisible();
    const screenCodeColor = await code.evaluate(el => getComputedStyle(el).color);

    await page.emulateMedia({ media: 'print' });
    // Paper output must not depend on a dark theme's background being printed.
    await expect(root).toHaveCSS('color-scheme', 'light');
    await expect(code).toHaveCSS('background-color', 'rgb(255, 255, 255)');
    await expect(code).toHaveCSS('color', 'rgb(26, 33, 29)');
    await expect(themes).toBeHidden();
    await expect(page.locator('.tombo-copy').first()).toBeHidden();
    await expect(page.locator('.tombo-skip-link')).toBeHidden();
    const glow = page.locator('.tombo-glow').first();
    await expect(glow).toHaveCSS('box-shadow', 'none');
    await expect(glow).toHaveCSS('background-image', 'none');
    await expect(page.locator('body')).toHaveCSS('transition-duration', '0s');

    // Trim marks are opt-in. This checks their generated boxes, not pagination.
    const marks = () => page.evaluate(() => ['::before', '::after'].map(pseudo => {
      const style = getComputedStyle(document.documentElement, pseudo);
      return { content: style.content, position: style.position, background: style.backgroundImage };
    }));
    expect((await marks()).map(mark => mark.content)).toEqual(['none', 'none']);
    await page.locator('body').evaluate(el => el.classList.add('tombo-trim'));
    for (const mark of await marks()) {
      expect(mark.content).toBe('""');
      expect(mark.position).toBe('fixed');
      expect(mark.background).not.toBe('none');
    }

    await page.emulateMedia({ media: 'screen' });
    await expect(root).toHaveAttribute('data-theme', theme);
    await expect(themes).toBeVisible();
    await expect(copy).toBeVisible();
    await expect(code).toHaveCSS('color', screenCodeColor);
    expect((await marks()).map(mark => mark.content)).toEqual(['none', 'none']);
  });
}
