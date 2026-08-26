from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, teams, demands, forum, ai, crawler, matching


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


@app.get("/")
def root():
    return {"message": "鸿雁平台 API", "docs": "/docs", "version": "1.0.0"}
