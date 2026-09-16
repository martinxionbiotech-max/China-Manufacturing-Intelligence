#!/usr/bin/env python3
"""Batch-fetch Chinese-language industry/product market data via Tavily.
Saves each result to research/raw/hub-<id>.json with rate limiting.
"""
import json, os, re, time, glob, yaml, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'research', 'raw')
os.makedirs(RAW, exist_ok=True)

def get_key():
    env = os.path.expanduser('~/.openclaw/.env')
    for line in open(env):
        if 'tavily' in line.lower() and '=' in line:
            return line.split('=', 1)[1].strip().strip('"').strip("'")
    raise RuntimeError('no tavily key')

KEY = get_key()

def fetch(query, slug):
    out = os.path.join(RAW, f'hub-{slug}.json')
    if os.path.exists(out) and os.path.getsize(out) > 500:
        return 'skip'
    payload = json.dumps({
        'api_key': KEY,
        'query': query,
        'max_results': 5,
        'search_depth': 'advanced',
    }).encode()
    req = urllib.request.Request('https://api.tavily.com/search',
                                 data=payload,
                                 headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
        open(out, 'wb').write(data)
        j = json.loads(data)
        n = len(j.get('results', []))
        return f'{n} results ({len(data)}B)'
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        return f'HTTP {e.code}: {body}'
    except Exception as e:
        return f'ERR {e}'

# Build query list from industries + products
queries = []
for kind in ['industries', 'products']:
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'entities', kind, '*.yaml'))):
        d = yaml.safe_load(open(f, encoding='utf-8'))
        zh = d.get('name_zh', '')
        en = d.get('name_en', '')
        q = f"{zh} 产业 2024 2025 规模 产量 出口 市场 数据"
        queries.append((q, d['id']))

print(f'共 {len(queries)} 个查询')
for i, (q, slug) in enumerate(queries, 1):
    r = fetch(q, slug)
    print(f'[{i}/{len(queries)}] {slug}: {r}')
    if r.startswith('HTTP 429') or r.startswith('HTTP 432'):
        print('!! RATE LIMIT — 停止')
        break
    time.sleep(1.5)
print('done')
