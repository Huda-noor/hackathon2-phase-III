import json
from typing import Dict, List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.message import Message, MessageCreate, ToolCall
from ..models.conversation import Conversation, ConversationCreate
from ..crud.message import create_message, get_messages_by_conversation
from ..crud.conversation import get_conversation, create_conversation, update_conversation
from ..utils.conversation_utils import can_add_message_to_conversation, update_conversation_title
from ..core.openai_client import get_openai_response


async def process_chat_message(
    db: AsyncSession,
    user_id: UUID,
    message_data: MessageCreate
) -> Message:
    """
    Process a chat message by sending it to the AI agent and executing any required tools.
    """
    # If a conversation_id is provided, get the existing conversation
    conversation = None
    if message_data.conversation_id:
        conversation = await get_conversation(db, message_data.conversation_id)
        
        # Verify the user owns this conversation
        if conversation and conversation.user_id != user_id:
            raise ValueError("User does not own this conversation")
        
        # Check if conversation is still active
        if conversation and not can_add_message_to_conversation(conversation):
            raise ValueError("Conversation is no longer active")
    
    # If no conversation was found or provided, create a new one
    if not conversation:
        conversation_data = ConversationCreate(
            title="",  # Will be updated after first message
            user_id=user_id
        )
        conversation = await create_conversation(db, conversation_data)
    
    # Create the user message in the database
    user_message = await create_message(
        db,
        MessageCreate(
            conversation_id=conversation.id,
            sender_type="user",
            content=message_data.content,
            tool_calls=message_data.tool_calls,
            response_metadata=message_data.response_metadata
        )
    )
    
    # Update conversation title if it's empty
    if not conversation.title:
        updated_title = update_conversation_title(conversation, message_data.content)
        await update_conversation(db, conversation.id, {"title": updated_title})
    
    # Process the message with the AI agent
    ai_response = await get_openai_response(message_data.content)
    
    # Extract any tool calls from the AI response
    tool_calls: List[ToolCall] = []
    if ai_response.get("tool_calls"):
        for tool_call in ai_response["tool_calls"]:
            # Execute the tool call
            tool_result = await execute_tool_call(tool_call)
            
            # Add the result to the tool call
            tool_call["result"] = tool_result
            tool_calls.append(ToolCall(**tool_call))
    
    # Create the AI response message in the database
    ai_message = await create_message(
        db,
        MessageCreate(
            conversation_id=conversation.id,
            sender_type="ai",
            content=ai_response["content"],
            tool_calls=tool_calls,
            is_confirmed=True  # Assuming AI responses are confirmed by default
        )
    )
    
    return ai_message


async def execute_tool_call(tool_call: Dict) -> str:
    """
    Execute a tool call and return the result.
    This is a simplified implementation - in a real system, this would
    interface with actual tools based on the tool_call specification.
    """
    tool_name = tool_call.get("tool_name")
    arguments = tool_call.get("arguments", {})
    
    # This is where you would implement actual tool execution logic
    # For now, we'll simulate a response
    if tool_name == "get_weather":
        city = arguments.get("city", "Unknown")
        return f"Weather in {city}: Sunny, 22°C"
    elif tool_name == "create_task":
        task_description = arguments.get("description", "Unknown task")
        return f"Task created: {task_description}"
    else:
        return f"Tool '{tool_name}' executed with arguments: {json.dumps(arguments)}"