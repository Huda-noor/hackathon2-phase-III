import pytest
from httpx import AsyncClient
from src.api.main import app
from src.core.config import settings


@pytest.mark.asyncio
async def test_auth_integration():
    """Integration test for authentication functionality"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        # Test the health endpoint (should be publicly accessible)
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
        
        # Test that protected endpoints require authentication
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await ac.get(f"/api/v1/users/{user_id}/conversations")
        
        # Should return 401 or 403 since no auth header was provided
        assert response.status_code in [401, 403]
        
        # Test the login endpoint structure (without valid credentials)
        login_data = {
            "username": "test@example.com",
            "password": "wrongpassword"
        }
        response = await ac.post("/api/v1/login", data=login_data)
        
        # Should return 401 for invalid credentials
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_routes_require_auth():
    """Test that all protected routes require authentication"""
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        conversation_id = "11111111-e89b-12d3-a456-426614174000"
        
        # Test various protected endpoints
        protected_endpoints = [
            f"/api/v1/users/{user_id}/conversations",
            f"/api/v1/users/{user_id}/conversations/{conversation_id}/messages",
        ]
        
        for endpoint in protected_endpoints:
            response = await ac.get(endpoint)
            # Should return 401 or 403 since no auth header was provided
            assert response.status_code in [401, 403], f"Endpoint {endpoint} should require authentication"