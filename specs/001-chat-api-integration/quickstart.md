# Quickstart Guide: Chat API & Frontend Integration

## Overview
This guide provides a quick introduction to setting up and using the Chat API & Frontend Integration feature.

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Docker (optional, for containerized deployment)

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn src.api.main:app --reload
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## API Usage Example
Once the backend is running, you can test the chat API:

```bash
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, can you help me create a task?",
    "conversation_id": "existing_conversation_id_optional"
  }'
```

## Running Tests
### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Key Components
- **Backend**: FastAPI application handling API requests, authentication, and business logic
- **Frontend**: React application providing the chat interface
- **Database**: PostgreSQL storing conversations, messages, and user data
- **Authentication**: JWT-based authentication system

## Configuration
Key configuration options:
- `DATABASE_URL`: Connection string for PostgreSQL database
- `OPENAI_API_KEY`: API key for OpenAI services
- `JWT_SECRET`: Secret key for JWT token signing
- `MCP_TOOL_ENDPOINT`: Endpoint for MCP tool execution

## Troubleshooting
- If you get authentication errors, verify your JWT token is valid
- If database connections fail, check your PostgreSQL configuration
- For slow responses, verify your OpenAI API key has sufficient quota