from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 数据库：本地开发默认 SQLite；生产(Railway/Render/Supabase)配置 PostgreSQL，如
    # DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/hongyan
    DATABASE_URL: str = "sqlite:///./hongyan.db"

    SECRET_KEY: str = "default-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # ===== 智能匹配核心 LLM（会议决策：弃用百度千帆，采用 DeepSeek V4 Pro）=====
    DEEPSEEK_API_KEY: str = ""
    DEEPSEEK_BASE_URL: str = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL: str = "deepseek-chat"   # deepseek-chat 当前映射 DeepSeek V4 系列

    # RAG 嵌入模型（待定：等嵌入模型 API 确定后填入）
    EMBEDDING_API_KEY: str = ""
    EMBEDDING_BASE_URL: str = "https://ark.cn-beijing.volces.com/api/v3"
    EMBEDDING_MODEL: str = "doubao-embedding-vision-251215"

    CORS_ORIGINS: list[str] = ["http://localhost:5173", "https://hongyan-3kr.pages.dev"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
