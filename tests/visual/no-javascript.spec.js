import { test, expect } from '@playwright/test';
import { readdirSync } from 'node:fs';
import { useLocalFonts } from './local-fonts.js';

// Disable page scripts at the browser-context level, including inline boot code.
test.use({ javaScriptEnabled: false });

test.beforeEach(async ({ page }) => {
  await useLocalFonts(page);
});

const examples = readdirSync('examples').filter(name => name.endsWith('.html')).sort();
for (const example of examples) {
  test(`without JavaScript: ${example}`, async ({ page }) => {
    await page.goto(`/examples/${example}`);
    await expect(page.getByRole('main')).toBeVisible();
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await expect(page.locator('.tombo-themes')).toHaveCount(1);
    await expect(page.locator('.tombo-themes')).toBeHidden();
    await expect(page.locator('.tombo-copy')).toHaveCount(0);
    await expect(page.locator('html')).not.toHaveAttribute('data-theme');
    // These are the existing foundation colors, resolved by light-dark() in CSS.
    await page.emulateMedia({ colorScheme: 'light' });
    await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(242, 244, 239)');
    await page.emulateMedia({ colorScheme: 'dark' });
    await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(19, 23, 20)');
    if (example !== 'lp.html') {
      // The landing page has no repeated navigation; other examples have a skip link.
      await page.keyboard.press('Tab');
      await expect(page.locator('.tombo-skip-link')).toBeFocused();
      await page.keyboard.press('Enter');
      await expect(page.getByRole('main')).toBeFocused();
    }
  });
}

test('native form controls remain operable without JavaScript', async ({ page }) => {
  await page.goto('/examples/components.html');
  const name = page.getByRole('textbox', { name: 'PROJECT NAME' });
  await name.fill('');
  await expect(name).toHaveJSProperty('willValidate', true);
  await expect(page.locator('#d-name:invalid')).toHaveCount(1);
  await name.fill('sample-project');
  await expect(name).toHaveValue('sample-project');
  await expect(page.locator('#d-name:valid')).toHaveCount(1);
  const checkbox = page.getByRole('checkbox', { name: 'Validate responses' });
  await checkbox.focus();
  await page.keyboard.press('Space');
  await expect(checkbox).not.toBeChecked();
  const lenient = page.getByRole('radio', { name: 'Lenient mode' });
  await lenient.check();
  await expect(lenient).toBeChecked();
  await expect(page.getByRole('radio', { name: 'Strict mode' })).not.toBeChecked();
  await page.getByLabel('FRAMEWORK ADAPTER').selectOption({ label: 'Symfony' });
  await expect(page.getByLabel('FRAMEWORK ADAPTER')).toHaveValue('Symfony');
  await expect(page.getByLabel('LOCKED FIELD')).not.toBeEditable();
  await expect(page.getByLabel('DISABLED FIELD')).toBeDisabled();
});
