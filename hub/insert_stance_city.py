#!/usr/bin/env python3
"""Insert '## The Author's Take' stance blocks into city pages."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content', 'cities')

STANCES = {
'cty-baoding': """*In my view, Baoding is positioning itself as the equipment backbone of China's renewables buildout, not a diversified manufacturing hub — its "wind-solar-hydrogen-storage-transmission" thread is a single coherent bet.*

That makes it the correct anchor for utility-scale transmission and distribution equipment, especially renewables-linked projects. But do not expect it to be a generalist electronics or consumer-goods play — that is not what this city is.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-baotou': """*In my view, Baotou owns the ore-and-oxide layer of the rare-earth chain — it is the price-setting node for light rare earth globally, not a finished-magnet hub.*

The practical question is which layer you buy: ore and oxides route to Baotou, finished magnets to Ningbo (or Baotou's growing magnet base). Rare earth is a quota-governed market, so layer and licensing matter more than price.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-changchun': """*In my view, Changchun is building a self-contained NEV ecosystem — FAW brand plus near-site suppliers plus a captive battery JV — reinforced by the densest auto R&D base in the country.*

That signals domestic-brand cost structures and a growing near-site parts ecosystem. It is not the export-grade volume pole — that is Shanghai — so match your compliance and export needs to the city accordingly.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-changsha': """*In my view, Changsha's five-firm structure makes it a competitive cluster — the co-location of rivals drives both variety and export aggressiveness.*

That makes it the correct floor for multi-vendor negotiation leverage and niche spec coverage. It is not the single-account scale play — that is Xuzhou — so pick the strategy before you pick the city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-changzhou': """*In my view, Changzhou's RMB 120B "new carbon materials" figure is broader than carbon fiber alone — it spans graphite and advanced-carbon materials — and the carbon-fiber-specific story is a chokepoint-breaking one.*

For aerospace-grade carbon fiber and composites, Changzhou is the correct anchor, but it carries export-control sensitivity around aircraft end-use. Verify end-use, and do not read the headline number as carbon fiber alone.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-chengdu': """*In my view, the Chengdu-Chongqing cluster is a policy-and-geography cluster — its "trillion-yuan" scale is partly a product of the twin-city economic-zone policy, not just organic industrial depth.*

For buyers, it is the right anchor for cost-sensitive, inland-scale electronics assembly and ICT manufacturing. It is not the place for design, component, or cutting-edge work — that stays in Shenzhen and the Deltas.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-chongqing': """*In my view, the Chengdu-Chongqing cluster is a policy-scaled twin-city cluster — its trillion-yuan scale comes from combining two megacities under one economic-zone policy.*

For buyers, Chongqing is the right anchor for inland, cost-optimized electronics assembly with a rail export route to Europe and Central Asia, plus NEV powertrain work. Do not expect leading-edge components here.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-dongguan': """*In my view, Dongguan is a dual-industry city — smartphones and furniture — a rare combination that reflects the Pearl River Delta's "one city, one chain" pattern.*

For finished smartphone and terminal assembly (the Huawei, OPPO, vivo tier), Dongguan is the anchor. For components, go upstream to Shenzhen; for furniture, it is the Foshan-Dongguan pair. Each half of the city routes differently.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-foshan': """*In my view, Foshan is a category-agglomeration city — its edge is that a single buyer can source ceramics, furniture, and appliances in one geography, the "pan-home" frame.*

That makes it the strongest single-city floor for home-goods multi-category sourcing. Its weakness is that two of its three clusters (ceramics, furniture) are mature and consolidating, so anchor on branded suppliers.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-ganzhou': """*In my view, Ganzhou owns the scarcest layer of the rare-earth chain — heavy ionic rare earth is geologically rarer and more concentrated than light rare earth, and its dysprosium and terbium are irreplaceable for heat-resistant magnets.*

For high-temperature magnets (EV motors, wind turbines, aerospace), you need Ganzhou's heavy rare earth. Standard NdFeB routes to Baotou instead. Element-matching is the whole game.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-guangzhou': """*In my view, the Shenzhen-Guangzhou pairing mirrors Zhangjiang-Suzhou in biopharma — a discovery-and-scale split rather than a rivalry.*

For hardware devices (monitors, ultrasound, IVD instruments), Shenzhen is the anchor, with Guangzhou as the clinical and research complement. Regulatory load — NMPA plus CE/FDA — is the real cost driver to price in.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-haining': """*In my view, Haining's leather industry is a seasonal fashion supply chain — its strength is finished autumn-winter garments, where it holds dominant influence, not commodity hides.*

For finished, fashion-tier leather and fur garments, Haining is the correct anchor, sourced in season (aligned to the CHIC spring and autumn-winter cycle). Its rising PV-and-semiconductor track is a separate, newer bet.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-hangzhou': """*In my view, Hangzhou is a dual-economy city — a knowledge-economy tech cluster coexisting with a traditional textile-cluster membership — and the two halves route differently.*

For video-surveillance hardware and AIoT platforms (Hikvision and Dahua, a two-vendor category), Hangzhou is the anchor. For textiles, use Hangzhou as one node in the broader Hangzhou Bay belt, not the whole chain.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-hefei': """*In my view, Hefei's voice industry is structurally sticky — anchored by a national champion and a research university, not by labor-cost arbitrage — but that also concentrates the category.*

For software and algorithm licensing (iFlytek), Hefei is the anchor; for hardware integration, Shenzhen. "AI" is too broad a sourcing category — split the software from the hardware and the routing becomes obvious.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-jiaxing': """*In my view, Jiaxing illustrates how the Hangzhou Bay cluster is a four-city shared designation — the national cluster boundary is larger than any single city's role.*

So Jiaxing is best used as one node in a Hangzhou Bay sourcing strategy: source fabric in Shaoxing, brand and garment in Hangzhou, and use Jiaxing and Ningbo as supporting nodes. Do not treat it as a standalone textile anchor.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-jinhua': """*In my view, Jinhua is a market-platform plus manufacturing-cluster pair — Yiwu is the discovery and distribution layer, Yongkang the hardware manufacturing layer.*

So it is best used as a combined sourcing surface: discover categories and order small-lot mixed containers in Yiwu, then trace hardware and power tools back to Yongkang for direct factory terms. The two halves work together.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-luoyang': """*In my view, agricultural machinery is a single-champion industry — one anchor firm, one city — and that concentration means a deep, stable supply chain but less competitive tension.*

For complete tractors and combine harvesters (YTO and its 300-firm chain), Luoyang is the correct anchor. If the need is engines or powertrain rather than complete machines, route to Weifang (Weichai) instead.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-nantong': """*In my view, Nantong is a market-plus-factory home-textile cluster — the Die-shi-qiao market is the discovery layer, with thousands of bedding makers as the factory layer behind it.*

For bedding and home textiles, Nantong is the correct anchor, with shipbuilding and marine engineering as a major secondary track. The market liquidity, not any single factory, is the real asset here.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-ningbo': """*In my view, Ningbo's defining trait is vertical complementarity — it takes others' raw materials (rare earth from Baotou and Ganzhou) and adds the high-value magnet layer.*

So Ningbo is the correct anchor for finished NdFeB magnets (downstream of ore) and niche small appliances (Cixi). It is not the ore source — that is Baotou and Ganzhou — so know which layer you are buying.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-ningde': """*In my view, Ningde is a champion-anchored ecosystem — CATL plus 90-plus upstream and downstream firms in one city — and its dominant global share is a genuine concentration risk for buyers.*

Ningde is unavoidable for high-performance cells, but the concentration argues for dual-sourcing: anchor volume with CATL-tier cells while qualifying a credible second source. Do not put the whole supply chain in one city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-qingdao': """*In my view, Qingdao is a dual-anchor city — brand appliances and heavy marine assembly — two very different industrial logics in one port.*

For brand and OEM-scale white goods (Haier, Hisense) and total assembly of large vessels (Beihai), Qingdao is the anchor. For marine-engineering platforms, route to Yantai; for co-building fabrication, to Weihai.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-quanzhou': """*In my view, Quanzhou's edge is supply-chain density — a 50-km self-contained radius covering R&D to component matching, which lets Anta, Xtep, and 361° all compete from the same base.*

So it serves both commodity OEM (volume, price) and branded ODM (the Anta and Xtep tier) — but those are different supplier tiers. Match deliberately, and do not treat them as one market.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-shanghai': """*In my view, Shanghai is the highest-value-density manufacturing city in this dataset — three clusters, each national #1 in its category, all built on research rather than cost.*

For export-grade NEVs, domestic IC design and foundry, and biopharma licensing and innovation, Shanghai is the anchor. It is not the cost play — for cost-optimized assembly you go inland, not here.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-shantou': """*In my view, Chenghai is a speed-and-IP cluster — its edge is iteration velocity (1,000 new SKUs a day) plus an IP-licensing moat, not just cheap labor.*

For plastic toys, especially licensed and IP toys, Shantou is the correct anchor, where its patent and IP-license leadership matters. The 300,000-SKU breadth is a discovery asset, not a commodity signal.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-shaoxing': """*In my view, Shaoxing is a market-plus-factory textile city — Keqiao's market is the discovery layer, with 8,000-plus mills and roughly 40% of national dyeing capacity behind it.*

For raw and printed fabric plus dyeing, Shaoxing is the correct anchor, and Datang adds the sock monopoly (70% of China's socks). "Textile capital" here means the fabric layer, not garments or home textiles.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-shenyang': """*In my view, robotics is a technology-origin cluster, not a volume cluster — Shenyang's strength is a roughly 50-year CAS lineage and SIASUN's industrial base, not enterprise density.*

So the split is robot arms (Shenyang, SIASUN) versus system integration (Shanghai and Shenzhen). Evaluate whether a supplier is a traditional-arm maker or an embodied-intelligence integrator — they are different bets.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-shenzhen': """*In my view, Shenzhen is a market-grown, component-dense cluster — the polar opposite of the policy-scaled clusters and the single-champion clusters.*

For components, PCBs, design, and device hardware, Shenzhen is the correct anchor and the first stop for any electronics sourcing journey. For finished smart terminals, route to Dongguan; for inland assembly, Chengdu-Chongqing.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-suzhou': """*In my view, Suzhou is a scale-and-materials city — it monetizes others' discoveries (biopharma CDMO) and builds advanced materials (nano) at industrial scale.*

So Suzhou is the correct anchor for biopharma CDMO and scale-up, and advanced nano-materials. It is not the discovery or licensing node (that is Shanghai) or the ore source — it sits one step downstream and adds value.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-taizhou': """*In my view, Taizhou is a category-density city — its edge is breadth (machine tools plus pumps plus valves plus motors) in one geography, not a single champion.*

For mid-to-high-end CNC machine tools and pumps and valves, Taizhou is the correct anchor. Its "hidden champion" profile means you verify per specialist rather than relying on one brand name.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-weifang': """*In my view, Weifang is a champion-anchored powertrain city — Weichai plus 27 national single champions, coordinated by a "chain-master" policy system.*

For diesel engines and powertrain systems (Weichai), Weifang is the correct anchor. If the need is complete tractors or machines, route to Luoyang (YTO) instead — powertrain here, complete machines there.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-weihai': """*In my view, Weihai illustrates the role-split cluster — the national designation covers three cities with distinct functions, and Weihai is the supporting-fabrication node.*

So it is best used as the fabrication node in a coordinated Qingdao-Yantai-Weihai sourcing strategy, plus a printer-and-carbon-fiber secondary track. Do not treat it as a standalone shipbuilding anchor.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-wenzhou': """*In my view, Wenzhou is a self-grown cluster — it emerged from township enterprises and traders, not a state anchor — which explains its extreme category breadth and its wide certification spread.*

For low-voltage apparatus, Wenzhou (Yueqing) is the correct anchor, with the caveat that certification tiers vary widely across the long tail. Chint-tier suppliers are not the same as the tail — verify per factory.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-wuhan': """*In my view, Optics Valley is an institution-anchored cluster — its engine is the 1976 fiber pull plus a 42-university talent base, not low-cost labor.*

For fiber, optical components, and laser equipment, Wuhan is the correct anchor. Pair Wuhan (fiber and optics) with Shenzhen (display integration) for complete optoelectronic-system sourcing.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-wuxi': """*In my view, Wuxi is a technology-cluster plus belt-member city — a knowledge-economy IoT anchor coexisting with a traditional textile-belt membership, mirroring Hangzhou's split.*

For IoT sensors, networking, and industrial-internet solutions, Wuxi is the correct anchor, and increasingly for special-steel and aerospace materials. For home textiles, use it as a node in the SWT belt, not the whole chain.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-xian': """*In my view, Xi'an is a defense-and-national-strategy cluster — its value is strategic (large aircraft, the Y-20) rather than commercial, which is why it is the least buyer-facing of the aerospace cities.*

For buyers, Xi'an is relevant mainly for aerospace-adjacent supply — structures, materials, testing — rather than commodity procurement. Its downstream carbon-fiber demand is the one commercial thread to watch.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-xuzhou': """*In my view, Xuzhou is a champion-led city — one vertically-integrated group (XCMG) carrying a full machine lineage, from excavator to crane to pile.*

For single-account scale and full-lineage consistency (XCMG), Xuzhou is the correct anchor. For multi-vendor negotiation leverage and niche specs, route to Changsha instead — the two are different strategies.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-yancheng': """*In my view, Yancheng's clean-energy pairing — wind plus PV — is unusual, since most cities anchor one energy cluster; its offshore-wind test-farm infrastructure is the differentiator.*

For offshore-wind turbines and systems and PV modules, Yancheng is the correct anchor, and you can pair both from one geography for integrated clean-energy capex. The test-farm is a genuine proof-of-scale asset.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-yangjiang': """*In my view, Yangjiang is a category monopoly, not a brand monopoly — it dominates kitchen cutlery through enterprise density (2,000-plus makers), not a single champion.*

For kitchen cutlery, Yangjiang is the correct anchor, and its standard-setting makes it a safer starting point than Yongkang's power tools, where certification varies more. Verify per maker against your spec.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-yantai': """*In my view, Yantai is a dual-anchor city — marine engineering (CIMC Raffles) plus petrochemicals (Wanhua) — and its trillion-scale industrial base means marine engineering sits atop a broad foundation.*

For offshore and marine-engineering platforms, Yantai is the correct anchor, with Wanhua's petrochemical chain as a major secondary track. It is the middle, high-value node of the Qingdao-Yantai-Weihai cluster.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-zhongshan': """*In my view, Guzhen is the purest category-monopoly cluster in this dataset — a sub-50 km² town owning roughly half a global market through extreme spatial density.*

For commodity LED fixtures, Zhongshan and Guzhen are the correct floor. But the "roughly 50% global" figure is an industry estimate, not a government census, and the chip/driver layer is a separate, upstream oligopoly.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cty-zhuzhou': """*In my view, Zhuzhou is a state-champion plus institutional-depth city — its mechanism is CRRC plus standards leadership, not market density, and the 5-km supply radius is a structural strength.*

For complete rail vehicles, traction systems, and metro equipment, Zhuzhou is the correct anchor, and its 84 international standards make it the safest starting point for spec-heavy or export rail projects.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",
}

def insert_stance(path, stance):
    txt = open(path, encoding='utf-8').read()
    if '## The Author\'s Take' in txt:
        return False
    m = re.search(r'\n## Sources\b', txt)
    if not m:
        print(f'  !! 无 Sources 段: {os.path.basename(path)}')
        return False
    block = "\n## The Author's Take\n\n" + stance + "\n"
    txt = txt[:m.start()] + block + txt[m.start():]
    open(path, 'w', encoding='utf-8').write(txt)
    return True

n = skip = 0
for eid, stance in STANCES.items():
    path = os.path.join(CONTENT, eid.replace('cty-', '') + '.md')
    if not os.path.exists(path):
        print(f'  !! 缺失 {path}'); continue
    if insert_stance(path, stance): n += 1
    else: skip += 1
print(f'city 立场块插入: {n} 篇, 跳过(已有): {skip}')
