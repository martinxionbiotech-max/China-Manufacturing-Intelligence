# 03 — PRIORITY MATRIX & SCORING METHODOLOGY

> Never present subjective rankings as objective facts. Every score has a
> definition, evidence, method, confidence, and date.

---

## A. SCORING DIMENSIONS (per entity)

Each entity (cluster / city / industry / product) is scored 1–5 on seven axes:

| Axis | Definition | What "5" means |
|---|---|---|
| **Search Potential** | English search volume for buyer queries | High "where is X made" demand |
| **Commercial Intent** | Likelihood the searcher is a buyer/sourcer | Direct sourcing/RFQ intent |
| **Evidence Quality** | Availability of primary Chinese + English sources | Rich gov/association data |
| **Content Difficulty** | Ease of producing differentiated, original content | Low competition, info-gap exists |
| **Uniqueness** | How underserved the topic is in English | Few/no strong English pages |
| **Database Value** | How many entities/edges this node connects | Hub connecting many clusters/products |
| **Cluster Density** (clusters only) | Supplier concentration / ecosystem depth | Dense verified ecosystem |

**Overall Priority** is derived, not a single number:

```
Priority (P0/P1/P2/P3) = f(Search, Commercial, Evidence, Uniqueness)
```

---

## B. PRIORITY TIER DEFINITIONS

- **P0 (Anchor / build first):** High search + high commercial intent + strong
  evidence + meaningful English info-gap. These are the pillar clusters/industries
  that seed the knowledge graph.
- **P1 (Depth layer):** Strong value but slightly lower on one axis (e.g., rich
  Chinese evidence but thinner English gap, or vice versa).
- **P2 (Expansion layer):** Solid but narrower; build once P0/P1 entities exist
  to link into.
- **P3 (Long-tail / opportunistic):** Low search volume but high uniqueness; only
  build when evidence is strong and it adds network value.

---

## C. TOP 30 INDUSTRIES — PRIORITY

| Priority | Industries |
|---|---|
| **P0** | Electronics & ICT, Semiconductors/IC, Power Batteries, NEV/ICV, Solar/PV, Construction Machinery, Home Appliances, LED/Lighting, Machine Tools, Energy Storage |
| **P1** | Textiles & Garments, Furniture & Home, Footwear, Hardware & Tools, Motors & Electrical Equipment, Pumps & Valves, Bearings, Medical Devices, Pharmaceuticals/Biotech, Advanced Materials (rare earth/magnetic/carbon) |
| **P2** | Agricultural Machinery, Rail Transit Equipment, Shipbuilding & Marine, Aviation & Aerospace, Robotics, Power Transmission (UHV), Scientific Instruments, Chemicals & Petrochemicals, Steel & Metals, Toys & Sports Products |
| **P3** | IoT, Digital Security/Surveillance, AI/Intelligent Voice, Wind Power, Small Commodities |

> Rationale: P0 = industries where China's cluster concentration is highest,
> English buyer demand is largest, and the "where is it made" question is most
> frequently searched but poorly answered in English.

---

## D. TOP 50 CLUSTERS — PRIORITY

| Priority | Clusters (abbrev) |
|---|---|
| **P0 (build first, ~15)** | Shenzhen Electronics, Dongguan Smart Terminal, Ningde Power Battery, Changsha Construction Machinery, Zhuzhou Rail Transit, Shanghai IC, Wuhan Optoelectronics, Guzhen Lighting, Yiwu Commodities, Yongkang Hardware, Jinjiang Footwear, Foshan Furniture, Cixi Small Appliances, Wenzhou Electrical, Ningbo Magnetic Materials |
| **P1 (~20)** | Shanghai NEV, Changchun Auto, Xuzhou Construction Machinery, Suzhou Nano, Changzhou Carbon, Ganzhou Rare Earth, Baotou Rare Earth, Ningbo Green Petrochemical, Suzhou-Wuxi-Nantong Textile, Hangzhou Bay Textile, Quanzhou Sports Products, Qingdao Appliances, Foshan-Dongguan Pan-Home, Shenyang Robotics, Yancheng PV, Hefei Intelligent Voice, Hangzhou Digital Security, Wuxi IoT, Chengdu-Chongqing Electronics, East-Zhejiang Machine Tools |
| **P2 (~15)** | Xi'an Aviation, Zhuzhou Aero Engines, Shanghai Zhangjiang Biomed, Suzhou Biomed, Shenzhen-Guangzhou Medical Devices, Qingdao Shipbuilding, Luoyang Agri-Machinery, Weifang Power Equipment, Baoding Power Equipment, Shantou Chenghai Toys, Yangjiang Knives, Shaoxing Keqiao Textiles, Taizhou Pumps, Zhuji Socks, Haining Leather |

---

## E. TOP 100 CITIES — PRIORITY (abbrev)

| Priority | Cities |
|---|---|
| **P0 (~20)** | Shenzhen, Guangzhou, Dongguan, Foshan, Shanghai, Suzhou, Ningbo, Hangzhou, Nanjing, Wuxi, Changzhou, Beijing, Tianjin, Qingdao, Wuhan, Changsha, Zhengzhou, Hefei, Chengdu, Chongqing |
| **P1 (~40)** | Zhongshan, Huizhou, Zhuhai, Jiangmen, Nantong, Taizhou, Wenzhou, Shaoxing, Jiaxing, Huzhou, Yangzhou, Xuzhou, Yancheng, Jinhua, Yantai, Weifang, Weihai, Jinan, Tangshan, Baoding, Dalian, Shenyang, Changchun, Harbin, Zhuzhou, Luoyang, Xiangyang, Nanchang, Xi'an, Deyang, Mianyang, Kunming, Xiamen, Quanzhou, Fuzhou, Ningde, Jinjiang, Shishi, Lanzhou, Baotou |
| **P2 (~40)** | Zhaoqing, Suqian, Huaian, Zhenjiang, Daqing, Qiqihar, Taiyuan, Shiyan, Suizhou, Zhangzhou, Putian, Yulin, Shihezi, + secondary county-level specialized towns |

---

## F. TOP 200 PRODUCTS — PRIORITY (abbrev)

| Priority | Product groups |
|---|---|
| **P0** | PCB, smartphone, semiconductor/IC, EV battery, solar panel, LED lighting, electric motor, CNC machine, injection molding machine, pump, valve, bearing, excavator, air conditioner, refrigerator, rice cooker, tire, auto parts, solar inverter, power adapter, connector, cable/wire harness, drone |
| **P1** | furniture (sofa/office/mattress), footwear (sneakers/leather), garment (socks/underwear/down jacket), textile (yarn/fabric), hardware (fasteners/locks/tools), lighting fixtures, small appliances (kettle/fan), medical devices, rare-earth magnets, aluminum profiles, plastic products, ceramics (tiles/sanitary ware), toys, stationery |
| **P2–P3** | long-tail: specific product × specific city/cluster combinations (see SEO Topic Map) |

> Full 200-item list is a Phase 2 expansion artifact (`data/product-taxonomy.md`),
> not published content. Only create a product page when enough unique evidence exists.

---

## G. METHOD & CONFIDENCE

- **Method:** Priority = weighted synthesis of Search, Commercial, Evidence,
  Uniqueness (weights 0.3 / 0.25 / 0.25 / 0.2). Cluster Density added for clusters.
- **Confidence:** Tier assignments are **Medium** confidence (analytical synthesis
  from MIIT cluster lists + city index + industrial geography). Individual facts
  inside each entity are researched and re-verified in Phase 2.
- **Date:** 2026-09-14. Tiers will shift as per-entity evidence is gathered.
