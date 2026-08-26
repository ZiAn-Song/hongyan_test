from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ai import ChatRequest, IndexResponse, SearchResponse
from app.services.ai_service import stream_ai_chat
from app.services.rag_service import index_all, search, get_context, clear_index
from app.utils.dependencies import get_current_user, CurrentUser

router = APIRouter()


@router.post("/chat")
async def chat(
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    context = ""
    if data.use_rag:
        context = get_context(db, data.message)

    async def stream():
        async for chunk in stream_ai_chat(data.message, context):
            yield chunk

    return StreamingResponse(stream(), media_type="text/event-stream")


@router.post("/index", response_model=IndexResponse)
def index_content(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    return index_all(db)


@router.get("/search", response_model=SearchResponse)
def search_content(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    top_k: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
):
    results = search(db, q, top_k)
    return {"query": q, "results": results}


@router.delete("/index")
def clear_index_endpoint(
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    count = clear_index(db)
    return {"message": f"已清除 {count} 个文本分块"}
