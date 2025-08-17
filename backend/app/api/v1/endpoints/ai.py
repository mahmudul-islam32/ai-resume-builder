from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.base import User, Resume, JobPosting, TailoredResume
from app.schemas.schemas import (
    AITailorRequest, AICoverLetterRequest, AIResponse, 
    TailoredResumeResponse
)
from app.api.v1.endpoints.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/tailor-resume", response_model=TailoredResumeResponse)
async def tailor_resume(
    request: AITailorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get resume
    result = await db.execute(
        select(Resume).where(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
            Resume.is_active == True
        )
    )
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Get job posting
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == request.job_posting_id)
    )
    job_posting = result.scalar_one_or_none()
    
    if not job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    # Check if tailored resume already exists
    result = await db.execute(
        select(TailoredResume).where(
            TailoredResume.original_resume_id == request.resume_id,
            TailoredResume.job_posting_id == request.job_posting_id
        )
    )
    existing_tailored = result.scalar_one_or_none()
    
    if existing_tailored:
        return existing_tailored
    
    # Use AI service to tailor resume
    ai_service = AIService()
    try:
        tailored_content, suggestions, changes = await ai_service.tailor_resume(
            resume.parsed_content,
            job_posting.description,
            job_posting.requirements or ""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
    
    # Create tailored resume record
    tailored_resume = TailoredResume(
        original_resume_id=request.resume_id,
        job_posting_id=request.job_posting_id,
        tailored_content=tailored_content,
        suggestions=suggestions,
        changes_made=changes
    )
    
    db.add(tailored_resume)
    await db.commit()
    await db.refresh(tailored_resume)
    
    return tailored_resume


@router.post("/generate-cover-letter", response_model=AIResponse)
async def generate_cover_letter(
    request: AICoverLetterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get resume
    result = await db.execute(
        select(Resume).where(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id,
            Resume.is_active == True
        )
    )
    resume = result.scalar_one_or_none()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Get job posting
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == request.job_posting_id)
    )
    job_posting = result.scalar_one_or_none()
    
    if not job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    # Use AI service to generate cover letter
    ai_service = AIService()
    try:
        cover_letter = await ai_service.generate_cover_letter(
            resume.parsed_content,
            job_posting.description,
            job_posting.company,
            job_posting.title,
            f"{current_user.first_name} {current_user.last_name}",
            request.additional_info
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
    
    return AIResponse(content=cover_letter)


@router.get("/tailored-resumes", response_model=List[TailoredResumeResponse])
async def get_tailored_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(TailoredResume)
        .join(Resume)
        .where(Resume.user_id == current_user.id)
    )
    return result.scalars().all()
