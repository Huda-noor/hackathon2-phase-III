# Quickstart: AI Chat Backend & Data Models

**Feature**: 001-chat-data-models
**Created**: 2026-02-06

## Prerequisites

- Python 3.11 or higher
- Neon Serverless PostgreSQL database (connection string required)
- Better Auth JWT secret (for authentication)

## Setup

### 1. Environment Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install in editable mode
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt
```

**Key Dependencies**:
- fastapi>=0.104.0
- sqlmodel>=0.0.14
- alembic>=1.13.0
- asyncpg>=0.29.0
- pydantic>=2.5.0
- pytest>=7.4.0
- pytest-asyncio>=0.21.0

### 3. Configure Environment

Create `.env` file in backend directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@your-neon-host/dbname

# Authentication
JWT_SECRET=your-jwt-secret-from-better-auth
JWT_ALGORITHM=HS256

# Application
DEBUG=True
LOG_LEVEL=INFO
```

### 4. Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Run migrations
alembic upgrade head
```

### 5. Start Development Server

```bash
# Run with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server runs at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/integration/test_tasks.py

# Run with verbose output
pytest -v
```

## API Endpoints

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks` - List user's tasks (with pagination)
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Conversations
- `POST /api/conversations` - Create conversation
- `GET /api/conversations` - List user's conversations
- `GET /api/conversations/{id}` - Get specific conversation
- `PUT /api/conversations/{id}` - Update conversation title
- `DELETE /api/conversations/{id}` - Delete conversation (cascades to messages)

### Messages
- `POST /api/messages` - Create message in conversation
- `GET /api/conversations/{id}/messages` - List messages in conversation

## Authentication

All endpoints require Bearer token authentication:

```bash
# Example request with auth
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8000/api/tasks
```

JWT token must contain `sub` claim with user ID.

## Database Migrations

```bash
# Create new migration after model changes
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one version
alembic downgrade -1

# Show current version
alembic current
```

## Troubleshooting

**Database Connection Errors**:
- Verify DATABASE_URL in .env
- Check Neon database is running
- Ensure asyncpg driver installed

**Authentication Errors**:
- Verify JWT_SECRET matches Better Auth configuration
- Check token expiration
- Ensure Bearer token format: `Authorization: Bearer <token>`

**Migration Errors**:
- Run `alembic upgrade head` before starting server
- Check alembic.ini database URL matches .env

## Next Steps

1. Review API documentation at `/docs`
2. Run integration tests to verify setup
3. Create sample data for testing
4. Review [data-model.md](data-model.md) for entity schemas
5. Review [contracts/](contracts/) for API specifications
