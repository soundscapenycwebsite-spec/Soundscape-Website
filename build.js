'use strict';

const fs = require('fs');
const path = require('path');

const base = __dirname;

function readJsonDir(dir, label) {
  const fullDir = path.join(base, 'data', dir);
  if (!fs.existsSync(fullDir)) {
    console.warn('Directory not found, creating: ' + fullDir);
    fs.mkdirSync(fullDir, { recursive: true });
    return [];
  }
  try {
    const items = fs.readdirSync(fullDir)
      .filter(f => f.endsWith('.json'))
      .sort()
      .map(f => {
        const filePath = path.join(fullDir, f);
        try {
          return JSON.parse(fs.readFileSync(filePath, 'utf8'));
        } catch (e) {
          console.error('Failed to parse ' + filePath + ': ' + e.message);
          return null;
        }
      })
      .filter(item => item !== null);
    return items;
  } catch (e) {
    console.error('Error reading ' + dir + ' directory: ' + e.message);
    return [];
  }
}

try {
  const gearItems = readJsonDir('gear', 'gear');
  const pkgItems = readJsonDir('packages', 'packages');

  fs.writeFileSync(
    path.join(base, 'data', 'gear.json'),
    JSON.stringify({ items: gearItems }, null, 2) + '\n'
  );

  fs.writeFileSync(
    path.join(base, 'data', 'packages.json'),
    JSON.stringify({ items: pkgItems }, null, 2) + '\n'
  );

  console.log('Merged ' + gearItems.length + ' gear items -> data/gear.json');
  console.log('Merged ' + pkgItems.length + ' packages -> data/packages.json');
} catch (e) {
  console.error('Build failed: ' + e.message);
  process.exit(1);
}