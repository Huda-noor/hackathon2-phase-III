from datetime import datetime, timedelta
from enum import Enum
from typing import Optional
from uuid import UUID
from ..models.conversation import Conversation


class ConversationState(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"


def is_conversation_expired(conversation: Conversation, expiry_hours: int = 24) -> bool:
    """
    Check if a conversation has expired based on its last activity
    """
    if not conversation.updated_at:
        return False
    
    expiry_time = conversation.updated_at + timedelta(hours=expiry_hours)
    return datetime.utcnow() > expiry_time


def get_conversation_state(conversation: Conversation) -> ConversationState:
    """
    Determine the current state of a conversation
    """
    if not conversation.is_active:
        return ConversationState.INACTIVE
    
    if is_conversation_expired(conversation):
        return ConversationState.EXPIRED
    
    return ConversationState.ACTIVE


def update_conversation_title(conversation: Conversation, new_message: str, max_length: int = 50) -> str:
    """
    Generate a title for a conversation based on the first message or a summary
    """
    if conversation.title and len(conversation.title.strip()) > 0:
        return conversation.title
    
    # Take the first part of the new message as the title
    title = new_message.strip()
    if len(title) > max_length:
        title = title[:max_length].rstrip() + "..."
    
    return title


def can_add_message_to_conversation(conversation: Conversation) -> bool:
    """
    Check if a message can be added to this conversation
    """
    state = get_conversation_state(conversation)
    return state == ConversationState.ACTIVE


def archive_conversation_if_inactive(conversation: Conversation, inactivity_hours: int = 24) -> bool:
    """
    Archive a conversation if it has been inactive for the specified number of hours
    """
    if not conversation.updated_at:
        return False
    
    inactivity_threshold = datetime.utcnow() - timedelta(hours=inactivity_hours)
    return conversation.updated_at < inactivity_threshold