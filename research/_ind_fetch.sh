#!/bin/bash
# 行业数据批量检索 — 中文产业规模关键词
KEY=$(grep -i tavily ~/.openclaw/.env | head -1 | cut -d= -f2)
OUTDIR="/home/ubuntu/.openclaw/workspace/projects/china-manufacturing-intel/research/raw"
mkdir -p "$OUTDIR"

declare -A Q
Q[advanced-materials]="中国 先进材料 新材料 产业 规模 2024 产值"
Q[agri-machinery]="中国 农业机械 产业 规模 2024 产值"
Q[ai]="中国 人工智能 产业 规模 2024"
Q[automotive]="中国 汽车 产业 产量 2024 新能源汽车"
Q[biopharma]="中国 生物医药 产业 规模 2024"
Q[building-materials]="中国 建材 陶瓷 产业 规模 2024"
Q[construction-machinery]="中国 工程机械 产业 规模 2024 产值"
Q[electrical]="中国 低压电器 电气设备 产业 规模 2024"
Q[electronics]="中国 电子信息 制造业 规模 2024"
Q[footwear]="中国 鞋业 运动鞋 产业 规模 2024"
Q[furniture]="中国 家具 产业 规模 2024"
Q[hardware]="中国 五金 工具 产业 规模 2024"
Q[home-appliances]="中国 家电 产业 规模 2024"
Q[leather]="中国 皮革 产业 规模 2024"
Q[lighting]="中国 照明 LED 产业 规模 2024"
Q[machine-tools]="中国 机床 数控机床 产业 规模 2024"
Q[medical-devices]="中国 医疗器械 产业 规模 2024"
Q[optoelectronics]="中国 光电子 光通信 产业 规模 2024"
Q[power-battery]="中国 动力电池 产业 规模 2024"
Q[power-equipment]="中国 电力装备 输变电 产业 规模 2024"
Q[pumps]="中国 泵阀 水泵 产业 规模 2024"
Q[rail-transit]="中国 轨道交通 装备 产业 规模 2024"
Q[rare-earth]="中国 稀土 产业 规模 2024"
Q[robotics]="中国 工业机器人 产业 规模 2024"
Q[semiconductors]="中国 半导体 集成电路 产业 规模 2024"
Q[shipbuilding]="中国 造船 船舶 产业 规模 2024"
Q[solar-pv]="中国 光伏 产业 规模 2024"
Q[textiles]="中国 纺织 产业 规模 2024"
Q[toys]="中国 玩具 产业 规模 2024"
Q[video-surveillance]="中国 视频监控 安防 产业 规模 2024"
Q[wind-power]="中国 风电 产业 规模 2024"

for slug in "${!Q[@]}"; do
  q="${Q[$slug]}"
  curl -s -m 30 -X POST https://api.tavily.com/search \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "import json,sys; print(json.dumps({'api_key':'$KEY','query':sys.argv[1],'max_results':4,'search_depth':'advanced'}))" "$q")" \
    > "$OUTDIR/ind-$slug.json"
  echo "[$slug] $q -> $(wc -c < "$OUTDIR/ind-$slug.json") bytes"
  sleep 1
done
echo "DONE"
