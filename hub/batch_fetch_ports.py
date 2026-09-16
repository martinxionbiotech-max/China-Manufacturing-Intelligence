#!/usr/bin/env python3
"""Batch-fetch China major port throughput data via Tavily.
Saves to research/raw/port-<slug>.json with rate limiting.
"""
import json, os, time, urllib.request

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

# (slug, 中文查询)
PORTS = [
    ('prt-shanghai', '上海港 2024 集装箱吞吐量 货物吞吐量 全球排名 数据'),
    ('prt-ningbo-zhoushan', '宁波舟山港 2024 集装箱吞吐量 货物吞吐量 全球第一 数据'),
    ('prt-shenzhen', '深圳港 2024 集装箱吞吐量 盐田 蛇口 全球排名 数据'),
    ('prt-guangzhou', '广州港 南沙 2024 集装箱吞吐量 货物吞吐量 数据'),
    ('prt-qingdao', '青岛港 2024 集装箱吞吐量 货物吞吐量 数据'),
    ('prt-tianjin', '天津港 2024 集装箱吞吐量 货物吞吐量 数据'),
    ('prt-suzhou', '苏州港 太仓港 2024 集装箱吞吐量 内河第一大港 数据'),
    ('prt-xiamen', '厦门港 2024 集装箱吞吐量 数据'),
    ('prt-yantai', '烟台港 2024 集装箱吞吐量 货物吞吐量 数据'),
    ('prt-quanzhou', '泉州港 2024 货物吞吐量 集装箱 数据'),
    ('prt-nantong', '南通港 2024 货物吞吐量 集装箱 数据'),
    ('prt-weihai', '威海港 2024 货物吞吐量 集装箱 数据'),
]

def fetch(slug, query):
    out = os.path.join(RAW, f'port-{slug}.json')
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
        return f'HTTP {e.code}'
    except Exception as e:
        return f'ERR {e}'

print(f'共 {len(PORTS)} 个港口查询')
for i, (slug, q) in enumerate(PORTS, 1):
    r = fetch(slug, q)
    print(f'[{i}/{len(PORTS)}] {slug}: {r}')
    if r.startswith('HTTP 429') or r.startswith('HTTP 432'):
        print('!! RATE LIMIT — 停止')
        break
    time.sleep(1.5)
print('done')
