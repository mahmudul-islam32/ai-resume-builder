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
    """
    Create a new job posting by scraping data from a job URL.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "url": "https://www.linkedin.com/jobs/view/123456789"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "url": "https://www.linkedin.com/jobs/view/123456789",
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "description": "We are looking for a Senior Software Engineer to join our growing team. You will be responsible for developing scalable web applications, leading development teams, and driving technical excellence.\n\nResponsibilities:\n- Develop and maintain web applications using Python, JavaScript, and React\n- Lead development teams and mentor junior developers\n- Optimize application performance and implement best practices\n- Collaborate with cross-functional teams to deliver high-quality solutions\n\nRequirements:\n- 5+ years of experience in software development\n- Strong proficiency in Python, JavaScript, and React\n- Experience with Django, Node.js, and modern web technologies\n- Leadership experience and ability to mentor team members\n- Excellent problem-solving and communication skills",
        "requirements": "5+ years of experience in software development\nStrong proficiency in Python, JavaScript, and React\nExperience with Django, Node.js, and modern web technologies\nLeadership experience and ability to mentor team members\nExcellent problem-solving and communication skills",
        "location": "San Francisco, CA",
        "salary_range": "$120,000 - $180,000",
        "extracted_keywords": {
            "skills": ["Python", "JavaScript", "React", "Django", "Node.js"],
            "technologies": ["Web Development", "Scalable Applications"],
            "experience_level": "Senior",
            "location": "San Francisco",
            "salary_range": "120000-180000"
        },
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
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
    """
    Get a specific job posting by ID.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `job_id`: ID of the job posting to retrieve
    
    **Example Request:**
    ```
    GET /api/v1/jobs/1
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "url": "https://www.linkedin.com/jobs/view/123456789",
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "description": "We are looking for a Senior Software Engineer to join our growing team. You will be responsible for developing scalable web applications, leading development teams, and driving technical excellence.\n\nResponsibilities:\n- Develop and maintain web applications using Python, JavaScript, and React\n- Lead development teams and mentor junior developers\n- Optimize application performance and implement best practices\n- Collaborate with cross-functional teams to deliver high-quality solutions\n\nRequirements:\n- 5+ years of experience in software development\n- Strong proficiency in Python, JavaScript, and React\n- Experience with Django, Node.js, and modern web technologies\n- Leadership experience and ability to mentor team members\n- Excellent problem-solving and communication skills",
        "requirements": "5+ years of experience in software development\nStrong proficiency in Python, JavaScript, and React\nExperience with Django, Node.js, and modern web technologies\nLeadership experience and ability to mentor team members\nExcellent problem-solving and communication skills",
        "location": "San Francisco, CA",
        "salary_range": "$120,000 - $180,000",
        "extracted_keywords": {
            "skills": ["Python", "JavaScript", "React", "Django", "Node.js"],
            "technologies": ["Web Development", "Scalable Applications"],
            "experience_level": "Senior",
            "location": "San Francisco",
            "salary_range": "120000-180000",
            "responsibilities": ["Team Leadership", "Mentoring", "Performance Optimization"],
            "soft_skills": ["Problem Solving", "Communication", "Collaboration"]
        },
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
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
    """
    Get all job postings with pagination.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum number of records to return (default: 100)
    
    **Example Request:**
    ```
    GET /api/v1/jobs/?skip=0&limit=10
    ```
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "url": "https://www.linkedin.com/jobs/view/123456789",
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "description": "We are looking for a Senior Software Engineer to join our growing team...",
            "requirements": "5+ years of experience in software development...",
            "location": "San Francisco, CA",
            "salary_range": "$120,000 - $180,000",
            "extracted_keywords": {
                "skills": ["Python", "JavaScript", "React"],
                "experience_level": "Senior"
            },
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "url": "https://www.indeed.com/jobs/view/987654321",
            "title": "Full Stack Developer",
            "company": "Startup Inc",
            "description": "Join our growing startup as a Full Stack Developer...",
            "requirements": "3+ years of experience in web development...",
            "location": "Remote",
            "salary_range": "$90,000 - $130,000",
            "extracted_keywords": {
                "skills": ["React", "Node.js", "MongoDB"],
                "experience_level": "Mid-level"
            },
            "created_at": "2024-01-16T14:20:00Z"
        },
        {
            "id": 3,
            "url": "https://www.glassdoor.com/jobs/view/456789123",
            "title": "Frontend Developer",
            "company": "Design Studio",
            "description": "We are seeking a creative Frontend Developer...",
            "requirements": "2+ years of experience in frontend development...",
            "location": "New York, NY",
            "salary_range": "$80,000 - $110,000",
            "extracted_keywords": {
                "skills": ["React", "TypeScript", "CSS"],
                "experience_level": "Junior"
            },
            "created_at": "2024-01-17T09:15:00Z"
        }
    ]
    ```
    """
    result = await db.execute(
        select(JobPosting).offset(skip).limit(limit)
    )
    return result.scalars().all()
