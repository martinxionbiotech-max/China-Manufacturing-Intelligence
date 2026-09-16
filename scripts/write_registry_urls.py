#!/usr/bin/env python3
"""Write backfilled URLs into research/*.md src registry tables (add URL column)."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assign = json.load(open(os.path.join(ROOT, 'scripts', 'assignments.json')))

n_files = n_urls = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'research', '*.md'))):
    fname = os.path.basename(f)
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'(\| src id \| Title \| Publisher \| Level \| Date \|\n\|[-:\s|]+\|\n)(.*?)(?=\n## |\Z)', txt, re.S)
    if not m:
        print('no registry:', fname); continue
    amap = assign.get(fname, {})
    body = m.group(2)
    new_head = '| src id | Title | Publisher | Level | Date | URL |\n|--|--|--|--|--|--|\n'
    out_lines = []
    for line in body.split('\n'):
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 5:
            continue
        url = amap.get(cells[0], '')
        if url:
            n_urls += 1
            out_lines.append(line.rstrip() + ' ' + url + ' |')
        else:
            out_lines.append(line.rstrip() + ' |')
    new_block = new_head + '\n'.join(out_lines) + '\n'
    txt = txt[:m.start()] + new_block + txt[m.end():]
    open(f, 'w', encoding='utf-8').write(txt)
    n_files += 1

print(f'wrote URL column into {n_files} registry files; {n_urls} URLs filled')
