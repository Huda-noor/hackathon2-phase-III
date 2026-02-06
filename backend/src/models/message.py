from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID
from .conversation import ConversationInDB


class SenderType(str, Enum):
    user = "user"
    ai = "ai"


class ToolCall(BaseModel):
    tool_name: str
    arguments: Dict[str, str]
    result: Optional[str] = None


class MessageBase(BaseModel):
    conversation_id: UUID
    sender_type: SenderType
    content: str
    tool_calls: Optional[List[ToolCall]] = None
    response_metadata: Optional[Dict] = None
    is_confirmed: Optional[bool] = False


class MessageCreate(MessageBase):
    pass


class MessageUpdate(BaseModel):
    content: Optional[str] = None
    is_confirmed: Optional[bool] = None


class MessageInDB(MessageBase):
    id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True


class Message(MessageInDB):
    conversation: Optional[ConversationInDB] = None