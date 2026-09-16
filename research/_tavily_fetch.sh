#!/bin/bash
# Tavily 直连检索（绕过工具旧 key，用 .env 新 key）
KEY=$(grep -i tavily ~/.openclaw/.env | head -1 | cut -d= -f2)
OUTDIR="/home/ubuntu/.openclaw/workspace/projects/china-manufacturing-intel/research/raw"
mkdir -p "$OUTDIR"
query="$1"
slug="$2"
curl -s -m 30 -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json,sys; print(json.dumps({'api_key':'$KEY','query':sys.argv[1],'max_results':5,'search_depth':'advanced'}))" "$query")" \
  > "$OUTDIR/$slug.json"
echo "saved $OUTDIR/$slug.json ($(wc -c < "$OUTDIR/$slug.json") bytes)"
