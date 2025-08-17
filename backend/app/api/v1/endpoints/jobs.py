from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.base import User, JobPosting
from app.schemas.schemas import JobPostingResponse, JobPostingCreate
from app.api.v1.endpoints.auth import get_current_user
from app.services.job_scraper import scrape_job_posting

router = APIRouter()


@router.post("/", response_model=JobPostingResponse)
async def create_job_posting(
    job_data: JobPostingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check if job posting already exists
    result = await db.execute(select(JobPosting).where(JobPosting.url == job_data.url))
    existing_job = result.scalar_one_or_none()
    
    if existing_job:
        return existing_job
    
    # Scrape job posting data
    try:
        scraped_data = await scrape_job_posting(job_data.url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to scrape job posting: {str(e)}"
        )
    
    # Create job posting
    job_posting = JobPosting(
        url=job_data.url,
        title=scraped_data.get("title", "Unknown Position"),
        company=scraped_data.get("company", "Unknown Company"),
        description=scraped_data.get("description", ""),
        requirements=scraped_data.get("requirements"),
        location=scraped_data.get("location"),
        salary_range=scraped_data.get("salary_range"),
        extracted_keywords=scraped_data.get("keywords", {})
    )
    
    db.add(job_posting)
    await db.commit()
    await db.refresh(job_posting)
    
    return job_posting


@router.get("/{job_id}", response_model=JobPostingResponse)
async def get_job_posting(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(JobPosting).where(JobPosting.id == job_id))
    job_posting = result.scalar_one_or_none()
    
    if not job_posting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job posting not found"
        )
    
    return job_posting


@router.get("/", response_model=List[JobPostingResponse])
async def get_job_postings(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(JobPosting).offset(skip).limit(limit)
    )
    return result.scalars().all()
