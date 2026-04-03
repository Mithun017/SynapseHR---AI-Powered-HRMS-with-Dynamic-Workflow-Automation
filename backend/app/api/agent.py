from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.agents.agent_controller import handle_chat
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: int
    role: str
    session_id: str = None

class ChatResponse(BaseModel):
    intent: str
    confidence: float
    reasoning: str
    clarification_needed: bool
    ui: dict = None

import traceback

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    
    try:
        response_data = handle_chat(
            session_id=session_id,
            user_id=request.user_id,
            user_role=request.role,
            message=request.message
        )
        return ChatResponse(**response_data)
    except Exception as e:
        print("--- CRITICAL CHAT ENDPOINT ERROR ---")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
