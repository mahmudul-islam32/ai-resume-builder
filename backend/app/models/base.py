from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()


class ApplicationStatus(enum.Enum):
    APPLIED = "applied"
    INTERVIEWING = "interviewing" 
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # pdf, docx
    parsed_content = Column(Text)
    extracted_data = Column(JSON)  # Structured resume data
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="resumes")
    tailored_resumes = relationship("TailoredResume", back_populates="original_resume", cascade="all, delete-orphan")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    location = Column(String)
    salary_range = Column(String)
    extracted_keywords = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    applications = relationship("Application", back_populates="job_posting")
    tailored_resumes = relationship("TailoredResume", back_populates="job_posting")


class TailoredResume(Base):
    __tablename__ = "tailored_resumes"

    id = Column(Integer, primary_key=True, index=True)
    original_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    tailored_content = Column(Text, nullable=False)
    suggestions = Column(JSON)  # AI suggestions
    changes_made = Column(JSON)  # Track what was changed
    file_path = Column(String)  # Path to generated resume file
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    original_resume = relationship("Resume", back_populates="tailored_resumes")
    job_posting = relationship("JobPosting", back_populates="tailored_resumes")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)
    cover_letter = Column(Text)
    cover_letter_file_path = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    job_posting = relationship("JobPosting", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    title = Column(String, nullable=False)  # e.g., "Technical Interview", "HR Round"
    scheduled_date = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer)
    interviewer_name = Column(String)
    interviewer_email = Column(String)
    meeting_link = Column(String)
    location = Column(String)
    interview_type = Column(String)  # video, phone, in-person
    status = Column(String, default="scheduled")  # scheduled, completed, cancelled
    feedback = Column(Text)
    notes = Column(Text)
    next_steps = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    application = relationship("Application", back_populates="interviews")
