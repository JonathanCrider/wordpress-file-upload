const { chromium } = require('playwright');
const { getFiles, moveFile } = require('./utils');
const os = require('os');
const path = require('path');
const fs = require('fs/promises');
require('dotenv').config();

const year = new Date().getFullYear();
const ROOT_DIRECTORY = process.env.ROOT_DIRECTORY
const DIRECTORY = path.join(os.homedir(), `${ROOT_DIRECTORY}${year}/${process.env.DIRECTORY}`);
const DESTINATION = path.join(os.homedir(), `${ROOT_DIRECTORY}${year}/${process.env.DESTINATION}`);

(async () => {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();
  
  const username = process.env.WORDPRESS_USERNAME;
  const password = process.env.WORDPRESS_PASSWORD;
  const site = process.env.WORDPRESS_SITE;
  const files = await getFiles(DIRECTORY);

  // Login to WordPress
  await page.goto('https://wordpress.com/log-in');
  await page.fill('input[name="usernameOrEmail"]', username);
  await page.click('button[type="submit"]');
  await page.waitForSelector('input[name="password"]', { timeout: 10000 });
  await page.fill('input[name="password"]', password);
  await page.click('button[type="submit"]');
  await page.waitForURL(`**/home/${site}`);

  // Go to the Media Library
  await page.goto(`https://wordpress.com/media/library/https://${site}`);
  await page.getByRole('button', { name: 'Add Media File' }).click();

  for (const filePath of files) {
    console.log('Uploading:', filePath);

    // Wait for file input
    const fileInput = await page.waitForSelector('input[type="file"]');

    // Upload file
    await fileInput.setInputFiles(filePath);

    // Wait some time or better, wait for upload confirmation
    await page.waitForTimeout(5000);

    // Move file to uploaded folder
    await moveFile(filePath, DESTINATION);
  }

  await browser.close();
})();
