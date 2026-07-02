from fastapi import APIRouter
from model import QueryRequest
from main import query_rag

router = APIRouter()


@router.post("/ask")
async def ask(request: QueryRequest):

    result = await query_rag(
        request.question
    )

    return result