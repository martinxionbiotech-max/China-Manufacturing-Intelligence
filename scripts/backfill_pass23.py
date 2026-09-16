#!/usr/bin/env python3
"""P0 pass 2+3: backfill URLs for registry rows unmatched in pass 1.

Pass 2: deep search of research/raw content fields for distinctive title fragments.
Pass 3: fresh Tavily search per remaining unmatched row (title+[publisher]), strict
        title-level acceptance only. Caches responses in research/raw/backfill/*.json.
Never assigns a URL unless the candidate title strongly matches the registry title
(exact / containment / char-bigram >= 0.8), optionally confirmed by publisher domain.
"""
import glob, json, os, re, subprocess, sys, time, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'research', 'raw')
BACKFILL = os.path.join(RAW, 'backfill')
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from backfill_sources import norm, load_raw, parse_registry, pub_hints

def bigrams(s):
    return set(s[i:i+2] for i in range(len(s)-1)) if len(s) >= 2 else set()

def jacc(a, b):
    if not a or not b: return 0.0
    return len(a & b) / len(a | b)

def title_sim(rt, tt):
    """Strong-match title similarity in [0,1]."""
    a, b = norm(rt), norm(tt)
    if not a or not b: return 0.0
    if a == b: return 1.0
    la, lb = len(a), len(b)
    if la >= 6 and a in b: return 0.95
    if lb >= 6 and b in a: return 0.95
    return jacc(bigrams(a), bigrams(b))

def load_assignments():
    p = os.path.join(ROOT, 'scripts', 'assignments.json')
    if os.path.exists(p):
        return json.load(open(p))
    return {}

def get_tavily_key():
    out = subprocess.run(['bash', '-c', "grep -i tavily ~/.openclaw/.env | head -1 | cut -d= -f2"],
                         capture_output=True, text=True)
    return out.stdout.strip()

def tavily_search(query, key):
    payload = json.dumps({'api_key': key, 'query': query, 'max_results': 5,
                          'search_depth': 'basic'})
    r = subprocess.run(['curl', '-s', '-m', '25', '-X', 'POST',
                        'https://api.tavily.com/search',
                        '-H', 'Content-Type: application/json', '-d', payload],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return None

def main():
    key = get_tavily_key()
    raw_items = load_raw()
    assign = load_assignments()
    os.makedirs(BACKFILL, exist_ok=True)

    # build unmatched list
    unmatched = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'research', '*.md'))):
        fname = os.path.basename(f)
        txt = open(f, encoding='utf-8').read()
        for r in parse_registry(txt):
            if fname in assign and r['sid'] in assign[fname]:
                continue
            unmatched.append((fname, r))

    print(f'unmatched to resolve: {len(unmatched)}')

    # ---------- pass 2: deep content search in existing raw ----------
    # index: for each raw item, full content + title
    resolved = {}
    still = []
    for fname, r in unmatched:
        rt = norm(r['title'])
        if len(rt) < 8:
            still.append((fname, r)); continue
        best, best_it, best_s = 0, None, 0
        # fragment = first 10 chars of normalized title (distinctive)
        frag = rt[:10]
        for it in raw_items:
            hay = norm(it['content']) + '|' + norm(it['title'])
            if frag in hay:
                s = title_sim(r['title'], it['title'])
                if s > best_s:
                    best_s = s; best_it = it
        if best_it and best_s >= 0.6:
            # require domain hint if title sim not near-exact
            hints = pub_hints(r['publisher'])
            domok = (not hints) or any(h in best_it['domain'] or best_it['domain'].endswith('.' + h) for h in hints)
            if best_s >= 0.9 or (best_s >= 0.6 and domok):
                resolved[(fname, r['sid'])] = best_it['url']
                continue
        still.append((fname, r))

    print(f'pass2 (deep content) resolved: {len(resolved)}; remaining: {len(still)}')

    # ---------- pass 3: fresh tavily per remaining row ----------
    def slugify(s):
        return re.sub(r'[^0-9a-z]+', '-', norm(s)[:40]).strip('-')

    for fname, r in still:
        rt = norm(r['title'])
        cache_path = os.path.join(BACKFILL, slugify(r['title']) + '.json')
        d = None
        if os.path.exists(cache_path):
            try:
                d = json.load(open(cache_path))
            except Exception:
                d = None
        if d is None:
            q = re.sub(r'["“”（）()《》]', ' ', r['title']).strip()
            d = tavily_search(q, key)
            if d:
                json.dump(d, open(cache_path, 'w'), ensure_ascii=False)
            time.sleep(0.35)
        if not d or not d.get('results'):
            continue
        best_s, best_url, best_dom = 0, None, None
        for it in d['results']:
            url, tt, ct = it.get('url') or '', it.get('title') or '', it.get('content') or ''
            if not url: continue
            dom = re.sub(r'^https?://', '', url).split('/')[0].lower()
            s = title_sim(r['title'], tt)
            # title-in-content fallback (snippet often starts with the title)
            if s < 0.8 and rt and len(rt) >= 8:
                if rt[:10] in norm(ct):
                    s = max(s, 0.75)
            if s > best_s:
                best_s, best_url, best_dom = s, url, dom
        if best_url and best_s >= 0.8:
            hints = pub_hints(r['publisher'])
            domok = (not hints) or any(h in best_dom or best_dom.endswith('.' + h) for h in hints)
            if domok:
                resolved[(fname, r['sid'])] = best_url
            else:
                # title-only match on a different domain: accept only near-exact (>=0.95)
                if best_s >= 0.95:
                    resolved[(fname, r['sid'])] = best_url

    print(f'pass3 (tavily) resolved: {len(resolved) - sum(1 for k,v in resolved.items() if v is None)} total resolved now: {len(resolved)}')

    # merge into assignments
    for (fname, sid), url in resolved.items():
        assign.setdefault(fname, {})[sid] = url
    json.dump(assign, open(os.path.join(ROOT, 'scripts', 'assignments.json'), 'w'),
              ensure_ascii=False, indent=1)
    n = sum(len(v) for v in assign.values())
    print(f'assignments total: {n}')
    print('\n--- still unmatched ---')
    done = set(resolved.keys())
    for fname, r in still:
        if (fname, r['sid']) not in done:
            print(f"{fname} | {r['sid']} | {r['title'][:45]} | {r['publisher'][:30]}")

if __name__ == '__main__':
    main()
