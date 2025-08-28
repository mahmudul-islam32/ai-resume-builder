from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.base import User
from app.schemas.schemas import UserResponse, UserUpdate
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """
    Get the current user's profile information.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request:**
    ```
    GET /api/v1/users/profile
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
    return current_user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update the current user's profile information.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "first_name": "Jonathan",
        "last_name": "Smith"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "email": "john.doe@example.com",
        "first_name": "Jonathan",
        "last_name": "Smith",
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    
    **Note:** Only first_name and last_name can be updated. Email cannot be changed through this endpoint.
    """
    # Update fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user
