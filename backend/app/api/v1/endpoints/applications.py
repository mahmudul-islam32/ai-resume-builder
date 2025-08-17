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
    
    for field, value in application_update.model_dump(exclude_unset=True).items():
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


@router.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get all applications for the user
    result = await db.execute(
        select(Application)
        .options(selectinload(Application.job_posting))
        .where(Application.user_id == current_user.id)
    )
    applications = result.scalars().all()
    
    # Calculate stats
    total_applications = len(applications)
    applications_by_status = {}
    
    for app in applications:
        status = app.status.value
        applications_by_status[status] = applications_by_status.get(status, 0) + 1
    
    # Get recent applications (last 10)
    recent_applications = sorted(applications, key=lambda x: x.created_at, reverse=True)[:10]
    
    # Get upcoming interviews (placeholder - would need to join with interviews table)
    upcoming_interviews = []
    
    return DashboardStats(
        total_applications=total_applications,
        applications_by_status=applications_by_status,
        recent_applications=recent_applications,
        upcoming_interviews=upcoming_interviews
    )
