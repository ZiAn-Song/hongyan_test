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
