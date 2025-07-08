const path = require('path');
const fs = require('fs/promises');

async function getFiles(dir) {
  try {
    const files = await fs.readdir(dir);
    return files.map(f => path.join(dir, f));
  } catch (err) {
    console.error('Failed to read directory', err);
    return [];
  }
}

async function moveFile(src, destDir) {
  const dest = path.join(destDir, path.basename(src));
  try {
    await fs.rename(src, dest);
    console.log(`Moved ${src} -> ${dest}`);
  } catch (err) {
    console.error(`Failed to move ${src}`, err);
  }
}

module.exports = {
  getFiles,
  moveFile
}
