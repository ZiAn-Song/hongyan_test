#!/bin/bash
# 鸿雁平台一键启动（前端 + 后端）
# 用法: 在本项目目录下执行  bash start.sh
set -e
cd "$(dirname "$0")"

PY=/Users/chaos/.workbuddy/binaries/python/envs/default/bin/python3
command -v python3 >/dev/null && PY=${PY:-python3}

cleanup() { kill $(jobs -p) 2>/dev/null; }
trap cleanup EXIT

(cd backend && exec $PY -m uvicorn app.main:app --host 0.0.0.0 --port 8000) &
(cd frontend && exec npx vite --port 5173 --strictPort) &

for i in $(seq 1 20); do
  curl -s -o /dev/null -m 1 http://localhost:5173 && \
  curl -s -o /dev/null -m 1 http://localhost:8000/docs && break
  sleep 1
done

open "http://localhost:5173" 2>/dev/null || true
echo ""
echo "=============================================="
echo " 鸿雁平台已启动"
echo "   网站      : http://localhost:5173"
echo "   接口文档   : http://localhost:8000/docs"
echo "   数据初始化 : cd backend && python scripts/import_real_data.py"
echo " 按 Ctrl+C 停止"
echo "=============================================="
wait
