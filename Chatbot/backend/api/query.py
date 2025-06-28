from fastapi import APIRouter
from schemas.query import QueryRequest, QueryResponse
from services.chatbot import handle_query

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_chatbot(request: QueryRequest):
    query = request.query
    message, data = handle_query(query)
    return QueryResponse(message=message, data=data)
