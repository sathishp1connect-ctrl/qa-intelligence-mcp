import { test, expect } from '@playwright/test';

test('addition works', async () => {
  expect(1 + 1).toBe(2);
});

test('string validation', async () => {
  expect('QA').toBe('QA');
});

test('boolean validation', async () => {
  expect(true).toBeTruthy();
});