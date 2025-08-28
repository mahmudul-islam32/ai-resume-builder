from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.core.database import get_db
from app.models.base import User, Application, JobPosting
from app.schemas.schemas import (
    ApplicationResponse, ApplicationCreate, ApplicationUpdate, DashboardStats
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application_data: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new job application.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "job_posting_id": 1,
        "notes": "Applied through company website. Follow up in 1 week."
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "job_posting_id": 1,
        "status": "applied",
        "notes": "Applied through company website. Follow up in 1 week.",
        "applied_date": "2024-01-15T10:30:00Z",
        "cover_letter": null,
        "cover_letter_file_path": null,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "job_posting": {
            "id": 1,
            "url": "https://example.com/job/123",
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "description": "We are looking for a senior software engineer...",
            "requirements": "5+ years experience in Python, JavaScript...",
            "location": "San Francisco, CA",
            "salary_range": "$120,000 - $180,000",
            "extracted_keywords": {
                "skills": ["Python", "JavaScript", "React"],
                "technologies": ["Django", "Node.js"]
            },
            "created_at": "2024-01-10T09:00:00Z"
        }
    }
    ```
    """
    # Check if job posting exists
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == application_data.job_posting_id)
    )
    job_posting = result.scalar_one_or_none()
    
    if not job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    # Check if application already exists
    result = await db.execute(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.job_posting_id == application_data.job_posting_id
        )
    )
    existing_application = result.scalar_one_or_none()
    
    if existing_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already exists for this job posting"
        )
    
    # Create application
    application = Application(
        user_id=current_user.id,
        job_posting_id=application_data.job_posting_id,
        notes=application_data.notes
    )
    
    db.add(application)
    await db.commit()
    await db.refresh(application)
    
    # Load related data
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job_posting))
        .where(Application.id == application.id)
    )
    application_with_relations = result.scalar_one()
    
    return application_with_relations


@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all applications for the current user with pagination.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum number of records to return (default: 100)
    
    **Example Request:**
    ```
    GET /api/v1/applications/?skip=0&limit=10
    ```
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "user_id": 1,
            "job_posting_id": 1,
            "status": "applied",
            "notes": "Applied through company website",
            "applied_date": "2024-01-15T10:30:00Z",
            "cover_letter": null,
            "cover_letter_file_path": null,
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "job_posting": {
                "id": 1,
                "url": "https://example.com/job/123",
                "title": "Senior Software Engineer",
                "company": "Tech Corp",
                "description": "We are looking for a senior software engineer...",
                "requirements": "5+ years experience in Python, JavaScript...",
                "location": "San Francisco, CA",
                "salary_range": "$120,000 - $180,000",
                "extracted_keywords": {
                    "skills": ["Python", "JavaScript", "React"]
                },
                "created_at": "2024-01-10T09:00:00Z"
            }
        },
        {
            "id": 2,
            "user_id": 1,
            "job_posting_id": 2,
            "status": "interviewing",
            "notes": "First interview scheduled for next week",
            "applied_date": "2024-01-10T14:20:00Z",
            "cover_letter": "Dear Hiring Manager...",
            "cover_letter_file_path": "/uploads/cover_letter_2.pdf",
            "created_at": "2024-01-10T14:20:00Z",
            "updated_at": "2024-01-12T16:45:00Z",
            "job_posting": {
                "id": 2,
                "url": "https://example.com/job/456",
                "title": "Full Stack Developer",
                "company": "Startup Inc",
                "description": "Join our growing team...",
                "requirements": "3+ years experience in web development...",
                "location": "Remote",
                "salary_range": "$90,000 - $130,000",
                "extracted_keywords": {
                    "skills": ["React", "Node.js", "MongoDB"]
                },
                "created_at": "2024-01-08T11:30:00Z"
            }
        }
    ]
    ```
    """
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job_posting))
        .where(Application.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific application by ID.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `application_id`: ID of the application to retrieve
    
    **Example Request:**
    ```
    GET /api/v1/applications/1
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "job_posting_id": 1,
        "status": "applied",
        "notes": "Applied through company website. Follow up in 1 week.",
        "applied_date": "2024-01-15T10:30:00Z",
        "cover_letter": "Dear Hiring Manager,\n\nI am writing to express my interest...",
        "cover_letter_file_path": "/uploads/cover_letter_1.pdf",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "job_posting": {
            "id": 1,
            "url": "https://example.com/job/123",
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "description": "We are looking for a senior software engineer with expertise in Python and JavaScript...",
            "requirements": "5+ years experience in Python, JavaScript, React. Experience with Django and Node.js preferred.",
            "location": "San Francisco, CA",
            "salary_range": "$120,000 - $180,000",
            "extracted_keywords": {
                "skills": ["Python", "JavaScript", "React", "Django", "Node.js"],
                "experience_level": "senior",
                "location": "San Francisco"
            },
            "created_at": "2024-01-10T09:00:00Z"
        }
    }
    ```
    """
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job_posting))
        .where(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    return application


@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update an application's status and notes.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `application_id`: ID of the application to update
    
    **Example Request Body:**
    ```json
    {
        "status": "interviewing",
        "notes": "First interview completed. Second interview scheduled for next week."
    }
    ```
    
    **Available Status Values:**
    - `applied`: Initial application submitted
    - `interviewing`: In interview process
    - `offer`: Job offer received
    - `rejected`: Application rejected
    - `withdrawn`: Application withdrawn
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "job_posting_id": 1,
        "status": "interviewing",
        "notes": "First interview completed. Second interview scheduled for next week.",
        "applied_date": "2024-01-15T10:30:00Z",
        "cover_letter": "Dear Hiring Manager...",
        "cover_letter_file_path": "/uploads/cover_letter_1.pdf",
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-20T16:30:00Z",
        "job_posting": {
            "id": 1,
            "url": "https://example.com/job/123",
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "description": "We are looking for a senior software engineer...",
            "requirements": "5+ years experience in Python, JavaScript...",
            "location": "San Francisco, CA",
            "salary_range": "$120,000 - $180,000",
            "extracted_keywords": {
                "skills": ["Python", "JavaScript", "React"]
            },
            "created_at": "2024-01-10T09:00:00Z"
        }
    }
    ```
    """
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    # Update fields
    for field, value in application_update.dict(exclude_unset=True).items():
        setattr(application, field, value)
    
    await db.commit()
    await db.refresh(application)
    
    # Load related data
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job_posting))
        .where(Application.id == application.id)
    )
    application_with_relations = result.scalar_one()
    
    return application_with_relations


@router.delete("/{application_id}")
async def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete an application permanently.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `application_id`: ID of the application to delete
    
    **Example Request:**
    ```
    DELETE /api/v1/applications/1
    ```
    
    **Example Response:**
    ```json
    {
        "message": "Application deleted successfully"
    }
    ```
    """
    result = await db.execute(
        select(Application).where(
            Application.id == application_id,
            Application.user_id == current_user.id
        )
    )
    application = result.scalar_one_or_none()
    
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    
    await db.delete(application)
    await db.commit()
    
    return {"message": "Application deleted successfully"}


@router.get("/stats/dashboard", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get dashboard statistics for the current user's applications.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request:**
    ```
    GET /api/v1/applications/stats/dashboard
    ```
    
    **Example Response:**
    ```json
    {
        "total_applications": 15,
        "applied_count": 8,
        "interviewing_count": 4,
        "rejected_count": 2,
        "accepted_count": 1
    }
    ```
    """
    # Get total applications
    result = await db.execute(
        select(Application).where(Application.user_id == current_user.id)
    )
    total_applications = len(result.scalars().all())
    
    # Get applications by status
    result = await db.execute(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.status == "applied"
        )
    )
    applied_count = len(result.scalars().all())
    
    result = await db.execute(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.status == "interviewing"
        )
    )
    interviewing_count = len(result.scalars().all())
    
    result = await db.execute(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.status == "rejected"
        )
    )
    rejected_count = len(result.scalars().all())
    
    result = await db.execute(
        select(Application).where(
            Application.user_id == current_user.id,
            Application.status == "accepted"
        )
    )
    accepted_count = len(result.scalars().all())
    
    return DashboardStats(
        total_applications=total_applications,
        applied_count=applied_count,
        interviewing_count=interviewing_count,
        rejected_count=rejected_count,
        accepted_count=accepted_count
    )
