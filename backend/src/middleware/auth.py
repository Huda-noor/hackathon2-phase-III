from fastapi import Request, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from ..utils.jwt_utils import verify_token
from ..crud.user import get_user_by_email


async def jwt_auth_middleware(request: Request, call_next):
    """
    Middleware to authenticate requests using JWT tokens
    """
    # Define public endpoints that don't require authentication
    public_endpoints = ["/health", "/docs", "/redoc", "/openapi.json"]
    
    # Skip authentication for public endpoints
    if request.url.path in public_endpoints:
        return await call_next(request)
    
    # For API endpoints, check for JWT token
    if request.url.path.startswith("/api/"):
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = param
        try:
            payload = verify_token(token)
            email = payload.get("email")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Add user info to request state for use in route handlers
            request.state.user_email = email
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    response = await call_next(request)
    return response