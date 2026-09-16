#!/usr/bin/env python3
"""China Manufacturing Intelligence — Database Hub generator.
Reads data/entities/*.yaml and emits structured MkDocs pages under hub/docs/.
No invented data: every fact rendered comes from the YAML verified_facts.
"""
import os, re, glob, yaml
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENT = os.path.join(ROOT, 'data', 'entities')
DOCS = os.path.join(ROOT, 'hub', 'docs')

KIND_DIRS = {
    'clusters': 'clusters',
    'cities': 'cities',
    'industries': 'industries',
    'products': 'products',
    'ports': 'ports',
}
KIND_LABEL = {
    'clusters': 'Manufacturing Clusters',
    'cities': 'Manufacturing Cities',
    'industries': 'Industries',
    'products': 'Products',
    'ports': 'Ports',
}
KIND_SINGULAR = {
    'clusters': 'Cluster',
    'cities': 'City',
    'industries': 'Industry',
    'products': 'Product',
    'ports': 'Port',
}

def slugify(s):
    s = s.lower().strip()
    s = re.sub(r'\(.*?\)', '', s)          # drop parentheticals
    s = re.sub(r'[^a-z0-9]+', '-', s)
    return s.strip('-')

def load_all():
    entities = {}   # id -> dict (+kind)
    by_kind = defaultdict(list)
    for kind, sub in KIND_DIRS.items():
        for f in sorted(glob.glob(os.path.join(ENT, kind, '*.yaml'))):
            d = yaml.safe_load(open(f, encoding='utf-8'))
            d['_kind'] = kind
            d['_file'] = f
            entities[d['id']] = d
            by_kind[kind].append(d)
    return entities, by_kind

def link_id(eid, entities):
    """Return a markdown relative link for an entity id, else None."""
    if eid not in entities:
        return None
    d = entities[eid]
    return f"../{KIND_DIRS[d['_kind']]}/{d['id']}.md"

def esc(s):
    return str(s).replace('|', '\\|')

def render_verified_facts(d, entities):
    facts = d.get('verified_facts', [])
    if not facts:
        return ''
    lines = ['## Verified facts', '']
    for vf in facts:
        fact = vf.get('fact', '')
        src = vf.get('source', '')
        if src.startswith(('cls-', 'cty-', 'ind-', 'prd-', 'src-')):
            if src.startswith(('cls-', 'cty-', 'ind-', 'prd-')):
                l = link_id(src, entities)
                src_str = f"[{src}]({l})" if l else src
            else:
                src_str = src
        else:
            src_str = src
        lines.append(f"- {fact}  \n  *Source: {src_str}*")
    lines.append('')
    return '\n'.join(lines)

def render_cross_links(d, entities, title='Related entities'):
    parts = []
    for key, label in [('major_clusters', 'Clusters'), ('major_industries', 'Industries'),
                       ('major_products', 'Products'), ('major_cities', 'Cities')]:
        vals = d.get(key) or []
        if not vals:
            continue
        links = []
        for v in vals:
            if isinstance(v, str) and v in entities:
                links.append(f"[{entities[v]['name_en']}]({link_id(v, entities)})")
            elif isinstance(v, str):
                links.append(v)
        if links:
            parts.append(f"**{label}:** " + ', '.join(links))
    if not parts:
        return ''
    return f"## {title}\n\n" + '\n\n'.join(parts) + '\n'

# ---------- per-kind page renderers ----------

def render_cluster(d, entities):
    lines = []
    lines.append(f"# {d['name_en']}")
    lines.append('')
    zh = d.get('name_zh')
    if zh:
        lines.append(f"**{zh}** — *{KIND_SINGULAR[d['_kind']]}*")
        lines.append('')
    # designation
    des = d.get('designation')
    if des:
        lines.append(f"- **Designation:** {des}")
    loc = d.get('location') or {}
    prov = loc.get('province')
    city = loc.get('city')
    if prov or city:
        lines.append(f"- **Location:** {prov or ''}{', ' if prov and city else ''}{city or ''}")
    pi = d.get('primary_industry')
    if pi:
        lines.append(f"- **Primary industry:** {pi}")
    # key manufacturers table
    km = d.get('key_manufacturers')
    if km:
        lines += ['', '## Key manufacturers', '']
        lines.append('| Name | 中文 | Role | Note |')
        lines.append('|---|---|---|---|')
        for m in km:
            name = esc(m.get('name', ''))
            nz = esc(m.get('name_zh', ''))
            role = esc(m.get('role', ''))
            note = esc(m.get('note', ''))
            lines.append(f'| {name} | {nz} | {role} | {note} |')
        lines.append('')
    # key_market_entities (trade clusters)
    kme = d.get('key_market_entities')
    if kme:
        lines += ['## Key market entities', '']
        for m in kme:
            if isinstance(m, dict):
                lines.append(f"- {esc(m.get('name', m))}")
            else:
                lines.append(f"- {esc(m)}")
        lines.append('')
    # sub_areas
    sa = loc.get('sub_areas')
    if sa:
        lines += ['## Sub-areas', '']
        lines.append('| Area | 中文 | Role | Anchor |')
        lines.append('|---|---|---|---|')
        for a in sa:
            lines.append(f"| {esc(a.get('name',''))} | {esc(a.get('name_zh',''))} | {esc(a.get('role',''))} | {esc(a.get('anchor',''))} |")
        lines.append('')
    # ports
    ports = d.get('ports')
    if ports:
        lines += ['## Ports & logistics', '']
        for p in ports:
            if isinstance(p, dict):
                lines.append(f"- {esc(p.get('name',''))} ({esc(p.get('name_zh',''))}) — {esc(p.get('role',''))}")
            else:
                lines.append(f"- {esc(p)}")
        lines.append('')
    # products
    mp = d.get('major_products')
    if mp:
        lines += ['## Major products', '']
        for p in mp:
            lines.append(f"- {esc(p)}")
        lines.append('')
    # related industries
    ri = d.get('related_industries')
    if ri:
        lines += ['## Related industries', '']
        for x in ri:
            lines.append(f"- {esc(x)}")
        lines.append('')
    lines.append(render_verified_facts(d, entities))
    lines.append(render_cross_links(d, entities))
    # metadata
    lines += ['## Metadata', '']
    lines.append(f"- **Entity id:** `{d['id']}`")
    lines.append(f"- **Type:** {d.get('type','')}")
    lines.append(f"- **Evidence level:** {d.get('evidence_level','')}")
    lines.append(f"- **Confidence:** {d.get('confidence','')}")
    lines.append(f"- **Last verified:** {d.get('last_verified','')}")
    lines.append('')
    return '\n'.join(lines)

def render_city(d, entities):
    lines = [f"# {d['name_en']}", '']
    zh = d.get('name_zh')
    if zh:
        lines.append(f"**{zh}** — *{KIND_SINGULAR[d['_kind']]}*")
        lines.append('')
    lines.append(f"- **Province:** {d.get('province','')}")
    ports = d.get('ports')
    if ports:
        links = []
        for p in ports:
            if p in entities:
                links.append(f"[{entities[p]['name_en']}]({link_id(p, entities)})")
            else:
                links.append(p)
        lines.append(f"- **Ports:** " + ', '.join(links))
    lines.append(render_cross_links(d, entities))
    lines.append(render_verified_facts(d, entities))
    lines += ['## Metadata', '']
    lines.append(f"- **Entity id:** `{d['id']}`")
    lines.append(f"- **Type:** {d.get('type','')}")
    lines.append(f"- **Evidence level:** {d.get('evidence_level','')}")
    lines.append(f"- **Confidence:** {d.get('confidence','')}")
    lines.append(f"- **Last verified:** {d.get('last_verified','')}")
    lines.append('')
    return '\n'.join(lines)

def render_industry(d, entities):
    lines = [f"# {d['name_en']}", '']
    zh = d.get('name_zh')
    if zh:
        lines.append(f"**{zh}** — *{KIND_SINGULAR[d['_kind']]}*")
        lines.append('')
    ss = d.get('super_sector')
    gb = d.get('gb_code')
    if ss:
        lines.append(f"- **Super sector:** {ss}")
    if gb:
        lines.append(f"- **GB code:** {gb}")
    lines.append(render_cross_links(d, entities))
    lines.append(render_verified_facts(d, entities))
    lines += ['## Metadata', '']
    lines.append(f"- **Entity id:** `{d['id']}`")
    lines.append(f"- **Type:** {d.get('type','')}")
    lines.append(f"- **Evidence level:** {d.get('evidence_level','')}")
    lines.append(f"- **Confidence:** {d.get('confidence','')}")
    lines.append(f"- **Last verified:** {d.get('last_verified','')}")
    lines.append('')
    return '\n'.join(lines)

def render_port(d, entities):
    lines = [f"# {d['name_en']}", '']
    zh = d.get('name_zh')
    if zh:
        lines.append(f"**{zh}** — *{KIND_SINGULAR[d['_kind']]}*")
        lines.append('')
    lines.append(f"- **City:** {d.get('city','')}")
    lines.append(f"- **Province:** {d.get('province','')}")
    serves = d.get('serves') or []
    if serves:
        links = []
        for v in serves:
            if v in entities:
                links.append(f"[{entities[v]['name_en']}]({link_id(v, entities)})")
            else:
                links.append(v)
        lines.append(f"- **Serves clusters:** " + ', '.join(links))
    lines.append('')
    lines.append(render_verified_facts(d, entities))
    lines += ['## Metadata', '']
    lines.append(f"- **Entity id:** `{d['id']}`")
    lines.append(f"- **Type:** {d.get('type','')}")
    lines.append(f"- **Evidence level:** {d.get('evidence_level','')}")
    lines.append(f"- **Confidence:** {d.get('confidence','')}")
    lines.append(f"- **Last verified:** {d.get('last_verified','')}")
    lines.append('')
    return '\n'.join(lines)

def render_product(d, entities):
    lines = [f"# {d['name_en']}", '']
    zh = d.get('name_zh')
    if zh:
        lines.append(f"**{zh}** — *{KIND_SINGULAR[d['_kind']]}*")
        lines.append('')
    ind = d.get('industry')
    if ind:
        lines.append(f"- **Industry:** {ind}")
    hs = d.get('hs_codes')
    if hs:
        lines.append(f"- **HS codes:** {', '.join(str(x) for x in hs)}")
    comp = d.get('components')
    if comp:
        lines.append(f"- **Components:** {', '.join(esc(x) for x in comp)}")
    em = d.get('export_markets')
    if em:
        lines.append(f"- **Export markets:** {', '.join(esc(x) for x in em)}")
    lines.append(render_cross_links(d, entities))
    lines.append(render_verified_facts(d, entities))
    lines += ['## Metadata', '']
    lines.append(f"- **Entity id:** `{d['id']}`")
    lines.append(f"- **Type:** {d.get('type','')}")
    lines.append(f"- **Evidence level:** {d.get('evidence_level','')}")
    lines.append(f"- **Confidence:** {d.get('confidence','')}")
    lines.append(f"- **Last verified:** {d.get('last_verified','')}")
    lines.append('')
    return '\n'.join(lines)

RENDERERS = {
    'clusters': render_cluster,
    'cities': render_city,
    'industries': render_industry,
    'products': render_product,
    'ports': render_port,
}

# ---------- index pages ----------

def render_kind_index(kind, items, entities):
    lines = [f"# {KIND_LABEL[kind]}", '']
    lines.append(f"{len(items)} entities. Sorted alphabetically.")
    lines.append('')
    lines.append('| Entity | 中文 | Key attributes |')
    lines.append('|---|---|---|')
    for d in sorted(items, key=lambda x: x['name_en'].lower()):
        attrs = []
        if kind == 'clusters':
            loc = d.get('location') or {}
            if loc.get('city'):
                attrs.append(str(loc.get('city')))
            pi = d.get('primary_industry')
            if pi:
                attrs.append(str(pi))
        elif kind == 'cities':
            attrs.append(str(d.get('province','')))
        elif kind == 'industries':
            if d.get('super_sector'):
                attrs.append(str(d.get('super_sector')))
        elif kind == 'products':
            if d.get('hs_codes'):
                attrs.append('HS ' + ', '.join(str(x) for x in d.get('hs_codes')))
        elif kind == 'ports':
            if d.get('province'):
                attrs.append(str(d.get('province')))
            if d.get('serves'):
                attrs.append(f"serves {len(d.get('serves'))} clusters")
        lines.append(f"| [{esc(d['name_en'])}]({d['id']}.md) | {esc(d.get('name_zh',''))} | {esc(' · '.join(attrs))} |")
    lines.append('')
    return '\n'.join(lines)

def render_province_index(city_items):
    prov = defaultdict(list)
    for d in city_items:
        prov[d.get('province','?')].append(d)
    lines = ['# Provinces & Regions', '']
    lines.append(f"{len(prov)} provinces/regions hosting the 41 tracked cities.")
    lines.append('')
    lines.append('| Province / Region | Cities |')
    lines.append('|---|---|')
    for p in sorted(prov.keys()):
        city_links = ', '.join(f"[{d['name_en']}](../cities/{d['id']}.md)" for d in sorted(prov[p], key=lambda x: x['name_en'].lower()))
        lines.append(f"| {esc(p)} | {city_links} |")
    lines.append('')
    return '\n'.join(lines)

def render_hs_index(product_items):
    hs = defaultdict(list)
    for d in product_items:
        for code in (d.get('hs_codes') or []):
            hs[str(code)].append(d)
    lines = ['# HS Code Index', '']
    lines.append(f"{len(hs)} distinct 4-digit HS codes across {len(product_items)} products.")
    lines.append('')
    lines.append('| HS code | Product |')
    lines.append('|---|---|')
    for code in sorted(hs.keys()):
        plinks = ', '.join(f"[{d['name_en']}](products/{d['id']}.md)" for d in hs[code])
        lines.append(f"| {code} | {plinks} |")
    lines.append('')
    return '\n'.join(lines)

def render_sources_index(entities):
    counter = Counter()
    for eid, d in entities.items():
        for vf in d.get('verified_facts', []):
            counter[vf.get('source','?')] += 1
    lines = ['# Source Index', '']
    lines.append(f"{len(counter)} distinct source references across {len(entities)} entities "
                 f"and {sum(counter.values())} fact citations.")
    lines.append('')
    lines.append('| Source | Citations |')
    lines.append('|---|---|')
    for s, c in sorted(counter.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| {esc(s)} | {c} |")
    lines.append('')
    return '\n'.join(lines)

def render_home(entities, by_kind):
    lines = ['# China Manufacturing Intelligence — Data Hub', '']
    lines.append('Structured knowledge graph of China\'s manufacturing geography: industrial '
                 'clusters, cities, industries, and products. Every fact below is drawn from '
                 'verified sources with evidence levels.')
    lines.append('')
    lines.append('## Entity counts')
    lines.append('')
    lines.append('| Dimension | Entities | Evidence High |')
    lines.append('|---|---|---|')
    total = 0
    total_high = 0
    for kind in ['clusters', 'cities', 'industries', 'products', 'ports']:
        items = by_kind[kind]
        high = sum(1 for d in items if d.get('evidence_level') == 'High')
        total += len(items)
        total_high += high
        lines.append(f"| [{KIND_LABEL[kind]}]({KIND_DIRS[kind]}/index.md) | {len(items)} | {high} |")
    lines.append(f"| **Total** | **{total}** | **{total_high}** |")
    lines.append('')
    lines.append('## Navigation')
    lines.append('')
    lines.append('- [Manufacturing Clusters](clusters/index.md)')
    lines.append('- [Manufacturing Cities](cities/index.md)')
    lines.append('- [Industries](industries/index.md)')
    lines.append('- [Products](products/index.md)')
    lines.append('- [Ports](ports/index.md)')
    lines.append('- [Provinces & Regions](provinces/index.md)')
    lines.append('- [HS Code Index](hs-codes.md)')
    lines.append('- [Source Index](sources.md)')
    lines.append('')
    lines.append('## Methodology')
    lines.append('')
    lines.append('This hub is the structured interface to the China Manufacturing Knowledge Graph. '
                 'It complements the editorial main site (research, analysis, and comparisons). '
                 'Facts are classified by evidence level (High) and each carries a source '
                 'reference. No production, market-share, ranking, or certification figure is '
                 'invented; where a figure cannot be verified it is omitted.')
    lines.append('')
    return '\n'.join(lines)

def main():
    entities, by_kind = load_all()

    # clean docs
    for kind in KIND_DIRS.values():
        os.makedirs(os.path.join(DOCS, kind), exist_ok=True)
    os.makedirs(os.path.join(DOCS, 'provinces'), exist_ok=True)

    counts = {}
    # entity pages
    for kind, sub in KIND_DIRS.items():
        renderer = RENDERERS[kind]
        for d in by_kind[kind]:
            out = os.path.join(DOCS, sub, d['id'] + '.md')
            open(out, 'w', encoding='utf-8').write(renderer(d, entities))
        # index
        idx = render_kind_index(kind, by_kind[kind], entities)
        open(os.path.join(DOCS, sub, 'index.md'), 'w', encoding='utf-8').write(idx)
        counts[kind] = len(by_kind[kind])

    # province index (single aggregated page)
    open(os.path.join(DOCS, 'provinces', 'index.md'), 'w', encoding='utf-8').write(
        render_province_index(by_kind['cities']))

    # hs codes index
    open(os.path.join(DOCS, 'hs-codes.md'), 'w', encoding='utf-8').write(
        render_hs_index(by_kind['products']))

    # sources index
    open(os.path.join(DOCS, 'sources.md'), 'w', encoding='utf-8').write(
        render_sources_index(entities))

    # home
    open(os.path.join(DOCS, 'index.md'), 'w', encoding='utf-8').write(
        render_home(entities, by_kind))

    print('=== Hub 生成完成 ===')
    for kind, c in counts.items():
        print(f'  {kind}: {c} 页')
    print(f'  provinces: 1 索引页')
    print(f'  hs-codes: 1 索引页')
    print(f'  sources: 1 索引页')
    print(f'  home: 1')
    total = sum(counts.values()) + 4 + 4  # entities + 4 kind index + home+prov+hs+sources
    print(f'  总计约 {sum(counts.values()) + 4 + 4} 页')

if __name__ == '__main__':
    main()
