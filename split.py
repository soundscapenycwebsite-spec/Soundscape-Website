import json, os

base = os.path.dirname(os.path.abspath(__file__))

# Split gear
gear_src = os.path.join(base, 'data', 'gear.json')
gear_dir = os.path.join(base, 'data', 'gear')
os.makedirs(gear_dir, exist_ok=True)

with open(gear_src, 'r', encoding='utf-8') as f:
    gear_data = json.load(f)

for item in gear_data['items']:
    filepath = os.path.join(gear_dir, item['id'] + '.json')
    with open(filepath, 'w', encoding='utf-8') as out:
        json.dump(item, out, ensure_ascii=False, indent=2)
        out.write('\n')

print('Created', len(gear_data['items']), 'gear files in', gear_dir)

# Split packages
pkg_src = os.path.join(base, 'data', 'packages.json')
pkg_dir = os.path.join(base, 'data', 'packages')
os.makedirs(pkg_dir, exist_ok=True)

with open(pkg_src, 'r', encoding='utf-8') as f:
    pkg_data = json.load(f)

for item in pkg_data['items']:
    filepath = os.path.join(pkg_dir, item['id'] + '.json')
    with open(filepath, 'w', encoding='utf-8') as out:
        json.dump(item, out, ensure_ascii=False, indent=2)
        out.write('\n')

print('Created', len(pkg_data['items']), 'package files in', pkg_dir)