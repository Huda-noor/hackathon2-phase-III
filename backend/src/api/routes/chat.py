from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from ..db.session import get_db
from ..models.message import Message, MessageCreate
from ..models.conversation import Conversation, ConversationCreate
from ..services.chat_service import process_chat_message
from ..services.auth_service import get_current_active_user
from ..models.user import User


router = APIRouter()


@router.post("/users/{user_id}/chat", response_model=Message)
async def chat_endpoint(
    user_id: UUID,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Process a natural language message and return AI response with potential tool calls.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's chat"
        )
    
    try:
        response = await process_chat_message(
            db=db,
            user_id=user_id,
            message_data=message_data
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.get("/users/{user_id}/conversations", response_model=List[Conversation])
async def get_user_conversations(
    user_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a list of conversations for the specified user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's conversations"
        )
    
    # Implementation would go here
    pass


@router.get("/users/{user_id}/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_conversation_messages(
    user_id: UUID,
    conversation_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve messages for a specific conversation.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's conversations"
        )
    
    # Implementation would go here
    pass