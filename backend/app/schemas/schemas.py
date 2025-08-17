from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Resume Schemas
class ResumeBase(BaseModel):
    title: str


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    title: Optional[str] = None


class ResumeResponse(ResumeBase):
    id: int
    user_id: int
    original_filename: str
    file_type: str
    parsed_content: Optional[str] = None
    extracted_data: Optional[dict] = None
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Job Posting Schemas
class JobPostingBase(BaseModel):
    url: str
    title: str
    company: str
    description: str
    requirements: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None


class JobPostingCreate(BaseModel):
    url: str


class JobPostingResponse(JobPostingBase):
    id: int
    extracted_keywords: Optional[dict] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Tailored Resume Schemas
class TailoredResumeBase(BaseModel):
    original_resume_id: int
    job_posting_id: int


class TailoredResumeCreate(TailoredResumeBase):
    pass


class TailoredResumeResponse(TailoredResumeBase):
    id: int
    tailored_content: str
    suggestions: Optional[dict] = None
    changes_made: Optional[dict] = None
    file_path: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Application Schemas
class ApplicationBase(BaseModel):
    job_posting_id: int
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    status: ApplicationStatus
    applied_date: datetime
    cover_letter: Optional[str] = None
    cover_letter_file_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Include related data
    job_posting: JobPostingResponse
    
    model_config = ConfigDict(from_attributes=True)


# Interview Schemas
class InterviewBase(BaseModel):
    title: str
    scheduled_date: datetime
    duration_minutes: Optional[int] = None
    interviewer_name: Optional[str] = None
    interviewer_email: Optional[str] = None
    meeting_link: Optional[str] = None
    location: Optional[str] = None
    interview_type: Optional[str] = None


class InterviewCreate(InterviewBase):
    application_id: int


class InterviewUpdate(BaseModel):
    title: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    interviewer_name: Optional[str] = None
    interviewer_email: Optional[str] = None
    meeting_link: Optional[str] = None
    location: Optional[str] = None
    interview_type: Optional[str] = None
    status: Optional[str] = None
    feedback: Optional[str] = None
    notes: Optional[str] = None
    next_steps: Optional[str] = None


class InterviewResponse(InterviewBase):
    id: int
    application_id: int
    status: str
    feedback: Optional[str] = None
    notes: Optional[str] = None
    next_steps: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_applications: int
    applications_by_status: dict
    recent_applications: List[ApplicationResponse]
    upcoming_interviews: List[InterviewResponse]


# AI Schemas
class AITailorRequest(BaseModel):
    resume_id: int
    job_posting_id: int


class AICoverLetterRequest(BaseModel):
    resume_id: int
    job_posting_id: int
    additional_info: Optional[str] = None


class AIResponse(BaseModel):
    content: str
    suggestions: Optional[dict] = None
