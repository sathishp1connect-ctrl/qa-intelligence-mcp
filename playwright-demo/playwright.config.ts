import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',

  retries: 1,

  reporter: [
    ['json', { outputFile: 'reports/results.json' }],
    ['html', { outputFolder: 'reports/html', open: 'never' }]
  ],

  use: {
    headless: true,
    screenshot: 'only-on-failure'
  }
});