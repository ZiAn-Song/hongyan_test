# 鸿雁 - 线上社会实践云平台

## 项目结构

```
鸿雁/
├── frontend/          # Vue 3 前端
├── backend/           # FastAPI 后端
├── scripts/           # 工具脚本
├── data/              # 静态数据
├── img/               # 图片资源
├── render.yaml        # Render 部署配置
└── README.md
```

## 本地开发

### 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

## 部署

### Cloudflare Pages（前端）

1. 在 Cloudflare Pages 创建项目
2. 构建命令: `npm run build`
3. 输出目录: `dist`
4. 环境变量按需配置

### Render（后端）

1. 在 Render 创建 Web Service
2. 指向 `backend/` 目录
3. 构建命令: `pip install -r requirements.txt`
4. 启动命令: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. 环境变量在 render.yaml 中定义


## 智能匹配 v2（三级漏斗）

核心接口：`GET /api/matching/v2/demands/{demand_id}/match?use_llm=true&top_k=8`

```
第一级 L1  SQL 全量载入：内地供给(36) + 山大人才库(48)
第二级 L2  关键词打分 + 标签匹配加权 × 三因子动态可信度（来源0.4/时效0.3/核验0.3）
第三级 L3  DeepSeek V4 研判：评分 + 匹配理由 + 风险提示 + 对接建议
           （失败自动降级规则模式，服务永不中断）
附    历史范式参考：已完成成果库的可复制协作点 Top3
```

- 跨类型统一排序：企业/政府供给与高校科研人才在同一序列竞争排名（candidate_type 标记来源）
- LLM 网络调用在独立子进程中执行（scripts/llm_call.py），主服务永不因网络层崩溃

### 导入真实数据

```bash
cd backend
python scripts/import_real_data.py   # 幂等，导入 142 条案例库 + 48 条人才库
```

### 环境变量

复制 `.env.example` 为 `.env` 并填入 `DEEPSEEK_API_KEY`。

## RAG 向量召回（L2 增强）

嵌入模型：火山方舟 `doubao-embedding-vision-251215`（多模态端点）。

1. `.env` 填入 `EMBEDDING_API_KEY=<ARK_API_KEY>`
2. 构建向量索引：`python scripts/build_embeddings.py`（幂等，文本变化自动重建）
3. 无向量/无 key 时自动降级为关键词+标签匹配；有向量时余弦相似度自动并入 L2 打分

生产 PostgreSQL 时 `resource_embeddings` 表平迁为 pgvector 列即可。
