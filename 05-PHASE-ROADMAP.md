# 05 — PHASE ROADMAP (Phase 1–5)

> Build the graph first, publish second. Network effect over page count.

---

## PHASE 1 — FOUNDATION (current, no articles)

**Deliverables (this phase):**
- [x] Master Entity Map
- [x] Manufacturing Cluster List (50)
- [x] Manufacturing City List (100)
- [x] Province List
- [x] Industry Taxonomy (35 → top 30)
- [x] Product Taxonomy (200 skeleton)
- [x] Manufacturer / Industrial Park / Port / Source entity models
- [x] Relationship Graph
- [x] SEO Topic Map
- [x] Priority Matrix
- [x] Phase 1–5 Roadmap

**Output rule:** Do NOT publish. Output MASTER CONTENT MAP + ENTITY GRAPH +
PRIORITY MATRIX, then enter per-entity research (Phase 2).

---

## PHASE 2 — DEPTH (per-entity research)

For each P0 cluster, build:
- Cluster page + City relationship + Products + Industries
- Manufacturers (verified only) + Industrial parks + Ports + Export markets
- Research article (one per major cluster)

**Workflow per topic (16 steps):**
1. Identify search intent → 2. Identify entities → 3. Search English →
4. Search Chinese → 5. Find primary evidence → 6. Cross-check conflicts →
7. Build structured facts → 8. Map relationships → 9. Analysis →
10. Original synthesis → 11. Author viewpoint → 12. Internal links →
13. Create/update DB entity → 14. Citations → 15. Factual QA → 16. SEO/AIO QA →
17. Publish only if quality gate met.

**Method rule:** search both English AND Chinese. Chinese terms:
`"[产品] 产业集群"` `"[产品] 产业基地"` `"[城市] 产业集群"` `"[产业] 产业链"` etc.

---

## PHASE 3 — COMPARISON

City vs City, Cluster vs Cluster, Province vs Province, product sourcing region
comparisons. No universal winner declared — explain which is better for WHICH
requirement.

---

## PHASE 4 — INDUSTRIAL RESEARCH

Original analysis articles (Why clusters formed where they did; PRD vs YRD;
EV supply-chain concentration; specialized towns; export geography evolution).

---

## PHASE 5 — LONG-TAIL

Expand Product×City, Product×Cluster, Industry×City, Industry×Province. Only
create pages when enough unique evidence exists.

---

## QUALITY GATE (every major page, before publish)

| Dimension | /10 |
|---|---|
| Research Depth | |
| Evidence Quality | |
| Originality | |
| Industrial Knowledge | |
| Data Quality | |
| SEO Value | |
| AIO Value | |
| Entity Relationships | |
| E-E-A-T | |
| Writing Quality | |

**Minimum to publish:** Overall ≥8, Evidence ≥8, Originality ≥8.
Below threshold → return to research. Do NOT publish.

---

## ARCHITECTURE (deployment)

- **Main site:** Astro (editorial authority + research + analysis)
- **Database hub:** MkDocs (structured knowledge + entities + data + evidence)
- No duplicated content between the two.

### Main site sections
`/ /manufacturing-clusters/ /manufacturing-cities/ /manufacturing-regions/
/industries/ /products/ /manufacturing-guides/ /research/ /reports/ /comparisons/
/methodology/ /about/ /authors/`

### Database hub sections
`/data/regions/ /provinces/ /cities/ /districts/ /clusters/ /industries/
/products/ /manufacturers/ /industrial-parks/ /components/ /raw-materials/
/ports/ /trade-fairs/ /export-markets/ /hs-codes/ /sources/`

---

## RELATIONSHIP TO OTHER PROJECTS (no duplication)

- This site = geographic/industrial foundation
- Vertical sites (EV/Battery/Solar/Machinery) = deep technical authority
- WorldFreightHub = trade/logistics layer

This project owns the **geographic relationship** (cluster ↔ city ↔ port ↔ market).

---

## FINAL PRINCIPLE

The product is not the article — it is the **China Manufacturing Knowledge Graph**.
Articles = human interface. Database pages = structured interface. Research =
authority layer. SEO = acquisition. AIO = retrieval. Commercial = monetization
(Phase 1 keeps editorial independence).
