from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, teams, demands, forum, ai, crawler, matching, contact


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="鸿雁平台 API",
    description="产学研融合助力边疆发展 - 线上社会实践云平台",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(teams.router, prefix="/api/teams", tags=["团队"])
app.include_router(demands.router, prefix="/api/demands", tags=["需求"])
app.include_router(forum.router, prefix="/api/forum", tags=["论坛"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(crawler.router, prefix="/api/crawler", tags=["爬虫"])
app.include_router(matching.router, prefix="/api/matching", tags=["智能匹配"])
app.include_router(contact.router, prefix="/api/contact", tags=["对接通道"])


# ============ 简单限流：防 LLM 接口被刷（单进程内存版；多 worker 部署时换 Redis）============
import time
from collections import defaultdict, deque

from fastapi import Request
from fastapi.responses import JSONResponse

RATE_LIMIT = 20          # 次
RATE_WINDOW = 60         # 秒
_req_log: dict[str, deque] = defaultdict(deque)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    path = request.url.path
    if request.method == "POST" and (path.startswith("/api/matching") or path.startswith("/api/ai")):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        q = _req_log[ip]
        while q and q[0] < now - RATE_WINDOW:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            return JSONResponse({"detail": "请求过于频繁，请稍后再试"}, status_code=429)
        q.append(now)
    return await call_next(request)


@app.get("/")
def root():
    return {"message": "鸿雁平台 API", "docs": "/docs", "version": "1.0.0"}
