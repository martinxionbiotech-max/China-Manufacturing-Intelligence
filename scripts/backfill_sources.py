#!/usr/bin/env python3
"""P0: Backfill URLs from research/raw/*.json into research/*.md src registries (and content/ Sources lists).

Matching: normalized title equality/containment + publisher->domain hints.
Never fabricates: only assigns a URL when match confidence is high.
"""
import glob, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'research', 'raw')
RESEARCH = os.path.join(ROOT, 'research')
CONTENT = os.path.join(ROOT, 'content')

# Publisher name -> likely domain fragment(s)
PUB_DOMAINS = {
    '证券时报': ['stcn.com'],
    '四川在线': ['scol.com.cn'],
    '中国日报': ['chinadaily.com.cn', 'cn.chinadaily.com.cn'],
    '红网': ['rednet.cn'],
    '湖南省政府': ['hunan.gov.cn'],
    '湖南政研网': ['hnzy.gov.cn'],
    '东莞市政府': ['dg.gov.cn'],
    '东莞投资促进局': ['fipc.dg.gov.cn'],
    '广州日报': ['dayoo.com'],
    'scmp': ['scmp.com'],
    'hktdc': ['hktdc.com'],
    '网易': ['163.com'],
    '南都': ['163.com', 'oeeee.com'],
    '前瞻': ['qianzhan.com'],
    '界面新闻': ['jiemian.com'],
    '百度百科': ['baike.baidu.com'],
    '陶瓷信息网': ['taocixinxi.com', 'ceramicschina.com'],
    '南方+': ['nfnews.com', 'southcn.com'],
    '佛山日报': ['fsnews.net'],
    '新华网': ['xinhuanet.com', 'news.cn'],
    '人民网': ['people.com.cn'],
    '央视': ['cctv.com', 'news.cctv.com'],
    '福建日报': ['fjrb.fjsen.com', 'fjsen.com'],
    '中新网': ['chinanews.com.cn'],
    '吉林省人民政府': ['jl.gov.cn'],
    '长春日报': ['caida.gov.cn', 'ccrb.1news.cc'],
    '上海市政府': ['shanghai.gov.cn'],
    '上海市经信委': ['sheitc.sh.gov.cn'],
    '苏州日报': ['subaonet.com'],
    '无锡市政府': ['wuxi.gov.cn'],
    '武汉市政府': ['wuhan.gov.cn'],
    '深圳市政府': ['sz.gov.cn'],
    '青岛市政府': ['qingdao.gov.cn'],
    '宁波市政府': ['ningbo.gov.cn'],
    '温州市政府': ['wenzhou.gov.cn'],
    '佛山市政府': ['foshan.gov.cn'],
    '淄博市政府': ['zibo.gov.cn'],
    '潍坊市政府': ['weifang.gov.cn'],
    '烟台市政府': ['yantai.gov.cn'],
    '徐州政府': ['xz.gov.cn'],
    '盐城市政府': ['yancheng.gov.cn'],
    '株洲市政府': ['zhuzhou.gov.cn'],
    '常州市政府': ['changzhou.gov.cn'],
    '保定市政府': ['baoding.gov.cn'],
    '包头市政府': ['baotou.gov.cn'],
    '赣州市政府': ['ganzhou.gov.cn'],
    '洛阳市政府': ['luoyang.gov.cn'],
    '台州市政府': ['zjtz.gov.cn'],
    '海宁市政府': ['haining.gov.cn'],
    '金华市政府': ['jinhua.gov.cn'],
    '嘉兴市政府': ['jiaxing.gov.cn'],
    '绍兴市政府': ['sx.gov.cn'],
    '中山市政府': ['zs.gov.cn'],
    '阳江市政府': ['yangjiang.gov.cn'],
    '芜湖市政府': ['wuhu.gov.cn'],
    '合肥市政府': ['hefei.gov.cn'],
    '西安市政府': ['xa.gov.cn'],
    '沈阳市政府': ['shenyang.gov.cn'],
    '哈尔滨市政府': ['harbin.gov.cn'],
    '第一财经': ['yicai.com'],
    '财新': ['caixin.com'],
    '澎湃': ['thepaper.cn'],
    '21世纪经济报道': ['21jingji.com'],
    '经济观察报': ['eeo.com.cn'],
    '每日经济新闻': ['nbd.com.cn'],
    '环球时报': ['globaltimes.cn', 'huanqiu.com'],
    '参考消息': ['cankaoxiaoxi.com'],
    '科技日报': ['stdaily.com'],
    '光明日报': ['gmw.cn'],
    '工人日报': ['workercn.cn'],
    '中国工业报': ['cinn.cn'],
    '机经网': ['mei.net.cn'],
    '中国机床工具工业协会': ['cmtba.cn', 'cmtba.org.cn'],
    '中国工程机械工业协会': ['cncma.org'],
    '农机通': ['nongjitong.com'],
    '农机360': ['nongji360.com'],
    '慧聪': ['hc360.com'],
    '知乎': ['zhihu.com'],
    'wiki': ['wikipedia.org'],
    'wikipedia': ['wikipedia.org'],
    'catl': ['catl.com'],
    'bytech': ['bytech.com.cn'],
    'byd': ['byd.com'],
    '特斯拉': ['tesla.cn', 'tesla.com'],
    '华为': ['huawei.com'],
    '小米': ['mi.com'],
    'oppo': ['oppo.com'],
    'vivo': ['vivo.com'],
    'tcl': ['tcl.com'],
    '海尔': ['haier.com'],
    '美的': ['midea.com'],
    '格力': ['gree.com'],
    '三一重工': ['sany.com.cn', 'sanyglobal.com'],
    '中联重科': ['zoomlion.com'],
    '徐工': ['xcmg.com'],
    '柳工': ['liugong.com'],
    '中国稀土': ['cre-ol.com'],
    '北方稀土': ['reht.cn'],
    '江西省工信厅': ['jxciit.gov.cn'],
    '工信部': ['miit.gov.cn'],
    '国家统计局': ['stats.gov.cn'],
    '中国汽车工业协会': ['caam.org.cn'],
    '中国光伏行业协会': ['cpia.org.cn'],
    '中国电子元件行业协会': ['ceca.org.cn'],
    '中国电池工业协会': ['chinabattery.org'],
    '高工锂电': ['gg-lb.com'],
    '真锂研究': ['evtank.com'],
    '中商产业研究院': ['askci.com'],
    '艾瑞': ['iresearch.com.cn'],
    '赛迪': ['ccidnet.com'],
    '智研咨询': ['chbaogao.com', 'zhiyan.info'],
    '观研报告网': ['chinabaogao.com'],
    '中研网': ['chinairn.com'],
    '同花顺': ['10jqka.com.cn'],
    '东方财富': ['eastmoney.com'],
    '雪球': ['xueqiu.com'],
    '新浪财经': ['finance.sina.com.cn', 'sina.com.cn'],
    '腾讯': ['qq.com'],
    '搜狐': ['sohu.com'],
    '凤凰': ['ifeng.com'],
    '观察者网': ['guancha.cn'],
    '钛媒体': ['tmtpost.com'],
    '36氪': ['36kr.com'],
    '虎嗅': ['huxiu.com'],
    '亿欧': ['iyiou.com'],
    '艾媒': ['iimedia.cn'],
    '生意社': ['100ppi.com'],
    '隆众资讯': ['oilchem.net'],
    '我的钢铁': ['mysteel.com'],
    '兰格钢铁': ['lgmi.com'],
    '中华商务网': ['chinaccm.com'],
    '世纪新能源网': ['ne21.com'],
    '北极星': ['bjx.com.cn'],
    '光伏們': ['pv-men.com'],
    '储能网': ['escn.com.cn'],
    '机床商务网': ['jc35.com'],
    '包装印刷产业网': ['pack.cn'],
    '中华门窗网': ['chinaleather.org'],
    '泛家居': ['fanjiaju.com'],
    '灯饰在线': ['lightonline.com.cn'],
    '古镇灯饰报': ['guzhends.com'],
    '电子发烧友': ['elecfans.com'],
    '半导体行业观察': ['semiinsights.com'],
    '芯思想': ['chipinsights.com'],
    '集微网': ['jiwei.net'],
    '爱集微': ['laoyaoba.com'],
    '满天芯': ['icnet.com.cn'],
    '中关村在线': ['zol.com.cn'],
    '汽车之家': ['autohome.com.cn'],
    '盖世汽车': ['gasgoo.com'],
    '汽车商业评论': ['autoreview.cn', 'cnev.com'],
    '中国交通报': ['zgjtb.com'],
    '港口圈': ['portinfo.net'],
    '航运界': ['ship.sh'],
    '国际船舶网': ['eworldship.com'],
    '中国船舶报': ['chinashipnews.com.cn'],
    '化工仪器网': ['chem17.com'],
    '氟化工': ['flu.com.cn'],
    '石化联合会': ['cpcia.org.cn'],
    '中国化工报': ['ccin.com.cn'],
    '农化网': ['agrochem.com.cn'],
    '中国纺织报': ['ctn1986.cn'],
    '纺织服装周刊': ['taweekly.com'],
    '全球纺织网': ['tnc.com.cn'],
    '中国纺织网': ['texnet.com.cn'],
    '纺织导报': ['texleader.com.cn'],
    '中国服装网': ['efu.com.cn'],
    '鞋业头条': ['xieyesc.com'],
    '环球鞋网': ['shoes.net.cn'],
    '中国皮革网': ['chinaleather.org'],
    '皮革天地': ['pgti.cn'],
    '中国玩具和婴童用品协会': ['tjpa-china.org'],
    '中外玩具网': ['ctoy.com.cn'],
    '玩具圈': ['toycircle.cn'],
    '中国文体用品协会': ['csa.org.cn'],
    '文体用品与科技': ['wtkjzz.com'],
}

def norm(s):
    if not s: return ''
    s = unicodedata.normalize('NFKC', str(s))
    s = s.lower()
    # keep CJK + alnum
    return re.sub(r'[^0-9a-z\u4e00-\u9fff]', '', s)

def load_raw():
    """Return list of dicts {url, title, content, file, domain}."""
    out = []
    for f in sorted(glob.glob(os.path.join(RAW, '*.json'))):
        raw = open(f, encoding='utf-8', errors='replace').read()
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            # salvage: parse first JSON object
            dec = json.JSONDecoder()
            try:
                d, _ = dec.raw_decode(raw)
            except Exception:
                print('  [skip unparseable]', os.path.basename(f), file=sys.stderr)
                continue
        for r in d.get('results', []) or []:
            url = r.get('url') or ''
            if not url: continue
            dom = re.sub(r'^https?://', '', url).split('/')[0].lower()
            out.append({
                'url': url, 'title': r.get('title') or '', 'content': r.get('content') or '',
                'file': os.path.basename(f), 'domain': dom,
            })
    return out

def extract_domain_hints(pub):
    """From publisher cell like '东莞投资促进局 fipc.dg.gov.cn' or 'CATL (catl.com PDF)'."""
    hints = set()
    for m in re.finditer(r'([a-z0-9][a-z0-9\-]*\.)+[a-z]{2,}(?:\.[a-z]{2,})?', pub, re.I):
        d = m.group(0).lower().strip('.').strip()
        if len(d) > 4 and '.' in d:
            hints.add(d)
    return hints

def pub_hints(pub):
    pub_l = (pub or '').lower()
    hints = extract_domain_hints(pub)
    for name, doms in PUB_DOMAINS.items():
        if name.lower() in pub_l:
            hints.update(doms)
    return hints

def match_score(reg_title, reg_pub, raw_item):
    """Return score 0..1 or 0 for no plausible match."""
    rt, rp = norm(reg_title), norm(reg_pub)
    tt, tp = norm(raw_item['title']), norm(raw_item['content'])[:200]
    dom = raw_item['domain']
    score = 0.0
    # 1) title match
    if rt and tt:
        if rt == tt:
            score = 1.0
        elif len(rt) >= 8 and rt in tt:
            score = 0.92
        elif len(tt) >= 8 and tt in rt:
            score = 0.92
        elif len(rt) >= 8 and len(tt) >= 8:
            # char bigram jaccard
            def big(s):
                return set(s[i:i+2] for i in range(len(s)-1))
            b1, b2 = big(rt), big(tt)
            j = len(b1 & b2) / max(1, len(b1 | b2))
            if j >= 0.72:
                score = 0.55 + 0.4 * j
            elif j >= 0.55 and (rt in tp or tt in tp):
                score = 0.5 + 0.2 * j
    # 2) domain hints
    hints = pub_hints(reg_pub)
    if hints:
        for h in hints:
            if h in dom or dom.endswith('.' + h):
                score = max(score, 0.75)
                break
        if score >= 0.55:
            score = min(1.0, score + 0.1)
    # 3) title fragments in content
    if score < 0.5 and rt and len(rt) >= 8 and rt[:8] in tp:
        score = max(score, 0.35)
    return score

def parse_registry(txt):
    rows = []
    m = re.search(r'## Sources \(evidence registry\)(.*?)(?:\n## |\Z)', txt, re.S)
    if not m:
        m = re.search(r'## Sources\s*\n(.*?)(?:\n## |\Z)', txt, re.S)
    if not m:
        return rows
    sec = m.group(1)
    for line in sec.split('\n'):
        line = line.rstrip()
        if not line.strip().startswith('|'):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 5: continue
        if cells[0].lower().startswith('src id') or re.match(r'^[-:\s]+$', cells[0]): continue
        rows.append({'sid': cells[0], 'title': cells[1], 'publisher': cells[2],
                     'level': cells[3], 'date': cells[4]})
    return rows

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'match'
    raw_items = load_raw()
    print(f'raw results: {len(raw_items)}')

    md_files = sorted(glob.glob(os.path.join(RESEARCH, '*.md')))
    total, matched, missing = 0, 0, []
    assignments = {}  # md_file -> {sid: url}
    for f in md_files:
        txt = open(f, encoding='utf-8').read()
        rows = parse_registry(txt)
        fname = os.path.basename(f)
        for r in rows:
            total += 1
            cands = []
            for it in raw_items:
                s = match_score(r['title'], r['publisher'], it)
                if s >= 0.55:
                    cands.append((s, it))
            if not cands:
                missing.append((fname, r['sid'], r['title'], r['publisher']))
                continue
            cands.sort(key=lambda x: -x[0])
            best_s, best = cands[0]
            if best_s >= 0.9:
                matched += 1
                assignments.setdefault(fname, {})[r['sid']] = best['url']
            else:
                missing.append((fname, r['sid'], r['title'], r['publisher']))
    print(f'registry rows: {total}, high-confidence matched: {matched}, unmatched: {len(missing)}')

    if mode == 'match':
        print('\n--- unmatched (first 40) ---')
        for x in missing[:40]:
            print(' | '.join(x[:3]))
        json.dump(assignments, open(os.path.join(ROOT, 'scripts', 'assignments.json'), 'w'),
                  ensure_ascii=False, indent=1)
        print('\nwrote scripts/assignments.json')
        return

    if mode == 'write':
        # write URLs into research md registry tables (add URL column)
        for f in md_files:
            fname = os.path.basename(f)
            if fname not in assignments: continue
            amap = assignments[fname]
            txt = open(f, encoding='utf-8').read()
            # rebuild the registry table block
            m = re.search(r'(\| src id \| Title \| Publisher \| Level \| Date \|\n\|[-\s|]+\|\n)(.*?)(?=\n## |\Z)', txt, re.S)
            if not m: continue
            head, sep, body = m.group(1), m.group(2), m.group(3)
            new_head = '| src id | Title | Publisher | Level | Date | URL |\n|--|--|--|--|--|--|\n'
            out_lines = []
            for line in body.split('\n'):
                if not line.strip().startswith('|'): continue
                cells = [c.strip() for c in line.strip().strip('|').split('|')]
                if len(cells) < 5: continue
                url = amap.get(cells[0], '')
                if not url:
                    # leave empty
                    out_lines.append(line.rstrip() + ' | |')
                else:
                    out_lines.append(line.rstrip() + ' ' + url + ' |')
            new_block = new_head + '\n'.join(out_lines) + '\n'
            txt = txt[:m.start()] + new_block + txt[m.end():]
            open(f, 'w', encoding='utf-8').write(txt)
        print('registry write done for', len(assignments), 'files')

if __name__ == '__main__':
    main()
