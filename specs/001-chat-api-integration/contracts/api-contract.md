# API Contract: Chat API & Frontend Integration

## Overview
This document specifies the API contracts for the Chat API & Frontend Integration feature.

## Base URL
`https://api.example.com`

## Authentication
All endpoints require JWT authentication in the Authorization header:
`Authorization: Bearer <jwt_token>`

## Endpoints

### POST /api/{user_id}/chat
Process a natural language message and return AI response with potential tool calls.

#### Request
**Headers:**
- `Authorization: Bearer <jwt_token>`
- `Content-Type: application/json`

**Path Parameters:**
- `user_id` (string): The ID of the authenticated user

**Body:**
```json
{
  "message": "Natural language message from user",
  "conversation_id": "Optional conversation ID to continue existing conversation"
}
```

**Request Body Schema:**
```json
{
  "type": "object",
  "properties": {
    "message": {
      "type": "string",
      "description": "The natural language message from the user",
      "example": "Please create a new task to buy groceries"
    },
    "conversation_id": {
      "type": "string",
      "description": "Optional ID of existing conversation to continue",
      "example": "abc123-def456"
    }
  },
  "required": ["message"]
}
```

#### Response
**Success Response (200 OK):**
```json
{
  "conversation_id": "unique conversation identifier",
  "message_id": "unique message identifier",
  "response": "AI-generated response to the user message",
  "tool_calls": [
    {
      "tool_name": "name of the tool called",
      "arguments": {
        "arg1": "value1",
        "arg2": "value2"
      },
      "result": "result of the tool execution (if already executed)"
    }
  ],
  "confirmation": "Confirmation message indicating successful action completion",
  "timestamp": "ISO 8601 timestamp of the response"
}
```

**Response Schema:**
```json
{
  "type": "object",
  "properties": {
    "conversation_id": {
      "type": "string",
      "description": "Unique identifier for the conversation"
    },
    "message_id": {
      "type": "string",
      "description": "Unique identifier for this message"
    },
    "response": {
      "type": "string",
      "description": "AI-generated response to the user message"
    },
    "tool_calls": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "tool_name": {
            "type": "string",
            "description": "Name of the tool that was called"
          },
          "arguments": {
            "type": "object",
            "description": "Arguments passed to the tool"
          },
          "result": {
            "type": "string",
            "description": "Result of the tool execution"
          }
        },
        "required": ["tool_name", "arguments"]
      }
    },
    "confirmation": {
      "type": "string",
      "description": "Confirmation that an action was completed"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp of the response"
    }
  },
  "required": ["conversation_id", "message_id", "response", "timestamp"]
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: User does not have permission to access this resource
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Unexpected server error

### GET /api/{user_id}/conversations
Retrieve a list of conversations for the specified user.

#### Request
**Headers:**
- `Authorization: Bearer <jwt_token>`

**Path Parameters:**
- `user_id` (string): The ID of the authenticated user

#### Response
**Success Response (200 OK):**
```json
[
  {
    "id": "conversation unique identifier",
    "title": "Brief description of the conversation topic",
    "created_at": "ISO 8601 timestamp when conversation was created",
    "updated_at": "ISO 8601 timestamp when conversation was last updated",
    "is_active": true
  }
]
```

### GET /api/{user_id}/conversations/{conversation_id}/messages
Retrieve messages for a specific conversation.

#### Request
**Headers:**
- `Authorization: Bearer <jwt_token>`

**Path Parameters:**
- `user_id` (string): The ID of the authenticated user
- `conversation_id` (string): The ID of the conversation

#### Response
**Success Response (200 OK):**
```json
[
  {
    "id": "message unique identifier",
    "sender_type": "Either 'user' or 'ai'",
    "content": "The actual message content",
    "tool_calls": [
      {
        "tool_name": "name of the tool called",
        "arguments": {
          "arg1": "value1",
          "arg2": "value2"
        },
        "result": "result of the tool execution"
      }
    ],
    "timestamp": "ISO 8601 timestamp of the message"
  }
]
```

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "code": "error_code_string",
    "message": "Human-readable error message",
    "details": "Additional error details (optional)"
  }
}
```

## Common Error Codes
- `INVALID_REQUEST`: Request format is invalid
- `AUTHENTICATION_FAILED`: JWT token is invalid or expired
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions
- `RESOURCE_NOT_FOUND`: Requested resource does not exist
- `RATE_LIMIT_EXCEEDED`: Request rate limit has been exceeded
- `INTERNAL_ERROR`: Unexpected server error occurred