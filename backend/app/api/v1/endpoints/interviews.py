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
    """
    Create a new interview for an application.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "application_id": 1,
        "title": "First Round Interview - Senior Software Engineer",
        "scheduled_date": "2024-01-25T14:00:00Z",
        "duration_minutes": 60,
        "interviewer_name": "Sarah Johnson",
        "interviewer_email": "sarah.johnson@techcorp.com",
        "meeting_link": "https://zoom.us/j/123456789",
        "location": "Virtual (Zoom)",
        "interview_type": "Technical Interview"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "application_id": 1,
        "title": "First Round Interview - Senior Software Engineer",
        "scheduled_date": "2024-01-25T14:00:00Z",
        "duration_minutes": 60,
        "interviewer_name": "Sarah Johnson",
        "interviewer_email": "sarah.johnson@techcorp.com",
        "meeting_link": "https://zoom.us/j/123456789",
        "location": "Virtual (Zoom)",
        "interview_type": "Technical Interview",
        "status": "scheduled",
        "feedback": null,
        "notes": null,
        "next_steps": null,
        "created_at": "2024-01-20T10:30:00Z",
        "updated_at": "2024-01-20T10:30:00Z"
    }
    ```
    """
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
    """
    Get all interviews for the current user's applications with pagination.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum number of records to return (default: 100)
    
    **Example Request:**
    ```
    GET /api/v1/interviews/?skip=0&limit=10
    ```
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "application_id": 1,
            "title": "First Round Interview - Senior Software Engineer",
            "scheduled_date": "2024-01-25T14:00:00Z",
            "duration_minutes": 60,
            "interviewer_name": "Sarah Johnson",
            "interviewer_email": "sarah.johnson@techcorp.com",
            "meeting_link": "https://zoom.us/j/123456789",
            "location": "Virtual (Zoom)",
            "interview_type": "Technical Interview",
            "status": "scheduled",
            "feedback": null,
            "notes": null,
            "next_steps": null,
            "created_at": "2024-01-20T10:30:00Z",
            "updated_at": "2024-01-20T10:30:00Z"
        },
        {
            "id": 2,
            "application_id": 2,
            "title": "Final Round Interview - Full Stack Developer",
            "scheduled_date": "2024-01-28T16:00:00Z",
            "duration_minutes": 90,
            "interviewer_name": "Mike Chen",
            "interviewer_email": "mike.chen@startupinc.com",
            "meeting_link": "https://meet.google.com/abc-defg-hij",
            "location": "Virtual (Google Meet)",
            "interview_type": "Final Round",
            "status": "scheduled",
            "feedback": null,
            "notes": "Prepare for system design questions",
            "next_steps": null,
            "created_at": "2024-01-22T14:15:00Z",
            "updated_at": "2024-01-22T14:15:00Z"
        },
        {
            "id": 3,
            "application_id": 1,
            "title": "Second Round Interview - Senior Software Engineer",
            "scheduled_date": "2024-01-30T10:00:00Z",
            "duration_minutes": 45,
            "interviewer_name": "David Wilson",
            "interviewer_email": "david.wilson@techcorp.com",
            "meeting_link": null,
            "location": "Tech Corp Office - San Francisco",
            "interview_type": "Behavioral Interview",
            "status": "scheduled",
            "feedback": null,
            "notes": "In-person interview at company office",
            "next_steps": null,
            "created_at": "2024-01-26T09:45:00Z",
            "updated_at": "2024-01-26T09:45:00Z"
        }
    ]
    ```
    """
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
    """
    Get a specific interview by ID.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `interview_id`: ID of the interview to retrieve
    
    **Example Request:**
    ```
    GET /api/v1/interviews/1
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "application_id": 1,
        "title": "First Round Interview - Senior Software Engineer",
        "scheduled_date": "2024-01-25T14:00:00Z",
        "duration_minutes": 60,
        "interviewer_name": "Sarah Johnson",
        "interviewer_email": "sarah.johnson@techcorp.com",
        "meeting_link": "https://zoom.us/j/123456789",
        "location": "Virtual (Zoom)",
        "interview_type": "Technical Interview",
        "status": "completed",
        "feedback": "Excellent technical skills and problem-solving abilities. Strong communication and team collaboration. Recommended for next round.",
        "notes": "Discussed system design, algorithms, and past projects. Interviewer was impressed with technical depth and leadership experience.",
        "next_steps": "Second round interview scheduled for January 30th with David Wilson (Engineering Manager)",
        "created_at": "2024-01-20T10:30:00Z",
        "updated_at": "2024-01-25T15:30:00Z"
    }
    ```
    """
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
    """
    Update an interview's details and status.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `interview_id`: ID of the interview to update
    
    **Example Request Body:**
    ```json
    {
        "status": "completed",
        "feedback": "Excellent technical skills and problem-solving abilities. Strong communication and team collaboration. Recommended for next round.",
        "notes": "Discussed system design, algorithms, and past projects. Interviewer was impressed with technical depth and leadership experience.",
        "next_steps": "Second round interview scheduled for January 30th with David Wilson (Engineering Manager)"
    }
    ```
    
    **Available Status Values:**
    - `scheduled`: Interview is scheduled
    - `completed`: Interview has been completed
    - `cancelled`: Interview was cancelled
    - `rescheduled`: Interview was rescheduled
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "application_id": 1,
        "title": "First Round Interview - Senior Software Engineer",
        "scheduled_date": "2024-01-25T14:00:00Z",
        "duration_minutes": 60,
        "interviewer_name": "Sarah Johnson",
        "interviewer_email": "sarah.johnson@techcorp.com",
        "meeting_link": "https://zoom.us/j/123456789",
        "location": "Virtual (Zoom)",
        "interview_type": "Technical Interview",
        "status": "completed",
        "feedback": "Excellent technical skills and problem-solving abilities. Strong communication and team collaboration. Recommended for next round.",
        "notes": "Discussed system design, algorithms, and past projects. Interviewer was impressed with technical depth and leadership experience.",
        "next_steps": "Second round interview scheduled for January 30th with David Wilson (Engineering Manager)",
        "created_at": "2024-01-20T10:30:00Z",
        "updated_at": "2024-01-25T15:30:00Z"
    }
    ```
    """
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
    
    # Update fields
    for field, value in interview_update.dict(exclude_unset=True).items():
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
    """
    Delete an interview permanently.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `interview_id`: ID of the interview to delete
    
    **Example Request:**
    ```
    DELETE /api/v1/interviews/1
    ```
    
    **Example Response:**
    ```json
    {
        "message": "Interview deleted successfully"
    }
    ```
    """
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
