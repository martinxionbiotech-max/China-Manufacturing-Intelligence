#!/usr/bin/env python3
"""Backfill URLs into content/*/*.md `## Sources` numbered lists by matching titles
against the (now URL-bearing) research src registries + raw research results.
Only exact/near-exact title matches are used — never guessed."""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from backfill_sources import norm, parse_registry, load_raw, pub_hints

# global registry: normalized title -> url (and sid)
title_url = {}
sid_url = {}
for f in glob.glob(os.path.join(ROOT, 'research', '*.md')):
    txt = open(f, encoding='utf-8').read()
    for r in parse_registry(txt):
        # parse the URL cell from raw table line (we appended URL column)
        m = re.search(r'^\|\s*' + re.escape(r['sid']) + r'\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\s*(https?://\S+)\s*\|', txt, re.M)
        url = m.group(1) if m else ''
        if url:
            title_url.setdefault(norm(r['title']), set()).add(url)
            sid_url[r['sid']] = url

# also index raw research results directly (titles may not be in registry)
raw_items = load_raw()
raw_title_url = {}
for it in raw_items:
    raw_title_url.setdefault(norm(it['title']), set()).add(it['url'])

def big(x):
    return set(x[i:i+2] for i in range(len(x)-1))

def jaccard(a, b):
    b1, b2 = big(a), big(b)
    return len(b1 & b2) / max(1, len(b1 | b2)) if b1 and b2 else 0

def find_url(title):
    n = norm(title)
    if n in title_url:
        return sorted(title_url[n])[0]
    if n in raw_title_url:
        return sorted(raw_title_url[n])[0]
    # near match: registry first (higher trust), then raw
    best, bestu = 0.8, None
    for src in (title_url, raw_title_url):
        for tn, urls in src.items():
            j = jaccard(n, tn)
            if j > best:
                best, bestu = j, sorted(urls)[0]
    return bestu if best >= 0.85 else None

n_files = n_links = 0
for f in sorted(glob.glob(os.path.join(ROOT, 'content', '*', '*.md'))):
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'^## Sources\n(.*?)(?=\n## |\Z)', txt, re.S | re.M)
    if not m:
        continue
    sec = m.group(1)
    lines = sec.split('\n')
    changed = False
    out = []
    for i, line in enumerate(lines):
        is_last = (i == len(lines) - 1)
        nl = '' if is_last else '\n'
        stripped = line.rstrip()
        if not stripped or not re.match(r'^\d+\.\s', stripped):
            out.append(stripped + nl)
            continue
        # skip lines already having a URL
        if re.search(r'https?://', stripped):
            out.append(stripped + nl)
            continue
        # extract quoted title
        tm = re.search(r'[""]([^""]{6,})[""]', stripped)
        url = None
        if tm:
            url = find_url(tm.group(1))
        if not url:
            # try entity-ref form: 'Ningde power battery cluster (cls-xxx)'
            em = re.search(r'\((cls-[a-z0-9\-]+)\)', stripped)
            if em and em.group(1) in sid_url:
                url = sid_url[em.group(1)]
        if url:
            stripped = stripped.rstrip() + ' ' + url
            changed = True
            n_links += 1
        out.append(stripped + nl)
    if changed:
        txt = txt[:m.start(1)] + ''.join(out) + txt[m.end(1):]
        open(f, 'w', encoding='utf-8').write(txt)
        n_files += 1

print(f'content files updated: {n_files}, URL links appended: {n_links}')
