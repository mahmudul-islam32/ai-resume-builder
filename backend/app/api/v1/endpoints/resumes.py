from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os
import shutil
from pathlib import Path

from app.core.database import get_db
from app.models.base import User, Resume
from app.schemas.schemas import ResumeResponse, ResumeCreate, ResumeUpdate
from app.api.v1.endpoints.auth import get_current_user
from app.services.resume_parser import parse_resume
from app.core.config import settings

router = APIRouter()


@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    title: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Upload and parse a resume file (PDF or DOCX).
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Form Data:**
    - `file`: Resume file (PDF or DOCX, max 10MB)
    - `title`: Optional custom title for the resume
    
    **Example cURL Request:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/resumes/upload" \
         -H "Authorization: Bearer YOUR_TOKEN" \
         -F "file=@resume.pdf" \
         -F "title=My Professional Resume"
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "title": "My Professional Resume",
        "original_filename": "resume.pdf",
        "file_type": "pdf",
        "parsed_content": "John Doe\nSoftware Engineer\n...",
        "extracted_data": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "skills": ["Python", "JavaScript", "React"],
            "experience": [...]
        },
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )
    
    # Validate file size
    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum of {settings.max_file_size} bytes"
        )
    
    # Create uploads directory if it doesn't exist
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    filename = f"{current_user.id}_{file.filename}"
    file_path = upload_dir / filename
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Parse resume content
    try:
        parsed_content, extracted_data = await parse_resume(str(file_path), file_extension)
    except Exception as e:
        # Clean up file if parsing fails
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to parse resume: {str(e)}"
        )
    
    # Create resume record
    resume = Resume(
        user_id=current_user.id,
        title=title or file.filename,
        original_filename=file.filename,
        file_path=str(file_path),
        file_type=file_extension,
        parsed_content=parsed_content,
        extracted_data=extracted_data
    )
    
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    
    return resume


@router.get("/", response_model=List[ResumeResponse])
async def get_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get all resumes for the current user.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Example Response:**
    ```json
    [
        {
            "id": 1,
            "user_id": 1,
            "title": "My Professional Resume",
            "original_filename": "resume.pdf",
            "file_type": "pdf",
            "parsed_content": "John Doe\nSoftware Engineer\n...",
            "extracted_data": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "skills": ["Python", "JavaScript"]
            },
            "is_active": true,
            "created_at": "2024-01-15T10:30:00Z"
        },
        {
            "id": 2,
            "user_id": 1,
            "title": "Updated Resume 2024",
            "original_filename": "resume_v2.pdf",
            "file_type": "pdf",
            "parsed_content": "John Doe\nSenior Software Engineer\n...",
            "extracted_data": {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "skills": ["Python", "JavaScript", "React", "Node.js"]
            },
            "is_active": true,
            "created_at": "2024-01-20T14:15:00Z"
        }
    ]
    ```
    """
    result = await db.execute(
        select(Resume).where(Resume.user_id == current_user.id, Resume.is_active == True)
    )
    return result.scalars().all()


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific resume by ID.
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `resume_id`: ID of the resume to retrieve
    
    **Example Request:**
    ```
    GET /api/v1/resumes/1
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "title": "My Professional Resume",
        "original_filename": "resume.pdf",
        "file_type": "pdf",
        "parsed_content": "John Doe\nSoftware Engineer\n...",
        "extracted_data": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "+1-555-0123",
            "skills": ["Python", "JavaScript", "React"],
            "experience": [
                {
                    "title": "Software Engineer",
                    "company": "Tech Corp",
                    "duration": "2020-2023",
                    "description": "Developed web applications..."
                }
            ],
            "education": [
                {
                    "degree": "Bachelor of Science",
                    "field": "Computer Science",
                    "institution": "University of Technology",
                    "year": "2020"
                }
            ]
        },
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
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
    
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: int,
    resume_update: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a resume's metadata (title only).
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `resume_id`: ID of the resume to update
    
    **Example Request Body:**
    ```json
    {
        "title": "Updated Resume Title"
    }
    ```
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "user_id": 1,
        "title": "Updated Resume Title",
        "original_filename": "resume.pdf",
        "file_type": "pdf",
        "parsed_content": "John Doe\nSoftware Engineer\n...",
        "extracted_data": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "skills": ["Python", "JavaScript"]
        },
        "is_active": true,
        "created_at": "2024-01-15T10:30:00Z"
    }
    ```
    """
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
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
    
    # Update fields
    for field, value in resume_update.dict(exclude_unset=True).items():
        setattr(resume, field, value)
    
    await db.commit()
    await db.refresh(resume)
    
    return resume


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Soft delete a resume (marks as inactive but doesn't remove from database).
    
    **Authentication required** - Include Bearer token in Authorization header or use session cookie.
    
    **Path Parameters:**
    - `resume_id`: ID of the resume to delete
    
    **Example Request:**
    ```
    DELETE /api/v1/resumes/1
    ```
    
    **Example Response:**
    ```json
    {
        "message": "Resume deleted successfully"
    }
    ```
    """
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
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
    
    # Soft delete
    resume.is_active = False
    await db.commit()
    
    return {"message": "Resume deleted successfully"}
