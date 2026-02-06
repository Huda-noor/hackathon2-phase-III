from datetime import timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.session import get_db
from ..models.user import UserInDB
from ..utils.jwt_utils import verify_token, create_access_token
from ..core.security import verify_password
from ..crud.user import get_user_by_email


security = HTTPBearer()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    """
    Authenticate a user by email and password
    """
    user = await get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_user_token(user: UserInDB) -> str:
    """
    Create an access token for a user
    """
    access_token_expires = timedelta(minutes=30)  # Default expiration
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email}, 
        expires_delta=access_token_expires
    )
    return access_token


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the current user based on the JWT token
    """
    token = credentials.credentials
    payload = verify_token(token)
    email: str = payload.get("email")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = await get_user_by_email(db, email=email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    """
    Get the current active user
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user