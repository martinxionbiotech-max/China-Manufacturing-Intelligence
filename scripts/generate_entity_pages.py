#!/usr/bin/env python3
"""P3: generate honest entity stub pages for manufacturers + industrial parks.

Strict rule: every field on the page comes from the verified YAML entity in
data-china-manufacturing-intel/data/entities/ — no invented numbers, no rankings.
Pages are baseline stubs (entity profile + cluster links), meant to grow later.
"""
import yaml, glob, os, datetime

DATA_ROOT = "/home/ubuntu/.openclaw/workspace/projects/data-china-manufacturing-intel/data/entities"
CONTENT_ROOT = "/home/ubuntu/.openclaw/workspace/projects/china-manufacturing-intel/content"

TODAY = datetime.date.today().isoformat()

ROLE_LABEL = {
    "manufacturer": "生产制造",
    "brand": "品牌商（无工厂生产角色，设计/品牌运营）",
    "contract_mfr": "代工制造 (contract manufacturer)",
}

def slug_of(yid, kind):
    prefix = "mfr-" if kind == "manufacturer" else "prk-"
    if yid.startswith(prefix):
        return yid[len(prefix):]
    return yid

def cluster_link(cid):
    return "/manufacturing-clusters/" + cid.replace("cls-", "") + "-cluster/"

def build_page(d, kind, slug):
    name = d.get("name_en") or d.get("id")
    loc = d.get("location") or {}
    city = loc.get("city", "")
    province = loc.get("province", "")
    industry = d.get("industry", "")
    role = d.get("entity_role", "")
    role_label = ROLE_LABEL.get(role, role or "未标注")
    confidence = d.get("confidence", "")
    vdate = d.get("verification_date", "")
    note = d.get("note", "")
    clusters = d.get("clusters", [])
    evidence = d.get("factory_evidence", [])

    type_slug = "manufacturer" if kind == "manufacturer" else "industrial-park"
    rel = [cluster_link(c) for c in clusters]

    lines = []
    lines.append("---")
    lines.append(f'title: "{name}"')
    loc_full = f"{province} {city}".strip()
    if kind == "manufacturer":
        lines.append(f'description: "{name} — {industry}，位于{loc_full}，{role_label}。所属集群与证据链见正文。"')
    else:
        lines.append(f'description: "{name} — {loc_full}的产业园区。所属集群与备注见正文。"')
    lines.append(f"entity_id: {d['id']}")
    lines.append(f"type: {type_slug}")
    lines.append(f"slug: {slug}")
    lines.append("status: draft")
    lines.append(f"date: {TODAY}")
    lines.append(f"last_verified: {vdate}")
    lines.append(f"city: {city}")
    lines.append(f"province: {province}")
    lines.append(f"industries: [{industry}]" if industry else "industries: []")
    lines.append("products: []")
    lines.append(f"related: {rel}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name}")
    lines.append("")
    lines.append("> 本页为实体档案基线版：所有字段取自 data/entities 的已核实 YAML 记录，未添加任何未经核实的数字或排名。")
    lines.append("")
    lines.append("## Entity profile")
    lines.append("")
    if kind == "manufacturer":
        lines.append(f"- **Name:** {name}")
        lines.append(f"- **Location:** {province} {city}")
        lines.append(f"- **Industry:** {industry}")
        lines.append(f"- **Entity role:** {role_label}")
    else:
        lines.append(f"- **Name:** {name}")
        lines.append(f"- **Location:** {province} {city}")
        lines.append(f"- **Note:** {note}" if note else "- **Note:** (无备注)")
    lines.append(f"- **Confidence:** {confidence}")
    lines.append(f"- **Verification date:** {vdate}")
    lines.append("")
    lines.append("## Linked clusters")
    lines.append("")
    if clusters:
        for c in clusters:
            lines.append(f"- [{c}]({cluster_link(c)})")
    else:
        lines.append("- (无关联集群)")
    lines.append("")
    if kind == "manufacturer" and evidence:
        lines.append("## Factory evidence")
        lines.append("")
        lines.append("The manufacturing role is asserted through the following cluster records:")
        lines.append("")
        for e in evidence:
            if e.startswith("cluster:"):
                c = e.split(":", 1)[1]
                lines.append(f"- {c} (集群记录)")
            else:
                lines.append(f"- {e}")
        lines.append("")
    lines.append("## The honest caveats")
    lines.append("")
    lines.append("- **基线页**：本页仅含实体档案字段，尚无独立的事实快照；详细数据见关联集群页。")
    lines.append("- **Confidence 字段**：以 data/entities YAML 的 confidence 为准，High/Medium 表示核实强度差异。")
    return "\n".join(lines) + "\n"

def main():
    made = []
    for kind, subdir in [("manufacturer", "manufacturers"), ("industrial-park", "industrial-parks")]:
        src = os.path.join(DATA_ROOT, subdir, "*.yaml")
        for f in sorted(glob.glob(src)):
            d = yaml.safe_load(open(f))
            slug = slug_of(d["id"], kind)
            outdir = os.path.join(CONTENT_ROOT, "manufacturers" if kind == "manufacturer" else "industrial-parks")
            os.makedirs(outdir, exist_ok=True)
            out = os.path.join(outdir, slug + ".md")
            with open(out, "w") as fh:
                fh.write(build_page(d, kind, slug))
            made.append(out)
    print(f"generated {len(made)} pages")
    for m in made[:5]:
        print(" ", m)

if __name__ == "__main__":
    main()
