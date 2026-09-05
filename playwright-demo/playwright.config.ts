import { defineConfig } from '@playwright/test';

const worker = process.env.WORKER_NAME || 'worker-local';

export default defineConfig({
  testDir: './tests',
  retries: 1,

  reporter: [
    ['list'],
    ['html', { outputFolder: `reports/${worker}/html`, open: 'never' }],
    ['json', { outputFile: `reports/${worker}/results.json` }]
  ]
});