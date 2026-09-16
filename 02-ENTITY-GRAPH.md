# 02 — ENTITY GRAPH & DATA MODEL

> The structured backbone. Every entity is typed, has a stable ID scheme, and
> carries provenance fields. Articles are the human interface; this is the graph.

---

## A. ENTITY TYPES (19)

| # | Entity | ID prefix | Example |
|---|---|---|---|
| 1 | Region (belt) | `reg` | Pearl River Delta |
| 2 | Province | `prv` | Guangdong |
| 3 | City | `cty` | Shenzhen |
| 4 | District/County | `dst` | Bao'an |
| 5 | Industrial Cluster | `cls` | Shenzhen electronics |
| 6 | Industry | `ind` | Electronics & ICT |
| 7 | Product | `prd` | PCB |
| 8 | Component | `cmp` | Connector |
| 9 | Raw Material | `mat` | Copper foil |
| 10 | Manufacturer | `mfr` | (verified only) |
| 11 | Industrial Park | `prk` | (verified only) |
| 12 | Port | `prt` | Shenzhen (Yantian) |
| 13 | Trade Fair | `fai` | Canton Fair |
| 14 | Export Market | `mkt` | USA / EU |
| 15 | HS Code | `hsc` | 8534 (PCB) |
| 16 | Technology | `tec` | SMT assembly |
| 17 | Certification | `cer` | ISO 9001 / CCC |
| 18 | Source | `src` | (evidence record) |
| 19 | Author/Institution | `org` | MIIT |

**ID convention:** `<prefix>-<slug>` lowercase ASCII, e.g. `cls-shenzhen-electronics`,
`prd-pcb`, `prv-guangdong`, `hsc-8534`.

---

## B. RELATIONSHIPS (directed edges)

```
Region     --contains-->       Province
Province   --contains-->       City
City       --contains-->       District
District   --contains-->       Cluster
Cluster    --specializes_in--> Industry
Industry   --produces-->       Product
Product    --requires-->       Component
Component  --requires-->       Raw Material
Cluster    --hosts-->          Manufacturer
Manufacturer --belongs_to-->   Cluster
Manufacturer --produces-->     Product
Manufacturer --holds-->        Certification
Manufacturer --has-->          Export Evidence
Cluster    --hosts-->          Industrial Park
City       --served_by-->      Port
Cluster    --exports_to-->     Export Market
Product    --maps_to-->        HS Code
Product    --made_with-->      Technology
Trade Fair --hosted_in-->      City
Source     --supports-->       (any entity claim)
```

**Edge cardinality note:** many-to-many throughout. A cluster can specialize in
multiple industries; a product can be made in multiple clusters. The graph is a
network, not a tree.

---

## C. ENTITY DATA SCHEMAS

### Cluster (core entity)
```yaml
id: cls-guzhen-lighting
type: IndustrialCluster
name_en: Guzhen Lighting Cluster
name_zh: 古镇灯饰产业集群
location: { province: Guangdong, city: Zhongshan, district: Guzhen Town }
cluster_type: specialized_town   # or national_cluster
primary_industry: Lighting
major_products: [LED bulbs, chandeliers, street lights]
evidence_level: Medium           # High | Medium | Low
last_verified: 2026-09-14
sources: [src-...]
```

### Manufacturer (strict evidence rules)
```yaml
id: mfr-<slug>
type: Manufacturer
legal_name: (registered name)
name_en: 
name_zh: 
location: { province, city, district }
cluster: [cls-...]
industry: [ind-...]
products: [prd-...]
entity_role: manufacturer       # manufacturer | trader | distributor | brand | OEM | ODM | contract_mfr
factory_evidence: [src-...]     # REQUIRED to claim "manufacturer"
certifications: [cer-...]
export_evidence: [src-...]
official_website: 
verification_date: 
confidence: Medium              # High | Medium | Low
```

> ⚠️ **Hard rule:** `entity_role` defaults to `trader` unless `factory_evidence`
> exists. "Company sells X" ≠ "Company manufactures X".

### Product (SEO anchor entity)
```yaml
id: prd-pcb
type: Product
name_en: Printed Circuit Boards (PCB)
name_zh: 印制电路板
industry: Electronics
hs_codes: [8534]
major_clusters: [cls-shenzhen-electronics, ...]
major_cities: [Shenzhen, Dongguan, Suzhou, ...]
components: [cmp-copper-foil, cmp-pcb-ink]
export_markets: [mkt-us, mkt-eu, mkt-jp]
```

### City
```yaml
id: cty-shenzhen
type: City
name_en: Shenzhen
name_zh: 深圳
province: Guangdong
region: Pearl River Delta
major_industries: [Electronics, NEV, ...]
clusters: [cls-...]
ports: [prt-yantian, prt-shekou]
```

### Port
```yaml
id: prt-yantian
type: Port
name_en: Shenzhen (Yantian)
name_zh: 深圳盐田港
city: Shenzhen
province: Guangdong
serves: [cls-shenzhen-electronics, ...]
```

### Source (evidence record — every fact links here)
```yaml
id: src-<hash>
type: Source
title: 
url: 
publisher:                 # gov | association | company | press | academic | b2b_platform
level: 1                   # 1 primary | 2 strong secondary | 3 discovery
date_accessed: 
supports_claim: (text)
```

---

## D. EVIDENCE MODEL

### Source hierarchy
- **Level 1 (primary):** government statistics, MIIT/local gov, customs (海关),
  industry associations, official industrial-park sites, company official sites,
  trade fairs, regulatory bodies.
- **Level 2 (strong secondary):** established industry press, academic research,
  research institutes, reputable trade publications, major consulting.
- **Level 3 (discovery):** B2B platforms (Alibaba/Made-in-China), sourcing blogs,
  forums, social media. **Discovery only — never authoritative.**

### Confidence levels
- **High** — corroborated by ≥2 independent primary sources, or 1 primary + 1 strong secondary.
- **Medium** — single primary source, or strong secondary only.
- **Low** — discovery sources only, or conflicting reports.

### Fact classification (write in every page)
- **FACT** — directly supported by cited evidence.
- **INFERENCE** — derived from facts via stated reasoning.
- **OPINION** — author's interpretation, clearly labeled.

### Forbidden (never)
- Invent manufacturers / locations / markets / production numbers / rankings / share / certifications.
- Convert supplier → manufacturer without factory evidence.
- Copy competitor databases.

---

## E. KNOWLEDGE GRAPH STORAGE

Phase 1: store as structured YAML/Markdown under `data/entities/` (one file per
entity type). Phase 3+: migrate to a graph DB (Neo4j / a JSON-LD dataset) for
querying "Where is X made?" relationships programmatically.

Directory layout:
```
data/
  entities/
    provinces/   cities/   districts/   clusters/   industries/
    products/    manufacturers/   industrial-parks/   ports/
    trade-fairs/ export-markets/  hs-codes/   sources/
  relationships/
    edges.yaml
```
