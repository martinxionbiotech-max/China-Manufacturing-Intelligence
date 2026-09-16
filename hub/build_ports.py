#!/usr/bin/env python3
"""Build Port entities from Tavily search results (research/raw/port-*.json).
Creates data/entities/ports/prt-*.yaml and backfills city.ports field.
All facts transcribed from authoritative sources (no invented numbers).
"""
import os, yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTS_DIR = os.path.join(ROOT, 'data', 'entities', 'ports')
CITIES_DIR = os.path.join(ROOT, 'data', 'entities', 'cities')
os.makedirs(PORTS_DIR, exist_ok=True)

# (id, name_en, name_zh, province, city_name, serves_clusters, facts[(fact, source)])
PORTS = [
    ('prt-shanghai', 'Shanghai Port', '上海港', 'Shanghai', 'Shanghai',
     ['cls-shanghai-ic', 'cls-shanghai-nev', 'cls-zhangjiang-biomed'],
     [("2024年上海港集装箱吞吐量首次突破5000万标准箱，创全球港口集装箱运输史上最高纪录，连续15年蝉联全球第一。", "上海市国资委/国务院国资委(2025-01)"),
      ("上海港拥有近350条国际航线，覆盖200多个国家和地区的700多个港口，港口连通度连续13年全球第一。", "上海市国资委(2025-01)"),
      ("2024年上海港货物吞吐量8.61亿吨，居全国第3。", "2024全国超亿吨港口货物吞吐量排名(2025)")]),
    ('prt-ningbo-zhoushan', 'Ningbo-Zhoushan Port', '宁波舟山港', 'Zhejiang', 'Ningbo',
     ['cls-ningbo-green-petrochemical', 'cls-ningbo-magnetic-materials', 'cls-cixi-small-appliances', 'cls-hangzhou-bay-textile'],
     [("2024年宁波舟山港完成货物吞吐量13.77亿吨(同比+4%)，连续16年位居全球第一。", "新华网(2025-01)"),
      ("2024年宁波舟山港完成集装箱吞吐量3930万标准箱(同比+11%)，增幅创近7年新高，稳居世界第三。", "新华网(2025-01)")]),
    ('prt-shenzhen', 'Shenzhen Port', '深圳港', 'Guangdong', 'Shenzhen',
     ['cls-shenzhen-electronics', 'cls-sg-medical-devices'],
     [("2024年深圳港集装箱吞吐量继2022年后再次突破3000万标箱，全港保持高位运行。", "深圳政府在线/深圳特区报(2024-11)"),
      ("2024年深圳港集团所属深圳港区集装箱吞吐量1736.5万标箱(同比+7%)创新高；盐田港区全年集装箱吞吐量首次突破1500万标箱。", "深圳市国资委/国务院国资委(2025-01)")]),
    ('prt-guangzhou', 'Guangzhou Port', '广州港', 'Guangdong', 'Guangzhou',
     ['cls-sg-medical-devices', 'cls-foshan-ceramics', 'cls-foshan-furniture', 'cls-fd-pan-home', 'cls-shunde-home-appliances'],
     [("2024年广州港完成集装箱吞吐量2518.2万标箱(同比+5.3%)，货物吞吐量5.68亿吨(同比+2.8%)，港口能级实现历史新跨越。", "广州港股份公告/证券时报(2025-01)"),
      ("广州港货物吞吐量由2020年6.36亿吨增长至2023年6.75亿吨，世界排名第5。", "广州市人民政府(2025)")]),
    ('prt-qingdao', 'Qingdao Port', '青岛港', 'Shandong', 'Qingdao',
     ['cls-qingdao-appliances', 'cls-qingdao-shipbuilding'],
     [("2024年青岛港完成货物吞吐量7.1亿吨、集装箱吞吐量3087万标准箱，分别位居全球第四、第五。", "山东港口青岛港(2025)"),
      ("青岛港累计开辟230余条集装箱航线，航线总数及密度稳居中国北方港口第一位。", "青岛港ESG报告(2025)")]),
    ('prt-tianjin', 'Tianjin Port', '天津港', 'Tianjin', 'Tianjin',
     [],
     [("2024年天津港集团完成货物吞吐量4.93亿吨(同比+3%)、集装箱吞吐量2328万标准箱(同比+5%)，双双创下历史最好水平。", "天津港集团/人民网天津(2025-01)")]),
    ('prt-suzhou', 'Suzhou Port', '苏州港', 'Jiangsu', 'Suzhou',
     ['cls-suzhou-biomed', 'cls-suzhou-nano', 'cls-swt-textile'],
     [("2024年苏州港完成集装箱吞吐量1002.6万标箱(同比+4.6%)，成为全国首个年吞吐量突破千万标箱的内河港，居全国第8、全球第20。", "江苏省国资委/荔枝新闻(2025-02)"),
      ("苏州港由太仓、张家港、常熟3个沿江港区和内河港区组成，现有泊位307个(万吨级以上142个)，2024年货物吞吐量6.05亿吨居全国第8。", "国务院国资委/光明日报(2024-12)")]),
    ('prt-xiamen', 'Xiamen Port', '厦门港', 'Fujian', 'Xiamen',
     [],
     [("2024年厦门港完成货物吞吐量2.11亿吨、集装箱吞吐量1225.47万标箱；2025年集装箱吞吐量1250.77万标箱(同比+2.06%)。", "厦门港务发展年报/人民网福建(2026)")]),
    ('prt-yantai', 'Yantai Port', '烟台港', 'Shandong', 'Yantai',
     ['cls-qingdao-shipbuilding'],
     [("2024年烟台港完成货物吞吐量5.02亿吨(同比+3.6%)，居全国第9。", "2024全国超亿吨港口货物吞吐量排名(2025)")]),
    ('prt-quanzhou', 'Quanzhou Port', '泉州港', 'Fujian', 'Quanzhou',
     ['cls-quanzhou-sports', 'cls-jinjiang-footwear'],
     [("2024年泉州港完成货物吞吐量约1.17亿吨(11686万吨)。", "2024全国超亿吨港口货物吞吐量排名(2025)")]),
    ('prt-nantong', 'Nantong Port', '南通港', 'Jiangsu', 'Nantong',
     ['cls-swt-textile'],
     [("2024年南通港完成集装箱吞吐量271.9万标箱(同比+33.1%)，增速位居全国主要港口前列。", "南通市交通局/人民网江苏(2025-01)"),
      ("2024年南通港货物吞吐量约3.03亿吨(30262万吨)。", "2024全国超亿吨港口货物吞吐量排名(2025)")]),
    ('prt-weihai', 'Weihai Port', '威海港', 'Shandong', 'Weihai',
     ['cls-qingdao-shipbuilding'],
     [("2024年1-11月威海港完成货物吞吐量4603.87万吨，集装箱吞吐量141.26万标箱(同比+4.75%)。", "威海市交通运输局(2024-12)")]),
]

# city_ports: city entity id -> list of port ids
CITY_PORTS = {
    'cty-shanghai': ['prt-shanghai'],
    'cty-ningbo': ['prt-ningbo-zhoushan'],
    'cty-shenzhen': ['prt-shenzhen'],
    'cty-guangzhou': ['prt-guangzhou'],
    'cty-qingdao': ['prt-qingdao'],
    'cty-suzhou': ['prt-suzhou'],
    'cty-yantai': ['prt-yantai'],
    'cty-quanzhou': ['prt-quanzhou'],
    'cty-nantong': ['prt-nantong'],
    'cty-weihai': ['prt-weihai'],
}

def dump_yaml(d, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(d, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=200)

n = 0
for pid, name_en, name_zh, province, city, serves, facts in PORTS:
    d = {
        'id': pid,
        'type': 'Port',
        'name_en': name_en,
        'name_zh': name_zh,
        'city': city,
        'province': province,
        'serves': serves,
        'evidence_level': 'High',
        'confidence': 'High',
        'last_verified': '2026-09-15',
        'verified_facts': [{'fact': f, 'source': s} for f, s in facts],
    }
    dump_yaml(d, os.path.join(PORTS_DIR, pid + '.yaml'))
    n += 1
print(f'港口实体生成: {n} 个')

# backfill city ports
m = 0
for cid, pids in CITY_PORTS.items():
    path = os.path.join(CITIES_DIR, cid + '.yaml')
    if not os.path.exists(path):
        print(f'  !! 缺失城市 {path}')
        continue
    d = yaml.safe_load(open(path, encoding='utf-8'))
    d['ports'] = pids
    dump_yaml(d, path)
    m += 1
print(f'城市 ports 字段回填: {m} 个')
