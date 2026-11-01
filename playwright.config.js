import { defineConfig } from '@playwright/test';

if (process.env.TOMBO_VISUAL_CONTAINER !== '1' || process.platform !== 'linux' || process.arch !== 'x64') {
  throw new Error('Use npm run test:visual (or test:visual:update) for the pinned Linux/amd64 environment.');
}

export default defineConfig({
  testDir: './tests/visual',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  forbidOnly: true,
  updateSnapshots: 'none',
  snapshotPathTemplate: '{testDir}/snapshots/{arg}{ext}',
  reporter: [['list'], ['html', { open: 'never' }]],
  expect: {
    timeout: 15_000,
    toHaveScreenshot: { animations: 'disabled', maxDiffPixels: 0 },
  },
  use: {
    browserName: 'chromium',
    deviceScaleFactor: 1,
    locale: 'en-US',
    timezoneId: 'UTC',
    colorScheme: 'light',
    baseURL: 'http://127.0.0.1:4173',
    trace: 'retain-on-failure',
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1280, height: 900 } } },
    {
      name: 'mobile',
      snapshotPathTemplate: '{testDir}/snapshots/mobile/{arg}{ext}',
      use: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true },
    },
  ],
  webServer: {
    command: 'python3 -m http.server 4173 --bind 127.0.0.1',
    url: 'http://127.0.0.1:4173/examples/components.html',
    reuseExistingServer: false,
  },
});
