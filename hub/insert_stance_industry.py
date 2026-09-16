#!/usr/bin/env python3
"""Insert '## The Author's Take' stance blocks into industry pages."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content', 'industries')

STANCES = {
'ind-advanced-materials': """*In my view, advanced materials is a layer, not a product — its value is that it sits upstream of aerospace, NEV, and electronics, so a materials breakthrough compounds across everything downstream.*

That is exactly why you should source it by application, not by generic category: carbon fiber routes to Changzhou (aerospace-grade, export-controlled), NdFeB magnets to Ningbo. "Advanced materials" as a shopping label hides the real decision.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-agri-machinery': """*In my view, agricultural machinery is a single-champion industry — one anchor, one city, one cluster — and that concentration is a trade-off, not a flaw.*

It produces a deep, stable supply chain, but less competitive tension than a multi-champion category. For complete machines, Luoyang (YTO) is the anchor; for engines and powertrain, Weifang (Weichai) is a separate lane.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-ai': """*In my view, the Hefei voice cluster is an algorithm-plus-institution cluster — built on a research university and a national champion, not on cheap labor or port logistics.*

That matters because "AI" is too broad a sourcing category. Split software and algorithm licensing (Hefei, iFlytek) from hardware integration (Shenzhen), and you stop making a category error that trips up a lot of buyers.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-automotive': """*In my view, China's auto industry is a dual-pole plus distributed-assembly structure — and matching brand tier and compliance requirement to the city is the whole sourcing game.*

Export and compliance NEVs go to Shanghai; domestic-brand cost structures go to Changchun; volume EV and electronics go to Shenzhen. Treat the three as different tiers of the same industry, not interchangeable regions.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-biopharma': """*In my view, biopharma is a discovery-and-scale-up pair — Shanghai discovers and licenses out; Suzhou develops and manufactures at CDMO scale — and it mirrors the IC and device industries' two-city logic.*

So split licensing and innovation (Shanghai Zhangjiang) from CDMO and biologics scale-up (Suzhou). The real cost driver is regulatory load — NMPA plus CE/FDA — and you should price that in before anything else.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-building-materials': """*In my view, building ceramics is a maturing, consolidating cluster — a shrinking firm base and flat export volume signal an industry rationalizing around branded product.*

So the split is branded tile (Foshan) versus production machinery and turnkey lines (Foshan's Keda and Lital, the higher-margin, Africa-exporting layer). If you only want commodity tile, expect thin margins and consolidation risk.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-construction-machinery': """*In my view, construction machinery is a dual-pole oligopoly — Changsha and Xuzhou split the industry's two strategic logics, and you pick a logic before you pick a city.*

Changsha gives competition and variety; Xuzhou (XCMG) gives integration and a full lineage. Multi-vendor negotiation leverage and niche specs go to Changsha; single-account scale and full-lineage consistency go to Xuzhou.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-electrical': """*In my view, low-voltage electricals is a category-density, channel-driven industry — 55% of sales flow through distribution, which keeps competition sharp and pricing honest.*

Yueqing is the correct anchor for commodity and mid-tier low-voltage (Chint and the cluster's 25,000+ models). For high-end and data-center-grade apparatus, route upstream — it is a different, more concentrated segment.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-electronics': """*In my view, electronics is a two-hub, layered industry — the Pearl River Delta and Yangtze Delta divide the work by layer, not by rivalry.*

So route by layer: components, PCBs, and design to Shenzhen; finished smart terminals to Dongguan; ICs and foundry to the Yangtze Delta (Shanghai); cost-optimized inland assembly to Chengdu-Chongqing. The layer tells you the city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-footwear': """*In my view, footwear is a density-plus-brand cluster — Chendai's extreme spatial density provides the commodity-OEM floor, while the anchor brands pull the whole cluster up-market.*

So match the supplier tier deliberately: commodity-volume sneakers to Chendai's 3,000-firm base; branded and ODM work to the Anta and Xtep tier; scaled contract manufacturing elsewhere. Different tiers, different prices, different quality.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-furniture': """*In my view, furniture is a market-plus-factory cluster — Lecong's 2-million-square-meter showroom is the discovery layer, with 30,000-plus makers behind it.*

The flat domestic market and faster export growth mean the value is shifting to branded home furnishings. Foshan is the correct anchor for multi-category sourcing (walk Lecong), but anchor on brands, not the anonymous factory tail.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-hardware': """*In my view, hardware is a niche-split industry — no single city owns all of "hardware," and Yongkang and Yangjiang each hold a category monopoly on opposite sides of the country.*

So anchor power tools and doors to Yongkang (with per-factory safety certification as a hard gate), and kitchen cutlery to Yangjiang (where standards leadership matters more). The two are complements, not competitors.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-home-appliances': """*In my view, home appliances is a three-tier industry — brand scale, manufacturing depth, and niche density each live in a different city, so routing all appliance needs to one place is the classic error.*

Brand and OEM-scale white goods go to Qingdao (Haier, Hisense); manufacturing depth to Shunde; niche density and fast SKU iteration to Cixi. Pick the tier, then the city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-leather': """*In my view, leather is a seasonal fashion supply chain, not a commodity industry — its strength is finished autumn-winter garments where a trading platform anchors the whole chain.*

So Haining is the correct anchor for finished, fashion-tier leather and fur garments, sourced in season. Commodity leather hides and mass garment blanks are not Haining's strength — that is a different, lower-value market.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-lighting': """*In my view, lighting is a category-monopoly plus technology-upgrade industry — Guzhen's extreme spatial density owns the commodity floor, while the LED-substitution wave is the growth engine.*

So anchor commodity LED fixtures to Guzhen, but source UV, plant, and Mini-LED specialty lighting from the technology layer (Shenzhen components plus specialized makers). The floor and the frontier are different cities.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-machine-tools': """*In my view, machine tools is a mother-machine plus upgrading industry — it makes the machines that make everything else, which makes it the highest-leverage layer in manufacturing.*

So coordinate machine-tool purchases against the rest of your factory investment; the multiplier runs both ways. Taizhou is the correct anchor for mid-to-high-end CNC and general machine tools, and its mother-machine role makes it a leverage point.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-medical-devices': """*In my view, medical devices sit at the hardware-software intersection — electronics, precision manufacturing, and clinical validation all meet in one product — so the sourcing split mirrors biopharma.*

Hardware devices (monitors, ultrasound, IVD instruments) route to Shenzhen; device-adjacent biologics and consumables scale-up route to Suzhou. Recognize which half of the device you are actually buying.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-optoelectronics': """*In my view, optoelectronics is a research-anchored, compute-driven industry — its demand now tracks AI and compute-network buildout as much as telecom.*

So anchor fiber, optical components, and laser equipment to Wuhan (Optics Valley), and pair Wuhan with Shenzhen for display integration. The compute cycle, not the telecom cycle, is now the demand driver to watch.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-power-battery': """*In my view, power batteries is the most concentrated industry in this dataset — a dominant two-firm share with the top-10 near saturation — and that is genuine concentration risk for buyers.*

Ningde and CATL are unavoidable for high-performance cells, but the concentration argues for dual-sourcing: anchor volume with CATL, qualify BYD or a credible second source in parallel, and do not put your supply chain in one basket.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-power-equipment': """*In my view, power equipment is a voltage-split industry — high-voltage transmission and low-voltage distribution are separate clusters in separate cities, unified only by the grid that connects them.*

So route by layer: transmission and UHV equipment to Baoding, low-voltage distribution to Yueqing. The grid-upgrade and new-energy cycle is a multi-year tailwind across both — a reason to anchor, not to hedge away.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-pumps': """*In my view, pumps is a fragmented, consolidating industry — no single champion, just a long tail of mid-size leaders, with roughly half the global market by volume but a smaller share of value.*

That fragmentation means per-supplier verification matters more than a regional label. Anchor commodity small water pumps to Wenling and precision valves to Yuhuan, with Wenzhou as the valve-and-pump complement.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-rail-transit': """*In my view, rail transit is a state-champion plus standards-led industry — its mechanism is CRRC plus standards leadership, not market density, and the 5-km local-supply radius is a structural strength.*

For complete locomotives, EMUs, traction systems, and metro equipment, Zhuzhou is the correct anchor, and its standards leadership makes it the safer starting point for spec-heavy or export rail projects.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-rare-earth': """*In my view, rare earth is a strategic, quota-governed industry — supply is policy-allocated, not market-cleared — and the light-versus-heavy element split is the key structural fact.*

For high-temperature magnets (dysprosium, terbium), route to Ganzhou's heavy rare earth; for standard NdFeB, route to Baotou's light feedstock. Element-matching and licensing, not price, are the real skills.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-robotics': """*In my view, robotics is a technology-origin plus volume-distributed industry — the technology was born in Shenyang, but the volume and deployment concentrate in the Delta.*

So split robot arms (Shenyang, SIASUN) from system integration and AI deployment (Shanghai and Shenzhen). Evaluate "robot plus AI" — embodied intelligence — capabilities specifically, because that is where the industry is heading.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-semiconductors': """*In my view, semiconductors is a foundry-anchored, substitution-driven industry — its growth is policy-pulled as much as market-pulled, which shapes what you can realistically source.*

For domestic IC design and foundry, route to Shanghai Zhangjiang. But advanced-node access is externally constrained, so the realistic use is design, packaging, and mature-node work — price that in rather than hoping for leading-edge capacity.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-shipbuilding': """*In my view, shipbuilding is a cyclical, capital-intensive champion industry, and the three-city Qingdao-Yantai-Weihai division is a role-split, not a rivalry.*

Anchor total assembly and large vessels to Qingdao (Beihai); marine-engineering platforms to Yantai (CIMC Raffles); co-building fabrication to Weihai. Treat the three as one cluster, and expect the upcycle to move price and lead time.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-solar-pv': """*In my view, solar PV is a full-chain, cost-leadership industry — China owns the entire value chain and sets global module pricing, which is both the opportunity and the risk.*

For PV modules, anchor to Yancheng (Trina Solar) and the Jiangsu-Anhui belt. The cost leadership means globally competitive pricing, but expect volatility — you are buying into a price-setting node, not a price-taking one.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-textiles': """*In my view, textiles is a layered, cluster-distributed industry — fabric, garments, home textiles, and socks each anchor a distinct geography, so "textile" is four sourcing decisions wearing one name.*

Route by layer: raw and printed fabric plus dyeing to Shaoxing (Keqiao); garments to Hangzhou Bay; home textiles to Nantong; socks to Zhuji. Match the layer to the cluster, not the label to one city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-toys': """*In my view, toys is a volume-to-IP shift industry — Chenghai's commodity plastic-toy base is being layered with Dongguan's art-toy and a rising AI-toy layer.*

So anchor commodity plastic toys to Chenghai; art and trend toys to Dongguan; and watch the AI-toy layer as the next move. The industry's center of value is shifting from volume to IP and intelligence.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-video-surveillance': """*In my view, video surveillance is a duopoly cluster — two firms hold roughly two-thirds of the market from one district — the mirror image of the fragmented category-monopoly clusters.*

The practical implication is that this is a two-vendor category: most enterprise procurement lands on Hikvision or Dahua. The real decision has moved past the camera to the AIoT and analytics stack you are committing to.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'ind-wind-power': """*In my view, wind power is a resource-plus-manufacturing, scale-leaping industry — China's dominant share of global new installations makes it the price-setting node, and the 18–26 MW turbine leap is the tell.*

For offshore-wind turbines and systems, anchor to Yancheng (Goldwind), and pair PV plus wind from one geography for integrated clean-energy capex. Scale, not cheap labor, is the moat here.

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
    path = os.path.join(CONTENT, eid[4:] + '.md')
    if not os.path.exists(path):
        print(f'  !! 缺失 {path}'); continue
    if insert_stance(path, stance): n += 1
    else: skip += 1
print(f'industry 立场块插入: {n} 篇, 跳过(已有): {skip}')
