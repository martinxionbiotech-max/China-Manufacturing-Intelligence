#!/usr/bin/env python3
"""Insert skill-26.2 '## The Author's Take' stance blocks into cluster pages.
Each stance is written from the page's unique mechanism/data (differentiated, not templated).
Placed immediately before the '## Sources' section.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content', 'manufacturing-clusters')

# entity_id -> stance block (markdown, first-person, Position + Reasoning + Disclosure)
STANCES = {
'cls-baoding-power-equipment': """*In my view, Baoding is the high-voltage + new-energy pole — and if you source a full electrical BOM you will almost certainly touch both Baoding and Wenzhou, because no single Chinese city owns the whole voltage spectrum.*

Its real differentiator is the wind-solar-hydrogen-storage-transmission chain: it is North China's largest power and new-energy equipment base, not just a transformer town. That makes it the right anchor for high-voltage transmission and grid-scale new-energy gear.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-baotou-rare-earth': """*In my view, Baotou is the light-rare-earth volume anchor, and treating it as interchangeable with Ganzhou is the single most common sourcing mistake in rare earths.*

Baotou owns the cerium-lanthanum (volume ore) fraction from Bayan Obo, while Ganzhou owns the rarer heavy fraction. For raw light-rare-earth material and its downstream uses, Baotou is the anchor; for heavy rare earths and finished magnets, you look elsewhere.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-changchun-auto': """*In my view, Changchun is a state-champion pivot, not a market-born cluster — and that distinction determines what it is good for.*

FAW is converting a 1956 legacy into NEV through near-field localization (Audi PPE's 50% local sourcing), which is a top-down industrialization model, the opposite of Shanghai's foreign-anchor localization. For near-field NEV component sourcing it makes sense; for export-led or brand-diverse auto work, the Yangtze Delta is stronger.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-changzhou-carbon-fiber': """*In my view, Changzhou is the correct anchor for aerospace-grade carbon-fiber composites — but only if you budget for certification friction, because the qualification gate, not the material, is the real bottleneck.*

The ">1/3 of Jiangsu" output is a capacity signal, not a quality signal. Aerospace and defense specs are certification-gated, so lead time and audit cost will dominate the sourcing decision far more than price.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-chenghai-toys': """*In my view, Chenghai is genuinely different from a commodity toy town: its IP-and-patent leadership is a verifiable moat, not a marketing claim.*

With 50,000+ firms, a third of global plastic-toy capacity, and #1 standing in brands and IP licenses, it is the right place for licensed-character and branded toy sourcing. The catch is that extreme density also means extreme variance in quality — you cannot skip supplier screening here.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-cixi-small-appliances': """*In my view, Cixi is the export-velocity pole of China's appliance triangle — it is not where you go for brand, it is where you go for speed.*

One firm pushing 20,000 fryers a day and RMB 5B in two months is a throughput signal, not a quality signal. Shunde owns volume-plus-brand, Qingdao owns branded smart appliances, and Cixi owns ODM/OEM export speed — so match your need to the right city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-cy-electronics': """*In my view, Chengdu-Chongqing is the inland counterweight to the coastal electronics clusters, and its significance is as much strategic as commercial.*

The trillion-yuan twin-city scale is real, but the strategic logic — supply-chain diversification away from the coast — is what a buyer should weigh. It is a serious second sourcing base for laptop and terminal assembly, not a replacement for Shenzhen's components and design density.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-ezd-machine-tools': """*In my view, East Zhejiang is China's machine-tool scale pole, but scale is not the same as precision — the cluster spans a wide quality spectrum and you must specify, not assume.*

With roughly a fifth of national output, it is the right anchor for commodity and mid-range machine tools. But commodity machines and emerging high-end CNC coexist here, so a buyer has to verify each supplier against the specific tolerance they actually need.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-fd-pan-home': """*In my view, the Foshan-Dongguan pan-home cluster is a buyer-convenience construct, not a production cluster — and that is fine as long as you do not mistake the wrapper for the factory.*

Its value is re-bundling: ceramics and appliances from Foshan plus furniture from Dongguan into one stop. The underlying strength is the single-category clusters that already existed; the pan-home label is the packaging, not the source of quality.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-foshan-ceramics': """*In my view, Foshan is the clearest manufacturing-flight-plus-brand-headquarters case in this project, and it reframes what you are actually buying.*

Since 2007 Foshan deliberately moved kilns out to Qingyuan, Guangxi, and Jiangxi while keeping brand, HQ, R&D, and standards at home. So "Foshan tile" increasingly means Foshan-owned and Foshan-specified — if you want the cheapest kiln output, you may be buying from the relocation cities, not Foshan itself.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-foshan-furniture': """*In my view, Foshan is the right floor for furniture sourcing, with Lecong as the discovery layer — but fragmentation is the price of that convenience.*

Lecong lets you physically compare thousands of dealers in one place, which is rare and genuinely useful. The tradeoff is a fragmented factory base: you must verify the actual manufacturer behind any showroom, because the trading hub and the production base are not the same thing.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-ganzhou-rare-earth': """*In my view, Ganzhou is the heavy-rare-earth anchor, and its scarcest output — dysprosium and terbium — is what gives NdFeB magnets their high-temperature performance.*

That is the strategic point: heavy rare earths are the rarer fraction and the one that actually constrains high-end magnet supply. Ganzhou's central-SOE consolidation and downstream extension make it the anchor for that critical fraction, complementary to Baotou's volume ore.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-guzhen-lighting': """*In my view, Guzhen is the smallest unit of government producing the largest single-product market share — a trade-and-assembly cluster, not a technology cluster.*

Its "grassroots imitation + trade circulation" mechanism means it is the right place for cost-sensitive, high-volume lighting. It is not where you go for LED chip technology or driver innovation — for those, the value sits upstream elsewhere.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-haining-leather': """*In my view, Haining's value is the trading floor and the autumn-winter style-setting, not raw hide processing — and its headline scale is dispersed, not concentrated.*

The gap between a "RMB 100B" cluster narrative and a RMB 237.7M market-operator revenue is the analytical crux: the scale lives across many firms, not one anchor. For design-led, fashion-driven leather sourcing it works; for commodity hide processing, look elsewhere.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-hangzhou-bay-textile': """*In my view, Hangzhou Bay is the scale-manufacturing anchor for fabric, with Keqiao as its discovery layer — the two are one system, not two competitors.*

The RMB 1.01 trillion output and roughly a fifth of national fabric output make it the manufacturing floor, while Keqiao's world's-largest distribution center is the liquidity signal. A fabric buyer should treat them as a single sourcing corridor.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-hangzhou-digital-security': """*In my view, Hangzhou is simultaneously your quality floor and your leverage risk — the duopoly that guarantees export-grade systems is also the thing that concentrates pricing power.*

Hikvision and Dahua holding roughly 65% of a global market is rare outside tech. You get certified, export-grade surveillance, but you also get less room to negotiate than in a fragmented market.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-hefei-intelligent-voice': """*In my view, Hefei is the Chinese-language voice-AI anchor, and its edge is Mandarin performance plus ecosystem, not commodity hardware cost.*

USTC seeded the research and iFlytek industrialized it, which is why Hefei wins on Chinese-language capability rather than on being the cheapest place to build a speaker. For Chinese voice and speech-AI sourcing, it is the right anchor; for low-cost commodity hardware, it is not the differentiator.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-jinjiang-footwear': """*In my view, Jinjiang is a brand-anchored density cluster, and that brand layer is what separates it from an anonymous commodity floor like Guzhen.*

Its 3,000 firms in a tight radius are organized behind homegrown brands (Anta and its peers) rather than behind anonymous price. For branded or brand-capable footwear sourcing, that structure matters; for pure commodity volume, the calculus is different.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-keqiao-textile': """*In my view, Keqiao is the cleanest market-plus-industry closed loop in this project, and that is exactly what makes it different from a pure trading hub like Yiwu.*

Yiwu's goods mostly come from outside, but Keqiao's market drives local manufacturing — a quarter of the world's fabric trades through it and feeds back into the surrounding mills. That loop is the signal to look for if you want the market and the factory in one place.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-luoyang-agri-machinery': """*In my view, Luoyang is a state-champion chain city, and its 2024 designation is a policy signal that Henan is consolidating a fragmented sector behind one anchor.*

YTO is the cradle of China's tractor industry, and Luoyang's uniqueness — rather than raw scale — is the real asset. For agricultural-machinery sourcing anchored on a national-team supplier, it is the reference point.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-ningbo-green-petrochemical': """*In my view, Ningbo's petrochemical cluster is a legacy-heavy-industry modernization story, and its value is the smart-factory-plus-green upgrade, not commodity refining volume.*

Refining volume is mature; what is differentiated is Sinopec Zhenhai's integrated green and intelligent base. For buyers, that means the cluster is more interesting as a signal of process capability and environmental compliance than as a source of cheaper commodity feedstock.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-ningbo-magnetic-materials': """*In my view, Ningbo is the finished-magnet anchor of China's NdFeB chain, and the geographic split is cleaner than most buyers realize: Baotou supplies the ore, Ningbo makes the magnet.*

Its "created-from-nothing" origin — skill-and-capital-intensive fabrication, not a resource endowment — is the key insight. For finished rare-earth magnets, Ningbo is the anchor; for raw material, you go back up the chain to Baotou and Ganzhou.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-ningde-power-battery': """*In my view, Ningde's chain-leader-plus-ecosystem model is structurally different from Shenzhen's market-driven or Dongguan's brand-spillover models, and it works because batteries are a high-capital, high-scale industry.*

CATL built a world battery capital essentially around one anchor. For power-battery sourcing, that concentration is a feature — deep, integrated supply — but it also means you are largely negotiating within one ecosystem.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-qingdao-appliances': """*In my view, Qingdao is the brand-and-smart pole of China's appliance triangle, and that is what you are paying for here.*

Shunde owns volume, Cixi owns export speed, and Qingdao owns branded smart appliances (Haier, Hisense). For a buyer who wants a branded, smart, high-end appliance line, Qingdao is the anchor; for pure ODM volume or fastest export turnaround, the other two cities fit better.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-qingdao-shipbuilding': """*In my view, the Qingdao-Yantai-Weihai cluster is a role-split cluster, not a single-anchor one — and a buyer should route by role, not by a single port name.*

Qingdao does total assembly and large vessels, Yantai concentrates on marine engineering, and Weihai is the co-building base. Treating them as interchangeable will send you to the wrong dock for the wrong vessel type.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-quanzhou-sports': """*In my view, Quanzhou is the brand-and-volume anchor of China's sports products, and its OEM-to-brand ladder is the mechanism that matters most.*

ANTA, Xtep, and 361° climbed from contract work to global brands, and Jinjiang (a county within Quanzhou) is the manufacturing density underneath. For brand-capable sportswear and footwear, Quanzhou is the anchor; note the overlap with Jinjiang rather than treating them as two markets.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-sg-medical-devices': """*In my view, Shenzhen is China's finished-instrument pole of medical devices, complementary to Suzhou's R&D density and Zhangjiang's innovation-drug licensing.*

Mindray's 15-year #1 is a scale-and-consistency signal. For finished, digitalized, high-end medical devices, Shenzhen is the anchor; for early-stage device R&D or drug discovery, the corridor points elsewhere.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-shanghai-ic': """*In my view, Zhangjiang is the correct anchor for chip-design partnerships and foundry access — but you must price in a geopolitical constraint that no sourcing decision can ignore.*

Advanced-node foundry access is externally constrained, so the practical, realistic use of Shanghai is design, packaging, and mature-node work. Buyers who assume Zhangjiang gives them leading-edge capacity will be disappointed; buyers who use it for design and mature-node integration will do well.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-shanghai-nev': """*In my view, Shanghai is the foreign-superplant-plus-local-anchor model, and Tesla's gigafactory is the catalyst, not the whole story.*

Tesla brings technology, brand, and export channels; the surrounding Yangtze Delta brings low-cost, high-speed supply. For export-led NEV and EV-component sourcing, that combination is the point — you are buying into a corridor, not a single factory.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-shenyang-robotics': """*In my view, Shenyang is a knowledge-anchored, geographically-isolated cluster — its systems-integration strength is real, but it is detached from the electronics density that most robot sourcing needs.*

Its 50-year CAS lineage and SIASUN give it genuine integration capability, but it lacks the surrounding components-and-electronics density of the Yangtze or Pearl River Deltas. For systems integration it is strong; for a full robot BOM, expect to pull parts from the coast.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-shunde-home-appliances': """*In my view, Shunde is the private-sector mirror of Ningde's chain-leader model — one grew from a state-anchored giant, the other from grassroots entrepreneurs who became giants.*

Midea and Galanz are the anchor brands of the world's kitchen-and-living-room factory. For volume home-appliance sourcing with brand and component depth, Shunde is the reference point; it is the "volume" leg of the appliance triangle.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-suzhou-biomed': """*In my view, Suzhou is the industrialization pole of biopharma — the place where a molecule discovered in Zhangjiang gets manufactured at scale.*

Its park economy and patient capital built CDMO-style scale-and-manufacturing capability. The two cities form one Shanghai-Suzhou corridor: discovery in Zhangjiang, industrialization in Suzhou. Buyers should read them as a single corridor, not rivals.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-suzhou-nano': """*In my view, Suzhou's nano cluster stands apart for its closed loop — raw-material-to-application in one place — and that is rarer than the word "nano" suggests.*

Few advanced-materials clusters achieve a full chain, and Suzhou does. For buyers needing a nano-material or nano-enabled product with a coherent, traceable chain, that closure is the differentiator.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-swt-textile': """*In my view, Nantong is the bedding-and-linens anchor, distinct from Keqiao's commodity-fabric anchor — and the two serve different buyers.*

The RMB 150B Die-shi-qiao turnover is the liquidity signal, and live-stream e-commerce has reshaped the cluster's speed. For home textiles and bedding, Nantong is the anchor; for raw commodity fabric, Keqiao and Hangzhou Bay remain the floor.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-taizhou-pumps': """*In my view, Taizhou is a growing commodity cluster, not a mature one — and that growth, the 16.3% CAGR, is its differentiator against declining sectors.*

Wenling does pumps and motors, Yuhuan does precision valves, and the cluster's profile is volume-plus-specialization rather than brand. For a buyer who wants a supplier in an expanding rather than shrinking segment, that trajectory matters.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-weifang-power-equipment': """*In my view, Weifang is a generation-equipment cluster, not a transmission cluster — and that distinction defines the buyer universe.*

Weichai's diesel engines serve trucks, ships, and generators, a different world from Baoding's high-voltage transmission gear. Do not let "power equipment" in both names blur the line: generation buyers look here, transmission buyers look to Baoding.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-wenzhou-electrical': """*In my view, Yueqing is the low-voltage pole of China's power-equipment industry, and a full electrical BOM spans both it and Baoding — low voltage here, high voltage there.*

Its private chain leaders (Chint, Delixi) grew from township enterprises, which explains both the flexibility and the breadth. For low-voltage electrical and switchgear, Yueqing is the anchor.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-wuhan-optics-valley': """*In my view, Optics Valley is a university-and-research-density cluster with national strategic placement — deliberately built on existing talent, not born from market demand.*

That makes it the anchor for fiber-optic and laser capability, but a different animal from a market-driven cluster. For photonics, optical fiber, and laser sourcing, it is the reference point; for commodity electronics, the coast still wins on density.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-wuxi-iot': """*In my view, Wuxi is the standards-and-solutions pole of China's IoT, and its value is integration — sensing, V2X, industrial internet — rather than commodity hardware.*

As China's sole national IoT cluster and a source of standards, it occupies the upper layer of the IoT stack. For IoT solutions and system integration it is the anchor; for cheap sensors and modules, commodity hardware clusters elsewhere compete on price.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-xian-aviation': """*In my view, Xi'an is the least buyer-facing cluster in this dataset, and a general commercial buyer will find very little here — its value is strategic, not transactional.*

It holds China's only complete aviation industry chain and a quarter of national aerospace R&D, but that is large-aircraft and military-adjacent work. The actionable commercial angle is narrow, in aerospace supply-chain niches, not general sourcing.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-xuzhou-construction-machinery': """*In my view, Xuzhou and Changsha are structurally opposite poles, and the choice between them is depth versus variety.*

Xuzhou is one group (XCMG) spanning the full lineage — depth. Changsha is five firms covering 70% of national model range — variety. For a deep, single-supplier relationship, Xuzhou fits; for broad model choice across competing champions, Changsha fits.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-yancheng-pv': """*In my view, Yancheng is a resource-plus-manufacturing PV cluster, and its self-reinforcing loop — generation feeding its own module manufacturing — is what few other clusters have.*

Built around Trina Solar's solar-storage integrated base, it couples wind-and-PV generation with module production. For solar-storage integrated sourcing, that loop is the differentiator.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-yancheng-wind-power': """*In my view, Yancheng is the resource-plus-manufacturing anchor for offshore wind, and its differentiator is the test-and-validation ground, not just assembly capacity.*

The "~10% global offshore-wind share" is a resource figure as much as a manufacturing one, and the Dafeng test-and-validation base is the harder-to-replicate asset. For offshore-wind equipment and validation, that matters more than pure assembly scale.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-yangjiang-knives': """*In my view, Yangjiang is a category monopoly with a standards moat — it owns the definition of blade quality, which makes it a safer starting point than a pure commodity cluster.*

Making 7 of every 10 Chinese blades and holding standard-setting authority is a genuinely defensible position. For kitchen knives and scissors, the moat is why you start here — but "monopoly" also means you should still verify against your specific spec.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-yiwu-small-commodities': """*In my view, Yiwu is the world's shelf, not the world's factory — and confusing the two is the classic small-commodities sourcing error.*

The state legalized and scaled what peddlers already did, building a trading hub whose goods mostly come from elsewhere. For spot trading, variety, and low-MOQ discovery it is unmatched; for manufacturing, you must trace each product back to its actual origin cluster.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-yongkang-hardware': """*In my view, Yongkang is a multi-niche category monopoly — its breadth across doors, power tools, and vacuum cups is the unusual feature, signaling a shared metalworking mechanism rather than a single niche.*

That breadth means one city can serve several hardware categories at once, which is convenient. But breadth also means you should verify per-category depth rather than assuming mastery across all of them.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-zhangjiang-biomed': """*In my view, Zhangjiang is the discovery-and-licensing pole of biopharma, complementary to Suzhou's industrialization pole — a molecule is discovered in Zhangjiang and manufactured in Suzhou.*

Its licensing-out engine is the differentiated asset. For innovation-drug R&D, licensing, and early-stage biotech, Zhangjiang is the anchor; for scale manufacturing, follow the corridor to Suzhou.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-zhuji-socks': """*In my view, Datang is the highest-volume, most-automated sock cluster on earth, and for commodity hosiery there is effectively no alternative anchor of equivalent scale.*

It already held ~70% of China's socks, and its 194 digital workshops show it is automating to defend that share rather than resting on it. For commodity hosiery at scale, that is decisive; for premium branded socks, the calculus shifts.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-zhuzhou-aero-engine': """*In my view, Zhuzhou is a strategic monopoly, not a commodity cluster — its value is supply-chain-critical, but it is not buyer-facing in the usual sense.*

Small and mid aero-engines for drones, trainers, and light aircraft are a national-strategy sector. For general commercial buyers it is mostly out of reach; its relevance is to specialized aerospace supply chains.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'cls-zhuzhou-rail-transit': """*In my view, Zhuzhou is a single state-owned technology tree — one 1936 works that divided into a factory and a research institute, then branched into five CRRC subsidiaries and hundreds of suppliers.*

That concentration makes it the densest railway-equipment base on earth and the natural anchor for rail-transit sourcing. The tradeoff of one tree is less internal competition than a multi-champion market like Changsha's construction machinery.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",
}

def insert_stance(path, stance):
    txt = open(path, encoding='utf-8').read()
    if '## The Author\'s Take' in txt:
        return False
    # find '## Sources' heading
    m = re.search(r'\n## Sources\b', txt)
    if not m:
        print(f'  !! 无 Sources 段: {os.path.basename(path)}')
        return False
    block = "\n## The Author's Take\n\n" + stance + "\n"
    txt = txt[:m.start()] + block + txt[m.start():]
    open(path, 'w', encoding='utf-8').write(txt)
    return True

n = 0
skip = 0
for eid, stance in STANCES.items():
    path = os.path.join(CONTENT, eid.replace('cls-', '') + '-cluster.md')
    if not os.path.exists(path):
        print(f'  !! 缺失 {path}')
        continue
    if insert_stance(path, stance):
        n += 1
    else:
        skip += 1
print(f'cluster 立场块插入: {n} 篇, 跳过(已有): {skip}')
