from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.base import User, Interview, Application
from app.schemas.schemas import InterviewResponse, InterviewCreate, InterviewUpdate
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=InterviewResponse)
async def create_interview(
    interview_data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if application exists and belongs to user
    result = await db.execute(
        select(Application).where(
            Application.id == interview_data.application_id,
            Application.user_id == current_user.id
        )
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Create interview
    interview = Interview(
        application_id=interview_data.application_id,
        title=interview_data.title,
        scheduled_date=interview_data.scheduled_date,
        duration_minutes=interview_data.duration_minutes,
        interviewer_name=interview_data.interviewer_name,
        interviewer_email=interview_data.interviewer_email,
        meeting_link=interview_data.meeting_link,
        location=interview_data.location,
        interview_type=interview_data.interview_type
    )
    
    db.add(interview)
    await db.commit()
    await db.refresh(interview)
    
    return interview


@router.get("/", response_model=List[InterviewResponse])
async def get_interviews(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get interviews for user's applications
    result = await db.execute(
        select(Interview)
        .join(Application)
        .where(Application.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{interview_id}", response_model=InterviewResponse)
async def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Interview)
        .join(Application)
        .where(
            Interview.id == interview_id,
            Application.user_id == current_user.id
        )
    )
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    return interview


@router.put("/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: int,
    interview_update: InterviewUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Interview)
        .join(Application)
        .where(
            Interview.id == interview_id,
            Application.user_id == current_user.id
        )
    )
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    for field, value in interview_update.model_dump(exclude_unset=True).items():
        setattr(interview, field, value)
    
    await db.commit()
    await db.refresh(interview)
    return interview


@router.delete("/{interview_id}")
async def delete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Interview)
        .join(Application)
        .where(
            Interview.id == interview_id,
            Application.user_id == current_user.id
        )
    )
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    await db.delete(interview)
    await db.commit()
    
    return {"message": "Interview deleted successfully"}
