from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


class GenerateTextRequest(BaseModel):
    prompt: str
    model: str | None = None
    temperature: float = 0.7
    max_tokens: int = 2000


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    model: str | None = None
    temperature: float = 0.7


class GenerateTextResponse(BaseModel):
    text: str
    model: str
    tokens_used: int | None = None


class ChatResponse(BaseModel):
    message: str
    model: str


@router.post("/generate-text", response_model=GenerateTextResponse)
async def generate_text(
    request: GenerateTextRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate text using AI"""
    try:
        text = await ai_service.generate_text(
            prompt=request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return GenerateTextResponse(
            text=text,
            model=request.model or ai_service.config.default_model,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Chat with AI"""
    try:
        message_list = [msg.model_dump() for msg in request.messages]
        response = await ai_service.chat(
            messages=message_list,
            model=request.model,
            temperature=request.temperature,
        )
        return ChatResponse(
            message=response,
            model=request.model or ai_service.config.default_model,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
