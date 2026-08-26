from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="用户消息")
    use_rag: bool = Field(False, description="是否启用 RAG 上下文增强")


class IndexResponse(BaseModel):
    indexed: int
    sources: dict
    message: str


class SearchResult(BaseModel):
    content: str
    source_type: str
    source_id: int
    score: float


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
