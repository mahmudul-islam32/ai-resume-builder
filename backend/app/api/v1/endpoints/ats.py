from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import logging

from app.core.database import get_db
from app.models.base import User, Resume, JobPosting
from app.schemas.schemas import AtsScoreRequest, AtsScoreResponse
from app.api.v1.endpoints.auth import get_current_user
try:
    from app.services.ats_service import AtsService
    ATS_SERVICE_AVAILABLE = True
except ImportError:
    from app.services.ats_service_simple import AtsServiceSimple as AtsService
    ATS_SERVICE_AVAILABLE = False
    print("Warning: Using simplified ATS service (spaCy not available)")

router = APIRouter()


# Set up logging
logger = logging.getLogger(__name__)

@router.post("/test-score", response_model=AtsScoreResponse)
async def test_score_resume(request: AtsScoreRequest):
    """
    Test endpoint for ATS scoring without authentication.
    
    **No authentication required** - This endpoint is for testing purposes.
    
    **Example Request Body:**
    ```json
    {
        "resume_text": "John Doe\nSoftware Engineer\n\nEXPERIENCE\nSoftware Engineer at Tech Corp (2020-2023)\n- Developed web applications using Python and JavaScript\n- Led team of 3 developers\n- Improved application performance by 40%\n\nSKILLS\nPython, JavaScript, React, Django, Node.js, SQL, Git",
        "job_description": "We are looking for a Senior Software Engineer with 5+ years of experience in Python and JavaScript. The ideal candidate should have experience with React, Django, and Node.js. Responsibilities include developing web applications, leading development teams, and optimizing application performance.",
        "job_title": "Senior Software Engineer"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "overall_score": 85.5,
        "keyword_score": 90.0,
        "semantic_score": 82.0,
        "format_score": 88.0,
        "experience_score": 85.0,
        "keyword_analysis": {
            "matched_keywords": ["Python", "JavaScript", "React", "Django", "Node.js", "web applications"],
            "missing_keywords": ["5+ years", "senior", "leading teams"],
            "keyword_match_percentage": 75.0
        },
        "semantic_analysis": {
            "semantic_similarity": 0.82,
            "relevant_experience": "High",
            "skill_alignment": "Good"
        },
        "format_analysis": {
            "format_score": 88.0,
            "structure_quality": "Good",
            "readability": "Excellent",
            "suggestions": ["Add more quantifiable achievements", "Include certifications section"]
        },
        "experience_analysis": {
            "experience_level": "Mid-level",
            "years_experience": 3,
            "leadership_experience": "Yes",
            "relevant_projects": "High"
        },
        "suggestions": [
            "Add more senior-level responsibilities",
            "Include quantifiable achievements",
            "Add certifications section",
            "Highlight leadership experience more prominently"
        ],
        "improvements": {
            "keyword_optimization": "Add more senior-level keywords",
            "experience_enhancement": "Quantify achievements with metrics",
            "format_improvements": "Add certifications and awards section"
        },
        "confidence": 0.92
    }
    ```
    """
    
    # Debug logging
    logger.info(f"Test ATS scoring request received")
    logger.info(f"Request data: resume_id={request.resume_id}, resume_text_length={len(request.resume_text) if request.resume_text else 0}")
    logger.info(f"Job data: job_posting_id={request.job_posting_id}, job_description_length={len(request.job_description) if request.job_description else 0}")
    
    # Validate input
    resume_text = request.resume_text
    if not resume_text:
        logger.error("No resume text provided")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text is required"
        )
    
    job_description = request.job_description
    job_title = request.job_title or ""
    
    if not job_description:
        logger.error("No job description provided")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is required"
        )
    
    logger.info(f"Processing ATS score with resume_text_length={len(resume_text)}, job_description_length={len(job_description)}")
    
    # Use ATS service to compute score
    ats_service = AtsService()
    try:
        ats_result = ats_service.compute_ats_score(resume_text, job_description, job_title)
        logger.info(f"ATS scoring completed successfully with overall_score={ats_result.overall_score}")
    except Exception as e:
        logger.error(f"ATS scoring error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ATS scoring error: {str(e)}"
        )
    
    return AtsScoreResponse(
        overall_score=ats_result.overall_score,
        keyword_score=ats_result.keyword_score,
        semantic_score=ats_result.semantic_score,
        format_score=ats_result.format_score,
        experience_score=ats_result.experience_score,
        keyword_analysis=ats_result.keyword_analysis,
        semantic_analysis=ats_result.semantic_analysis,
        format_analysis=ats_result.format_analysis,
        experience_analysis=ats_result.experience_analysis,
        suggestions=ats_result.suggestions,
        improvements=ats_result.improvements,
        confidence=ats_result.confidence
    )


@router.post("/score-resume", response_model=AtsScoreResponse)
async def score_resume(
    request: AtsScoreRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Score a resume against a job description using professional ATS algorithms.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body (using resume_id and job_posting_id):**
    ```json
    {
        "resume_id": 1,
        "job_posting_id": 1
    }
    ```
    
    **Example Request Body (using direct text):**
    ```json
    {
        "resume_text": "John Doe\nSoftware Engineer\n\nEXPERIENCE\nSoftware Engineer at Tech Corp (2020-2023)\n- Developed web applications using Python and JavaScript\n- Led team of 3 developers\n- Improved application performance by 40%\n\nSKILLS\nPython, JavaScript, React, Django, Node.js, SQL, Git",
        "job_description": "We are looking for a Senior Software Engineer with 5+ years of experience in Python and JavaScript. The ideal candidate should have experience with React, Django, and Node.js. Responsibilities include developing web applications, leading development teams, and optimizing application performance.",
        "job_title": "Senior Software Engineer"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "overall_score": 85.5,
        "keyword_score": 90.0,
        "semantic_score": 82.0,
        "format_score": 88.0,
        "experience_score": 85.0,
        "keyword_analysis": {
            "matched_keywords": ["Python", "JavaScript", "React", "Django", "Node.js", "web applications"],
            "missing_keywords": ["5+ years", "senior", "leading teams"],
            "keyword_match_percentage": 75.0,
            "keyword_density": {
                "Python": 0.8,
                "JavaScript": 0.6,
                "React": 0.4
            }
        },
        "semantic_analysis": {
            "semantic_similarity": 0.82,
            "relevant_experience": "High",
            "skill_alignment": "Good",
            "context_matching": 0.78
        },
        "format_analysis": {
            "format_score": 88.0,
            "structure_quality": "Good",
            "readability": "Excellent",
            "ats_compatibility": "High",
            "suggestions": ["Add more quantifiable achievements", "Include certifications section"]
        },
        "experience_analysis": {
            "experience_level": "Mid-level",
            "years_experience": 3,
            "leadership_experience": "Yes",
            "relevant_projects": "High",
            "achievement_metrics": "Good"
        },
        "suggestions": [
            "Add more senior-level responsibilities",
            "Include quantifiable achievements",
            "Add certifications section",
            "Highlight leadership experience more prominently"
        ],
        "improvements": {
            "keyword_optimization": "Add more senior-level keywords",
            "experience_enhancement": "Quantify achievements with metrics",
            "format_improvements": "Add certifications and awards section",
            "content_enhancement": "Include more leadership examples"
        },
        "confidence": 0.92
    }
    ```
    """
    
    # Get resume if resume_id is provided
    resume_text = request.resume_text
    if request.resume_id:
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
        
        resume_text = resume.parsed_content or ""
    
    if not resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text is required"
        )
    
    # Get job posting if job_posting_id is provided
    job_description = request.job_description
    job_title = request.job_title or ""
    
    if request.job_posting_id:
        result = await db.execute(
            select(JobPosting).where(JobPosting.id == request.job_posting_id)
        )
        job_posting = result.scalar_one_or_none()
        
        if not job_posting:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job posting not found"
            )
        
        job_description = job_posting.description
        job_title = job_posting.title
    
    if not job_description:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description is required"
        )
    
    # Use ATS service to compute score
    ats_service = AtsService()
    try:
        ats_result = ats_service.compute_ats_score(resume_text, job_description, job_title)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ATS scoring error: {str(e)}"
        )
    
    return AtsScoreResponse(
        overall_score=ats_result.overall_score,
        keyword_score=ats_result.keyword_score,
        semantic_score=ats_result.semantic_score,
        format_score=ats_result.format_score,
        experience_score=ats_result.experience_score,
        keyword_analysis=ats_result.keyword_analysis,
        semantic_analysis=ats_result.semantic_analysis,
        format_analysis=ats_result.format_analysis,
        experience_analysis=ats_result.experience_analysis,
        suggestions=ats_result.suggestions,
        improvements=ats_result.improvements,
        confidence=ats_result.confidence
    )


@router.post("/analyze-resume", response_model=AtsScoreResponse)
async def analyze_resume_only(
    request: AtsScoreRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze a resume for ATS compatibility without job matching.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body (using resume_id):**
    ```json
    {
        "resume_id": 1
    }
    ```
    
    **Example Request Body (using direct text):**
    ```json
    {
        "resume_text": "John Doe\nSoftware Engineer\n\nEXPERIENCE\nSoftware Engineer at Tech Corp (2020-2023)\n- Developed web applications using Python and JavaScript\n- Led team of 3 developers\n- Improved application performance by 40%\n\nSKILLS\nPython, JavaScript, React, Django, Node.js, SQL, Git"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "overall_score": 78.0,
        "keyword_score": 75.0,
        "semantic_score": 80.0,
        "format_score": 85.0,
        "experience_score": 75.0,
        "keyword_analysis": {
            "keyword_diversity": "Good",
            "keyword_density": "Balanced",
            "technical_skills": ["Python", "JavaScript", "React", "Django", "Node.js"],
            "soft_skills": ["Leadership", "Team Management"]
        },
        "semantic_analysis": {
            "content_quality": "High",
            "professional_tone": "Excellent",
            "achievement_focus": "Good"
        },
        "format_analysis": {
            "format_score": 85.0,
            "structure_quality": "Good",
            "readability": "Excellent",
            "ats_compatibility": "High",
            "suggestions": ["Add certifications section", "Include more quantifiable achievements"]
        },
        "experience_analysis": {
            "experience_level": "Mid-level",
            "years_experience": 3,
            "achievement_metrics": "Good",
            "leadership_experience": "Yes"
        },
        "suggestions": [
            "Add certifications section",
            "Include more quantifiable achievements",
            "Add professional summary",
            "Include relevant projects section"
        ],
        "improvements": {
            "format_improvements": "Add certifications and awards section",
            "content_enhancement": "Include more quantifiable achievements",
            "structure_improvements": "Add professional summary section"
        },
        "confidence": 0.88
    }
    ```
    """
    
    # Get resume if resume_id is provided
    resume_text = request.resume_text
    if request.resume_id:
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
        
        resume_text = resume.parsed_content or ""
    
    if not resume_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text is required"
        )
    
    # Use ATS service to analyze resume format and structure
    ats_service = AtsService()
    try:
        # Create a generic job description for format analysis
        generic_jd = "Software Engineer with experience in programming, development, and technical skills."
        ats_result = ats_service.compute_ats_score(resume_text, generic_jd, "")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Resume analysis error: {str(e)}"
        )
    
    return AtsScoreResponse(
        overall_score=ats_result.overall_score,
        keyword_score=ats_result.keyword_score,
        semantic_score=ats_result.semantic_score,
        format_score=ats_result.format_score,
        experience_score=ats_result.experience_score,
        keyword_analysis=ats_result.keyword_analysis,
        semantic_analysis=ats_result.semantic_analysis,
        format_analysis=ats_result.format_analysis,
        experience_analysis=ats_result.experience_analysis,
        suggestions=ats_result.suggestions,
        improvements=ats_result.improvements,
        confidence=ats_result.confidence
    )
