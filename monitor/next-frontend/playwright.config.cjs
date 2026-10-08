const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  workers: 1,
  retries: process.env.CI ? 1 : 0,
  reporter: "list",
  use: { baseURL: "http://127.0.0.1:3001", browserName: "chromium", headless: true },
  webServer: {
    command: "npm run start",
    url: "http://127.0.0.1:3001",
    reuseExistingServer: true,
    timeout: 120000,
  },
});
