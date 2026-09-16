#!/usr/bin/env python3
"""Insert '## The Author's Take' stance blocks into product pages."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, 'content', 'products')

STANCES = {
'prd-agri-machinery': """*In my view, agricultural machinery is a single-champion industry — one anchor, one city, one cluster — so the real sourcing decision is which machine you need, not which region to shop.*

For complete tractors and combines, YTO in Luoyang is the anchor; for engines and powertrain, Weichai in Weifang is a separate lane. That concentration gives you a deep, stable supply chain, but it also means less competitive tension than in a multi-champion category.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-biopharma': """*In my view, biopharma is a discovery-and-scale-up pair, and you should route by that split rather than treating Shanghai and Suzhou as competitors.*

Shanghai discovers and licenses out; Suzhou develops and manufactures at CDMO scale. But the real cost driver is regulatory load — NMPA plus CE/FDA — which you should price in before anything else.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-carbon-fiber': """*In my view, carbon fiber is a strategic, export-controlled material, so its value is supply-chain security, not commodity volume — and that changes what "sourcing" means here.*

Changzhou is the correct anchor for aerospace-grade fiber and composites, but export controls attach to aircraft end-use, so verifying end-use is a hard requirement, not a formality.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-ceramic-tile': """*In my view, building ceramics is maturing and consolidating — flat-to-declining tile volume means the value has shifted from commodity tile to branded tile and the machinery that makes it.*

For branded tile, Foshan is the anchor; for production machinery and turnkey lines, Foshan's Keda and Lital are actually the higher-margin layer. If you only want commodity volume, expect thin margins and a shrinking firm base.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-ev-battery': """*In my view, EV batteries are the most concentrated industry in this dataset, and that concentration is a real risk you should hedge, not accept.*

CATL is effectively unavoidable for high-performance cells, but with two firms holding the bulk of supply, the prudent move is dual-sourcing — anchor volume with CATL and qualify BYD or a credible second source in parallel.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-excavator': """*In my view, excavators sit inside a dual-pole oligopoly, and the choice between Changsha and Xuzhou is variety versus integration — two different buying strategies, not two interchangeable regions.*

Go to Changsha for multi-vendor negotiation leverage and niche specs; go to Xuzhou for single-account scale and a full machine lineage. Match the strategy to the purchase, not the other way around.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-footwear': """*In my view, footwear is a density-plus-brand cluster, and the mistake is treating Chendai's commodity floor and the Anta/Xtep brand tier as one market.*

They are different supplier tiers with different pricing, quality, and lead-time profiles. Match deliberately: commodity volume to Chendai's 3,000-firm base, branded or ODM work to the Anta/Xtep tier.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-furniture': """*In my view, Foshan is the right anchor for multi-category furniture sourcing because of one asset — Lecong's showroom floor, where you can physically compare thousands of suppliers in one place.*

But the flat domestic market means commodity margins stay thin. The play is to walk Lecong for discovery, then anchor on branded home-furnishing suppliers rather than the anonymous factory long tail.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-hardware-tools': """*In my view, Yongkang is a category monopoly, not a brand monopoly — it dominates hardware through enterprise density and a 50-year local supply chain, not through one champion.*

That means power tools and doors route to Yongkang, but with per-factory safety certification as a hard gate, and kitchen cutlery routes to Yangjiang, where standards leadership matters more.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-home-appliance': """*In my view, home appliances is a three-tier industry, and each tier owns a different layer of the same value chain — the error is routing all appliance needs to one city.*

Brand and OEM-scale white goods go to Qingdao (Haier, Hisense); manufacturing depth to Shunde; niche density and fast SKU iteration to Cixi. Pick the tier, then the city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-home-textile': """*In my view, Nantong home textiles are market-anchored, not factory-anchored — the trading towns are the gravitational center, and thousands of factories orbit them.*

That structure is ideal for small batches and fast iteration, which is exactly what the RMB 150B Die-shi-qiao turnover signals. For bedding and linens, that liquidity is the reason to anchor here.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-industrial-robot': """*In my view, industrial robots are a technology-origin plus volume-distributed industry, so you must separate the arm from the deployment.*

Shenyang (SIASUN) owns the standards and lineage for robot arms; Shenzhen and Shanghai own volume, integration, and AI deployment. Evaluate whether a supplier is a traditional-arm maker or an embodied-intelligence integrator — they are different bets.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-intelligent-voice': """*In my view, intelligent voice is a champion-anchored, policy-designated industry — one firm plus one national cluster concentrated the entire chain in Hefei.*

That concentration is great for speech recognition, synthesis, and platform licensing (iFlytek), but it also means less competitive tension. For voice-AI you anchor in Hefei; for the hardware that runs it, Shenzhen is the integration node.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-knives-scissors': """*In my view, Yangjiang is a category monopoly with a standards moat — it owns the quality-definition layer, which makes it a safer starting point than a pure commodity cluster.*

For kitchen cutlery, that standards leadership (international plus national) is a genuine differentiator. But "monopoly" cuts both ways: you still verify each maker against your specific spec rather than assuming uniformity.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-leather': """*In my view, Haining leather is a trade-city-anchored, fashion-upgrading chain, and the tier you buy from matters more than the city itself.*

The market floor is commodity; the design-and-ODM tier is the value layer. Haining is the right anchor for finished leather garments and autumn-winter fashion, but commodity hides and mass garment blanks are not its strength.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-led-lighting': """*In my view, Guzhen's LED lighting is a density-driven category monopoly — its edge is spatial density that produces unmatched speed and price on fixtures.*

But the chip and driver layer is a distinct oligopoly, and that is where the technology actually lives. Anchor fixtures and assembly in Guzhen, and source the chip/driver upstream, separately.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-low-voltage-electrical': """*In my view, Yueqing is a self-grown cluster with a champion tier — it emerged from township enterprises, which explains both its extreme category breadth and the wide certification spread across its long tail.*

For low-voltage breakers, contactors, relays, and switchgear, Yueqing is the anchor and complements Baoding's high-voltage pole. But verify certification per factory: Chint-tier suppliers are not the same as the tail.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-machine-tool': """*In my view, East Zhejiang is a self-grown, upgrade-driven cluster, so the buying decision is about the specific tolerance you need, not the region's average quality.*

It provides volume and price on commodity and conventional machine tools, while the national story is the CNC-ization climb. For commodity tools, East Zhejiang wins on price; for high-end CNC, you specify and verify per supplier.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-medical-device': """*In my view, medical devices sit at the hardware-software intersection, which is why the sourcing split mirrors biopharma — hardware in one place, scale-up in another.*

Hardware devices (monitors, ultrasound, IVD instruments) go to Shenzhen; device-adjacent consumables and biologics scale-up go to Suzhou. Recognize which half of the device you are actually buying.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-ndfeb-magnet': """*In my view, NdFeB magnets are a three-node value chain, and matching the magnet grade to the node is the whole game.*

Raw light rare earth is Baotou, raw heavy rare earth is Ganzhou, finished magnets are Ningbo. For standard NdFeB, the Baotou-to-Ningbo chain works; for high-temperature grades, you depend on Ganzhou's dysprosium and terbium.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-nev': """*In my view, EVs are a three-pole, penetration-driven industry, and the poles diverge structurally, not just geographically.*

BYD in Shenzhen is vertically integrated, Shanghai is the foreign-brand and energy-storage pole, and Changchun is the near-site FAW ecosystem. Route by what you actually need — platform, export brand, or domestic cost structure.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-optical-fiber': """*In my view, optical fiber is a full-chain, single-anchor industry, and the layer you buy matters more than the city label.*

Wuhan owns the preform-fiber-cable vertical — the high-barrier core — while Shenzhen owns components and modules. Match the layer: the preform is the hard part, and that routes to Wuhan's Optics Valley.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-pcb': """*In my view, PCBs sit at the electronics-stack midpoint, and Shenzhen's assembly layer and Dongguan's CCL material layer are two different value chains, not two substitutes.*

For finished PCBs and assembly, Shenzhen is the density-and-speed anchor; for CCL materials, Dongguan (Shengyi) is the barrier layer. High-layer-count HDI boards also route to Shenzhen's advanced fabs.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-power-equipment': """*In my view, power transmission equipment is a state-anchored, transmission-layer industry, and "power equipment" is too broad a label to source against.*

Baoding owns the high-voltage/UHV transformer-and-transmission stack, a policy-priority, few-supplier segment. For high-voltage and UHV, Baoding is the anchor; low-voltage is a different city, and generation is a third.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-pump-valve': """*In my view, pumps and valves are a specialist-base, town-anchored industry — each town owns a niche, so you match the specialist to the part.*

Industrial pumps route to Wenling (Taizhou), precision valves to Yuhuan, and general valves to Wenzhou. There is no single "pump-and-valve city" that covers everything well; the fragmentation is the structure.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-rail-equipment': """*In my view, rail equipment is effectively a single-vendor category, and that changes how you buy — this is not a market with interchangeable suppliers.*

It routes through CRRC's two poles: Zhuzhou for rolling stock and locomotives, Changchun for high-speed rail. For spec-heavy or export rail projects, Zhuzhou's standards leadership is the safer anchor.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-rare-earth': """*In my view, rare earth is a quota-governed, dual-source industry, and the light-versus-heavy element split is the defining structural fact you must match against.*

Light rare earth (Nd/Pr) routes to Baotou; heavy rare earth (Dy/Tb) routes to Ganzhou. High-temperature magnets cannot substitute around the heavy fraction, so element-matching — and licensing — is the real skill.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-security-camera': """*In my view, security cameras are a duopoly cluster, and that means this is effectively a two-vendor category — most enterprise procurement lands on Hikvision or Dahua.*

The real decision has already moved past the camera itself to the AIoT and analytics stack. So the sourcing question is less "which camera maker" and more "which platform you are committing to."

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-semiconductor': """*In my view, semiconductors are a foundry-anchored, substitution-driven industry — growth is policy-pulled as much as market-pulled, which shapes what you can realistically source.*

Domestic IC design and foundry route to Shanghai Zhangjiang. But advanced-node access is externally constrained, so the realistic use is design, packaging, and mature-node work — price that in rather than hoping for leading-edge capacity.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-ship': """*In my view, shipbuilding is a cyclical, capital-intensive champion industry, and profit growth outpacing revenue is the signature of a supply-constrained upcycle — which affects both price and lead time.*

Route by role: total assembly and large vessels to Qingdao, marine-engineering platforms to Yantai, co-building fabrication to Weihai. Treat the three as one role-split cluster, not three ports.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-small-appliance': """*In my view, Cixi is the niche-density layer of small appliances — a cluster optimized for fast SKU iteration and price, not for brand equity.*

For air fryers, kettles, and hair dryers where speed and price matter, Cixi is the right anchor. For branded white goods, you are in the wrong city — that is Qingdao's or Shunde's layer.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-smartphone': """*In my view, smartphones are a brand-anchored assembly industry, and the "1 in 5 / 1 in 7" figures are assembly-share metrics — distinct from the components-and-design layer in Shenzhen.*

For final assembly and ODM, Dongguan (Android) and Zhengzhou (iPhone) are the anchors. For components and design, go upstream to Shenzhen. Do not conflate assembly share with component capability.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-socks': """*In my view, Datang is a single-town category monopoly — for volume hosiery there is effectively no alternative anchor of equivalent scale, and the density produces unmatched price and speed.*

The 194 digital workshops signal it is automating to defend share, not resting on it. But for branded and design socks, the value layer sits upstream; Datang is the commodity floor, not the brand layer.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-solar-panel': """*In my view, solar panels are a full-chain, cost-leadership industry — China owns the entire value chain and sets global module pricing, which is both the opportunity and the risk.*

For PV modules, Yancheng (Trina Solar) and the Jiangsu-Anhui belt are the anchors. The cost leadership means globally competitive pricing, but expect volatility — you are buying into a price-setting, not price-taking, node.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-textile-fabric': """*In my view, textile fabrics are a trading-plus-manufacturing layer, and you route by which layer of the textile stack you actually need.*

Raw and printed fabric plus dyeing route to Keqiao (Shaoxing); garment-layer production routes to Hangzhou Bay; finished home textiles route to Nantong. "Textile" is four different sourcing decisions wearing one name.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-toys': """*In my view, toys are a volume-to-IP shift industry, and the two ends of the market are different cities.*

Commodity plastic toys route to Chenghai (a third of the world), while art and trend toys route to Dongguan, with a rising AI-toy layer on top. Match the product tier — commodity, IP, or AI — to the city.

*This is my editorial judgment, not a verified fact — the sourced figures are above.*""",

'prd-wind-turbine': """*In my view, wind turbines are a resource-plus-manufacturing, scale-leaping industry, and China's share of global new installations makes it the price-setting node.*

For offshore-wind turbines and systems, Yancheng (Goldwind) is the anchor, and you can pair PV plus wind from one geography for integrated clean-energy capex. The 18–26 MW turbine leap is the signal that scale, not cost labor, is the moat.

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
    path = os.path.join(CONTENT, eid.replace('prd-', '') + '.md')
    if not os.path.exists(path):
        print(f'  !! 缺失 {path}'); continue
    if insert_stance(path, stance): n += 1
    else: skip += 1
print(f'product 立场块插入: {n} 篇, 跳过(已有): {skip}')
