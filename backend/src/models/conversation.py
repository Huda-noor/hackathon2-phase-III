from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID, uuid4
from .user import UserInDB


class ConversationBase(BaseModel):
    title: str


class ConversationCreate(ConversationBase):
    user_id: UUID


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_active: Optional[bool] = None


class ConversationInDB(ConversationBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True


class Conversation(ConversationInDB):
    user: Optional[UserInDB] = None