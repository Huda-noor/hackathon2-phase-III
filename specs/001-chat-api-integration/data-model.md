# Data Model: Chat API & Frontend Integration

## Overview
This document defines the data models for the Chat API & Frontend Integration feature.

## Entity: User
Represents an authenticated user with access to the chat functionality.

**Fields:**
- `id` (UUID): Unique identifier for the user
- `email` (String): User's email address (unique)
- `name` (String): User's display name
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated
- `is_active` (Boolean): Whether the user account is active

**Validation rules:**
- Email must be a valid email format
- Name must be 1-100 characters
- Email must be unique

## Entity: Conversation
Represents a continuous dialogue between a user and the AI agent.

**Fields:**
- `id` (UUID): Unique identifier for the conversation
- `user_id` (UUID): Reference to the owning user
- `title` (String): Brief description of the conversation topic
- `created_at` (DateTime): Timestamp when conversation was started
- `updated_at` (DateTime): Timestamp when conversation was last updated
- `is_active` (Boolean): Whether the conversation is currently active

**Relationships:**
- Belongs to one User
- Has many Messages

**Validation rules:**
- Title must be 1-200 characters
- User must exist

## Entity: Message
Represents a single exchange in a conversation.

**Fields:**
- `id` (UUID): Unique identifier for the message
- `conversation_id` (UUID): Reference to the parent conversation
- `sender_type` (Enum): Either 'user' or 'ai'
- `content` (Text): The actual message content
- `tool_calls` (JSON): List of tools called in response to this message (nullable)
- `response_metadata` (JSON): Additional metadata about the AI response (nullable)
- `timestamp` (DateTime): When the message was sent/received
- `is_confirmed` (Boolean): Whether the action was confirmed as completed

**Relationships:**
- Belongs to one Conversation

**Validation rules:**
- Content must not be empty
- Sender type must be either 'user' or 'ai'
- Conversation must exist
- Tool calls must be valid JSON if present

## State Transitions

### Conversation States
- **Active**: New messages can be added to the conversation
- **Inactive**: Conversation is archived, no new messages allowed
- **Expired**: Conversation has timed out due to inactivity

Transition rules:
- Active → Inactive: When user explicitly ends the conversation
- Active → Expired: After 24 hours of inactivity
- Inactive → Active: When user resumes the conversation (within 30 days)