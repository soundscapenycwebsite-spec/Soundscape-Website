const fs = require('fs');
const path = require('path');

const base = __dirname;

const gearDir = path.join(base, 'data', 'gear');
const pkgDir = path.join(base, 'data', 'packages');

const gearItems = fs.readdirSync(gearDir)
  .filter(f => f.endsWith('.json'))
  .sort()
  .map(f => JSON.parse(fs.readFileSync(path.join(gearDir, f), 'utf8')));

const pkgItems = fs.readdirSync(pkgDir)
  .filter(f => f.endsWith('.json'))
  .sort()
  .map(f => JSON.parse(fs.readFileSync(path.join(pkgDir, f), 'utf8')));

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