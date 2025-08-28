from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.core.database import get_db
from app.models.base import User, Resume, JobPosting, TailoredResume
from app.schemas.schemas import (
    AITailorRequest, AICoverLetterRequest, AIResponse, 
    TailoredResumeResponse, ModelConfigRequest, ModelConfigResponse
)
from app.api.v1.endpoints.auth import get_current_user
from app.services.ai_service import AIService
from app.services.model_factory import ModelFactory
from app.core.config import settings

router = APIRouter()


@router.post("/tailor-resume", response_model=TailoredResumeResponse)
async def tailor_resume(
    request: AITailorRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Tailor a resume to match a specific job posting using AI.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "resume_id": 1,
        "job_posting_id": 1
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "original_resume_id": 1,
        "job_posting_id": 1,
        "tailored_content": "John Doe\nSenior Software Engineer\n\nPROFESSIONAL SUMMARY\nResults-driven Senior Software Engineer with 5+ years of experience developing scalable web applications using Python, JavaScript, and React. Proven track record of leading development teams and delivering high-impact solutions that improve application performance by 40%.\n\nEXPERIENCE\nSenior Software Engineer at Tech Corp (2020-2023)\n- Led development of enterprise web applications using Python, Django, and React\n- Managed team of 3 developers, improving project delivery time by 25%\n- Optimized application performance resulting in 40% improvement in load times\n- Implemented CI/CD pipelines reducing deployment time by 60%\n\nSKILLS\nProgramming Languages: Python, JavaScript, TypeScript\nFrameworks: Django, React, Node.js, Express\nDatabases: PostgreSQL, MongoDB, Redis\nTools: Git, Docker, AWS, Jenkins\nLeadership: Team Management, Agile Methodologies, Technical Mentoring",
        "suggestions": {
            "keyword_optimization": "Added senior-level keywords and quantifiable achievements",
            "experience_enhancement": "Emphasized leadership and team management experience",
            "skill_alignment": "Reorganized skills to match job requirements"
        },
        "changes_made": {
            "title_update": "Software Engineer → Senior Software Engineer",
            "summary_added": "Added professional summary highlighting senior-level experience",
            "achievements_enhanced": "Added quantifiable metrics to experience descriptions",
            "skills_reorganized": "Grouped skills by category and added leadership skills"
        },
        "file_path": "/uploads/tailored_resume_1.pdf",
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
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
    """
    Generate a personalized cover letter for a specific job posting using AI.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "resume_id": 1,
        "job_posting_id": 1,
        "personal_message": "I am particularly excited about Tech Corp's innovative approach to software development and their commitment to using cutting-edge technologies."
    }
    ```
    
    **Example Response:**
    ```json
    {
        "content": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Senior Software Engineer position at Tech Corp. With over 5 years of experience in developing scalable web applications using Python, JavaScript, and React, I am excited about the opportunity to contribute to your innovative team.\n\nMy experience at Tech Corp aligns perfectly with your requirements. I have successfully led development teams, improved application performance by 40%, and implemented CI/CD pipelines that reduced deployment time by 60%. I am particularly excited about Tech Corp's innovative approach to software development and their commitment to using cutting-edge technologies.\n\nI am confident that my technical expertise, leadership experience, and passion for delivering high-quality solutions make me an ideal candidate for this role. I look forward to discussing how I can contribute to Tech Corp's continued success.\n\nThank you for considering my application.\n\nBest regards,\nJohn Doe",
        "suggestions": {
            "tone": "Professional and enthusiastic",
            "personalization": "High - includes specific company details",
            "achievement_focus": "Strong - highlights quantifiable results"
        }
    }
    ```
    """
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
            request.personal_message or ""
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
    
    return AIResponse(content=cover_letter)


@router.get("/available-models")
async def get_available_models():
    """
    Get list of available AI model types and current configuration.
    
    **No authentication required.**
    
    **Example Response:**
    ```json
    {
        "models": [
            {
                "id": "openai",
                "name": "OpenAI GPT",
                "description": "OpenAI's GPT models for text generation",
                "capabilities": ["text_generation", "summarization", "translation"]
            },
            {
                "id": "anthropic",
                "name": "Anthropic Claude",
                "description": "Anthropic's Claude models for advanced reasoning",
                "capabilities": ["text_generation", "reasoning", "analysis"]
            },
            {
                "id": "ollama",
                "name": "Ollama Local",
                "description": "Local models using Ollama",
                "capabilities": ["text_generation", "local_inference"]
            }
        ],
        "current_model": "openai"
    }
    ```
    """
    return {
        "models": ModelFactory.get_available_models(),
        "current_model": settings.custom_model_type if settings.use_custom_model else "openai"
    }


@router.post("/configure-model", response_model=ModelConfigResponse)
async def configure_model(
    request: ModelConfigRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Configure custom AI model settings.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "model_type": "ollama",
        "config": {
            "model_name": "llama2",
            "base_url": "http://localhost:11434",
            "temperature": 0.7,
            "max_tokens": 2000
        }
    }
    ```
    
    **Example Response:**
    ```json
    {
        "success": true,
        "message": "Model ollama configured successfully",
        "model_type": "ollama"
    }
    ```
    """
    try:
        # Validate configuration
        if not ModelFactory.validate_config(request.model_type, request.config):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid model configuration"
            )
        
        # Update settings (in a real implementation, you'd save this to database)
        settings.use_custom_model = True
        settings.custom_model_type = request.model_type
        settings.custom_model_config = request.config
        
        return ModelConfigResponse(
            success=True,
            message=f"Model {request.model_type} configured successfully",
            model_type=request.model_type
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to configure model: {str(e)}"
        )


@router.post("/generate-customized-cover-letter", response_model=AIResponse)
async def generate_customized_cover_letter(
    request: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a customized cover letter with specific requirements and styling.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Request Body:**
    ```json
    {
        "resume_content": "John Doe\nSoftware Engineer\n\nEXPERIENCE\nSoftware Engineer at Tech Corp (2020-2023)\n- Developed web applications using Python and JavaScript\n- Led team of 3 developers\n- Improved application performance by 40%",
        "job_description": "We are looking for a Senior Software Engineer with 5+ years of experience in Python and JavaScript. The ideal candidate should have experience with React, Django, and Node.js.",
        "company_name": "Tech Corp",
        "job_title": "Senior Software Engineer",
        "applicant_name": "John Doe",
        "customization": {
            "tone": "enthusiastic",
            "length": "medium",
            "focus_areas": ["leadership", "technical_skills"],
            "include_salary_expectations": false,
            "mention_referral": "Jane Smith from Engineering team"
        }
    }
    ```
    
    **Example Response:**
    ```json
    {
        "content": "Dear Hiring Manager,\n\nI am writing to express my enthusiastic interest in the Senior Software Engineer position at Tech Corp. Jane Smith from your Engineering team recommended this opportunity to me, and I am excited about the possibility of joining your innovative team.\n\nWith over 5 years of experience in software development, I have successfully led development teams and delivered high-impact solutions. At Tech Corp, I led a team of 3 developers and improved application performance by 40%, demonstrating my ability to drive technical excellence and team success.\n\nMy technical expertise in Python, JavaScript, React, Django, and Node.js aligns perfectly with your requirements. I am particularly drawn to Tech Corp's commitment to innovation and the opportunity to work on cutting-edge projects.\n\nI look forward to discussing how my leadership experience and technical skills can contribute to Tech Corp's continued success.\n\nBest regards,\nJohn Doe",
        "suggestions": {
            "tone": "Enthusiastic and professional",
            "personalization": "High - includes referral and company-specific details",
            "achievement_focus": "Strong - highlights leadership and technical achievements"
        }
    }
    ```
    """
    
    # Extract data from request
    resume_content = request.get("resume_content", "")
    job_description = request.get("job_description", "")
    company_name = request.get("company_name", "")
    job_title = request.get("job_title", "")
    applicant_name = request.get("applicant_name", "")
    customization = request.get("customization", {})
    
    if not all([resume_content, job_description, company_name, job_title, applicant_name]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing required fields: resume_content, job_description, company_name, job_title, applicant_name"
        )
    
    # Use AI service to generate customized cover letter
    ai_service = AIService()
    try:
        cover_letter = await ai_service.generate_customized_cover_letter(
            resume_content,
            job_description,
            company_name,
            job_title,
            applicant_name,
            customization
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
    
    return AIResponse(content=cover_letter)


@router.get("/cover-letter-templates", response_model=List[dict])
async def get_cover_letter_templates():
    """
    Get available cover letter templates.
    
    **No authentication required.**
    
    **Example Response:**
    ```json
    [
        {
            "id": "professional",
            "name": "Professional Standard",
            "description": "A traditional, formal cover letter suitable for most industries",
            "template": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the {job_title} position at {company_name}...",
            "variables": ["job_title", "company_name", "applicant_name"]
        },
        {
            "id": "creative",
            "name": "Creative & Modern",
            "description": "A more engaging and creative approach for innovative companies",
            "template": "Hi there!\n\nI'm {applicant_name}, and I'm genuinely excited about the {job_title} opportunity...",
            "variables": ["applicant_name", "job_title", "company_name"]
        },
        {
            "id": "technical",
            "name": "Technical Focus",
            "description": "Emphasizes technical skills and achievements for tech roles",
            "template": "Dear Hiring Manager,\n\nI am excited to apply for the {job_title} position at {company_name}...",
            "variables": ["job_title", "company_name", "years_experience", "primary_technology"]
        }
    ]
    ```
    """
    
    templates = [
        {
            "id": "professional",
            "name": "Professional Standard",
            "description": "A traditional, formal cover letter suitable for most industries",
            "template": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the {job_title} position at {company_name}...",
            "variables": ["job_title", "company_name", "applicant_name"]
        },
        {
            "id": "creative",
            "name": "Creative & Modern",
            "description": "A more engaging and creative approach for innovative companies",
            "template": "Hi there!\n\nI'm {applicant_name}, and I'm genuinely excited about the {job_title} opportunity...",
            "variables": ["applicant_name", "job_title", "company_name"]
        },
        {
            "id": "technical",
            "name": "Technical Focus",
            "description": "Emphasizes technical skills and achievements for tech roles",
            "template": "Dear Hiring Manager,\n\nI am excited to apply for the {job_title} position at {company_name}...",
            "variables": ["job_title", "company_name", "years_experience", "primary_technology"]
        }
    ]
    
    return templates


@router.get("/tailored-resumes", response_model=List[TailoredResumeResponse])
async def get_tailored_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all tailored resumes for the current user.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "original_resume_id": 1,
            "job_posting_id": 1,
            "tailored_content": "John Doe\nSenior Software Engineer\n\nPROFESSIONAL SUMMARY\nResults-driven Senior Software Engineer...",
            "suggestions": {
                "keyword_optimization": "Added senior-level keywords",
                "experience_enhancement": "Emphasized leadership experience"
            },
            "changes_made": {
                "title_update": "Software Engineer → Senior Software Engineer",
                "skills_reorganized": "Grouped by frontend/backend"
            },
            "file_path": "/uploads/tailored_resume_1.pdf",
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "original_resume_id": 1,
            "job_posting_id": 2,
            "tailored_content": "John Doe\nFull Stack Developer\n\nPROFESSIONAL SUMMARY\nVersatile Full Stack Developer...",
            "suggestions": {
                "skill_focus": "Emphasized full-stack capabilities",
                "project_highlighting": "Added relevant project examples"
            },
            "changes_made": {
                "title_update": "Software Engineer → Full Stack Developer",
                "skills_reorganized": "Grouped by frontend/backend"
            },
            "file_path": "/uploads/tailored_resume_2.pdf",
            "created_at": "2024-01-16T14:20:00Z"
        }
    ]
    ```
    """
    result = await db.execute(
        select(TailoredResume)
        .join(Resume)
        .where(Resume.user_id == current_user.id)
    )
    return result.scalars().all()


@router.get("/tailored-resumes/{tailored_id}", response_model=TailoredResumeResponse)
async def get_tailored_resume(
    tailored_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific tailored resume by ID.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `tailored_id`: ID of the tailored resume to retrieve
    
    **Example Request:**
    ```
    GET /api/v1/ai/tailored-resumes/1
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "original_resume_id": 1,
        "job_posting_id": 1,
        "tailored_content": "John Doe\nSenior Software Engineer\n\nPROFESSIONAL SUMMARY\nResults-driven Senior Software Engineer with 5+ years of experience developing scalable web applications using Python, JavaScript, and React. Proven track record of leading development teams and delivering high-impact solutions that improve application performance by 40%.\n\nEXPERIENCE\nSenior Software Engineer at Tech Corp (2020-2023)\n- Led development of enterprise web applications using Python, Django, and React\n- Managed team of 3 developers, improving project delivery time by 25%\n- Optimized application performance resulting in 40% improvement in load times\n- Implemented CI/CD pipelines reducing deployment time by 60%\n\nSKILLS\nProgramming Languages: Python, JavaScript, TypeScript\nFrameworks: Django, React, Node.js, Express\nDatabases: PostgreSQL, MongoDB, Redis\nTools: Git, Docker, AWS, Jenkins\nLeadership: Team Management, Agile Methodologies, Technical Mentoring",
        "suggestions": {
            "keyword_optimization": "Added senior-level keywords and quantifiable achievements",
            "experience_enhancement": "Emphasized leadership and team management experience",
            "skill_alignment": "Reorganized skills to match job requirements",
            "content_structure": "Improved overall flow and readability"
        },
        "changes_made": {
            "title_update": "Software Engineer → Senior Software Engineer",
            "summary_added": "Added professional summary highlighting senior-level experience",
            "achievements_enhanced": "Added quantifiable metrics to experience descriptions",
            "skills_reorganized": "Grouped skills by category and added leadership skills",
            "content_restructuring": "Improved overall document structure and flow"
        },
        "file_path": "/uploads/tailored_resume_1.pdf",
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
    result = await db.execute(
        select(TailoredResume)
        .join(Resume)
        .where(
            TailoredResume.id == tailored_id,
            Resume.user_id == current_user.id
        )
    )
    tailored_resume = result.scalar_one_or_none()
    
    if not tailored_resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tailored resume not found"
        )
    
    return tailored_resume
