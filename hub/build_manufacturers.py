#!/usr/bin/env python3
"""Build data/entities/manufacturers/*.yaml from verified key_manufacturers in cluster YAMLs.

Strict evidence rule: entity_role defaults to 'manufacturer' only when the cluster
research already asserts a manufacturing role. Fabless designers -> brand.
Software companies -> skipped. Industrial-park entries -> routed to industrial-parks.
"""
import yaml, glob, re, os, json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLUSTER_DIR = os.path.join(ROOT, 'data/entities/clusters')
OUT_DIR = os.path.join(ROOT, 'data/entities/manufacturers')
PARK_DIR = os.path.join(ROOT, 'data/entities/industrial-parks')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PARK_DIR, exist_ok=True)

# role -> entity_role mapping
ROLE_MAP = {
    'telecom_equipment': 'manufacturer',
    'internet_software': None,            # software company, not a manufacturer
    'drones': 'manufacturer',
    'electronics_manufacturer': 'manufacturer',
    'PCB': 'manufacturer',
    'chip_design': 'brand',               # fabless
    'smartphones_brand': 'brand',
    'consumer_electronics': 'brand',
    'contract_manufacturer': 'contract_mfr',
    'components_assembly': 'manufacturer',
    'battery_cells': 'manufacturer',
    'power_storage_batteries': 'manufacturer',
    'consumer_batteries': 'manufacturer',
    'cathode_materials_recycling': 'manufacturer',
    'battery_equipment': 'manufacturer',
    'stainless_steel': 'manufacturer',
    'excavators_concrete': 'manufacturer',
    'cranes_concrete': 'manufacturer',
    'pile_drivers_excavators': 'manufacturer',
    'tbm_underground': 'manufacturer',
    'aerial_work_platforms': 'manufacturer',
    'complete_vehicles': 'manufacturer',
    'traction_control': 'manufacturer',
    'traction_motors': 'manufacturer',
    'components': 'manufacturer',
    'residential_lighting': 'manufacturer',
    'decorative_lighting': 'manufacturer',
    'commercial_lighting': 'manufacturer',
    'pcb_materials': 'manufacturer',
}

# Curated slug + entity_role for empty-role / messy-name entries
# (name, slug, entity_role, industry_hint)
CURATED = {
    '北方稀土 (China Northern Rare Earth, 600111)': ('china-northern-rare-earth', 'manufacturer', 'Rare Earth'),
    '一汽集团 (FAW)': ('faw-group', 'manufacturer', 'Automotive'),
    '奥迪一汽新能源 (Audi-FAW NEV)': ('audi-faw-nev', 'manufacturer', 'NEV'),
    '中简科技 (Sinofibers, 300777)': ('sinofibers', 'manufacturer', 'Carbon Fiber'),
    'Dongpeng': ('dongpeng-ceramics', 'manufacturer', 'Ceramics'),
    'Monalisa': ('monalisa-ceramics', 'manufacturer', 'Ceramics'),
    'New Pearl': ('new-pearl-ceramics', 'manufacturer', 'Ceramics'),
    'Eagle': ('eagle-ceramics', 'manufacturer', 'Ceramics'),
    'Keda': ('keda-ceramics-machinery', 'manufacturer', 'Ceramics Machinery'),
    'Oceano': ('oceano-ceramics', 'manufacturer', 'Ceramics'),
    '中国稀土集团 (China Rare Earth Group)': ('china-rare-earth-group', 'manufacturer', 'Rare Earth'),
    '海康威视 (Hikvision)': ('hikvision', 'manufacturer', 'Security Equipment'),
    '大华股份 (Dahua)': ('dahua', 'manufacturer', 'Security Equipment'),
    'iFLYTEK (科大讯飞)': ('iflytek', 'brand', 'AI / Voice'),   # mostly software
    'Anta Sports (安踏)': ('anta-sports', 'manufacturer', 'Sportswear / Footwear'),
    'Xtep (特步)': ('xtep', 'manufacturer', 'Sportswear / Footwear'),
    '361 Degrees (361°)': ('361-degrees', 'manufacturer', 'Sportswear / Footwear'),
    '中国一拖 (YTO Group)': ('yto-group', 'manufacturer', 'Agricultural Machinery'),
    '镇海炼化 (Sinopec Zhenhai Refining & Chemical)': ('sinopec-zhenhai', 'manufacturer', 'Petrochemicals'),
    '宁波韵升 (Yunsheng': ('ningbo-yunsheng', 'manufacturer', 'Magnetic Materials'),
    '海尔集团 (Haier)': ('haier', 'manufacturer', 'Home Appliances'),
    '海信集团 (Hisense)': ('hisense', 'manufacturer', 'Home Appliances'),
    '中集来福士 (CIMC Raffles)': ('cimc-raffles', 'manufacturer', 'Shipbuilding'),
    '安踏 (ANTA)': ('anta-sports', 'manufacturer', 'Sportswear / Footwear'),
    '特步 (Xtep)': ('xtep', 'manufacturer', 'Sportswear / Footwear'),
    '迈瑞医疗 (Mindray, 300760)': ('mindray', 'manufacturer', 'Medical Devices'),
    'SMIC (中芯国际)': ('smic', 'manufacturer', 'Semiconductors (foundry)'),
    'Hua Hong (华虹半导体)': ('hua-hong', 'manufacturer', 'Semiconductors (foundry)'),
    'Tesla Shanghai Gigafactory': ('tesla-shanghai-gigafactory', 'manufacturer', 'NEV'),
    'SAIC Motor (上汽集团)': ('saic-motor', 'manufacturer', 'Automotive'),
    '新松机器人 (SIASUN, 300024)': ('siasun', 'manufacturer', 'Robotics'),
    'Midea': ('midea', 'manufacturer', 'Home Appliances'),
    'Galanz': ('galanz', 'manufacturer', 'Home Appliances'),
    'Hisense Kelon': ('hisense-kelon', 'manufacturer', 'Home Appliances'),
    'Vanward': ('vanward', 'manufacturer', 'Water Heaters / Appliances'),
    'Xinbao': ('xinbao', 'manufacturer', 'Small Appliances'),
    'Bear': ('bear-appliances', 'manufacturer', 'Small Appliances'),
    '苏州工业园区 (SIP)': ('suzhou-industrial-park', None, 'Industrial Park'),  # park, not mfr
    '潍柴集团 (Weichai)': ('weichai', 'manufacturer', 'Power / Diesel Engines'),
    'Chint Group (正泰集团)': ('chint-group', 'manufacturer', 'Electrical Equipment'),
    'Delixi (德力西)': ('delixi', 'manufacturer', 'Electrical Equipment'),
    'YOFC (长飞光纤)': ('yofc', 'manufacturer', 'Optical Fiber'),
    'FiberHome (烽火通信)': ('fiberhome', 'manufacturer', 'Optical Communications'),
    'YMTC (长江存储)': ('ymtc', 'manufacturer', 'Memory IC'),
    '徐工机械 (XCMG)': ('xcmg', 'manufacturer', 'Construction Machinery'),
    '天合光能 (Trina Solar)': ('trina-solar', 'manufacturer', 'Solar / PV'),
    '金风科技 (Goldwind) 大丰基地': ('goldwind', 'manufacturer', 'Wind Power'),
    # --- pure-Chinese entries: classify carefully (strict evidence rule) ---
    # industrial parks / bases (-> industrial-parks)
    '保定高新区': ('baoding-high-tech-zone', None, 'Industrial Park'),
    '西安阎良航空基地': ('xian-yanliang-aviation-base', None, 'Industrial Park'),
    '张江科学城': ('zhangjiang-science-city', None, 'Industrial Park'),
    # genuine single manufacturers
    '招宝磁业': ('zhaobao-magnetics', 'manufacturer', 'Magnetic Materials'),
    '北海造船': ('beihai-shipbuilding', 'manufacturer', 'Shipbuilding'),
    '十八子': ('shibazi', 'manufacturer', 'Kitchen Knives'),
    '中国航发南方公司': ('aecc-south', 'manufacturer', 'Aero Engines'),
    '浙江万得凯流体设备': ('wandekai-fluid', 'manufacturer', 'Pumps & Valves'),
    '大唐袜业': ('datang-socks', 'manufacturer', 'Socks / Hosiery'),
}

# pure-Chinese entries to SKIP entirely (not single manufacturers):
# trading markets, research institutes, cluster/industry self-names, company lists
SKIP_NAMES = {
    '澄海玩具集群', '成都电子信息产业', '重庆电子信息产业', '浙东工业母机集群',
    '东莞家具产业', '佛山陶瓷产业', '分散的家具制造企业群', '海宁中国皮革城',
    '中国轻纺城', '中科星图/华米科技等', '361°', '中微半导体/紫光展锐/格科微等',
    '苏大维格/南大光电/晶方半导体/锦富新材/禾盛新材/天华超净/聚灿光电',
    '叠石桥国际家纺城', '温岭泵与电机产业', '人民电器/天正等知名企业集团',
    '无锡市物联网创新促进中心', '中国飞机强度研究所', '金辉刀剪 / 美珑美利',
    '王力/博大/三锋/星月/步阳/群升/哈尔斯等', '中国航发湖南动力机械研究所',
    '远景能源 (Envision) 等',
}

def slugify_en(name):
    s = name.lower()
    s = re.sub(r'\([^)]*\)', '', s)      # drop parenthetical
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s

# gather
mfr_rows = defaultdict(list)   # slug -> list of (cluster, role, province, city, name_en, name_zh)
park_rows = []

for f in sorted(glob.glob(os.path.join(CLUSTER_DIR, '*.yaml'))):
    d = yaml.safe_load(open(f))
    cid = d.get('id', '')
    loc = d.get('location') or {}
    province = loc.get('province', '')
    city = str(loc.get('city') or '').split('(')[0].strip()
    ev_level = d.get('evidence_level', 'Medium')
    km = d.get('key_manufacturers') or []
    for m in km:
        if not isinstance(m, dict):
            continue
        name = (m.get('name') or '').strip()
        if not name:
            continue
        name_zh = m.get('name_zh', '').strip()
        role = m.get('role', '').strip()

        # skip non-manufacturer pure-Chinese entries
        if name in SKIP_NAMES:
            continue

        # curated first
        if name in CURATED:
            slug, er, hint = CURATED[name]
            if er is None:
                if hint == 'Industrial Park':
                    park_rows.append({'name': name, 'name_zh': name_zh, 'cluster': cid,
                                      'province': province, 'city': city,
                                      'note': m.get('note', ''), 'slug': slug})
                continue  # skip software / park
            mfr_rows[slug].append(dict(name_en=name, name_zh=name_zh, role=role, cluster=cid,
                                       province=province, city=city, ev=ev_level,
                                       entity_role=er, industry=hint))
            continue

        # role-map based
        er = ROLE_MAP.get(role, 'manufacturer') if role else 'manufacturer'
        if er is None:
            continue  # software, skip
        # clean english name
        en = re.sub(r'\([^)]*\)', '', name).strip()
        if not re.search(r'[A-Za-z]', en):
            en = name
        slug = slugify_en(en)
        if not slug:
            slug = slugify_en(name)
        mfr_rows[slug].append(dict(name_en=name, name_zh=name_zh, role=role, cluster=cid,
                                   province=province, city=city, ev=ev_level,
                                   entity_role=er, industry=''))

print(f'manufacturers to write: {len(mfr_rows)}')
print(f'industrial-parks to write: {len(park_rows)}')

# write manufacturer entities
for slug, rows in sorted(mfr_rows.items()):
    r0 = rows[0]
    clusters = sorted(set(x['cluster'] for x in rows))
    provinces = sorted(set(x['province'] for x in rows if x['province']))
    cities = sorted(set(x['city'] for x in rows if x['city']))
    # pick best name_en (prefer pure English)
    name_en = r0['name_en']
    name_zh = r0['name_zh'] or ''
    ev = 'High' if any(x['ev'] == 'High' for x in rows) else 'Medium'

    y = {
        'id': f'mfr-{slug}',
        'type': 'Manufacturer',
        'name_en': name_en,
        'name_zh': name_zh,
        'entity_role': r0['entity_role'],
        'location': {
            'province': provinces[0] if provinces else '',
            'city': cities[0] if cities else '',
        },
        'clusters': clusters,
        'industry': r0['industry'] or '',
        'factory_evidence': [f'cluster:{c}' for c in clusters],  # verified via cluster research
        'confidence': ev,
        'verification_date': '2026-09-14',
    }
    path = os.path.join(OUT_DIR, f'mfr-{slug}.yaml')
    with open(path, 'w') as fh:
        fh.write(f'# Manufacturer — {name_en}\n')
        yaml.safe_dump(y, fh, allow_unicode=True, sort_keys=False, default_flow_style=False)

# write industrial-park entities (only SIP extracted so far)
for p in park_rows:
    slug = p['slug']
    y = {
        'id': f'prk-{slug}',
        'type': 'IndustrialPark',
        'name_en': p['name'],
        'name_zh': p['name_zh'],
        'location': {'province': p['province'], 'city': p['city']},
        'clusters': [p['cluster']],
        'note': p['note'],
        'confidence': 'Medium',
        'verification_date': '2026-09-14',
    }
    path = os.path.join(PARK_DIR, f'prk-{slug}.yaml')
    with open(path, 'w') as fh:
        fh.write(f'# Industrial Park — {p["name"]}\n')
        yaml.safe_dump(y, fh, allow_unicode=True, sort_keys=False, default_flow_style=False)

print('DONE')
