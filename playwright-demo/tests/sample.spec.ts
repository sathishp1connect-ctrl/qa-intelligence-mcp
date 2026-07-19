import { test, expect } from '@playwright/test';

test('passing test', async () => {
  expect(1 + 1).toBe(2);
});

test('failing test', async () => {
  expect(1 + 1).toBe(3);
});

test.skip('skipped test', async () => {
  expect(true).toBe(true);
});

test('flaky test', async ({}, testInfo) => {
  if (testInfo.retry === 0) {
    expect(1).toBe(2);
  }

  expect(1).toBe(1);
});