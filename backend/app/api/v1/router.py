from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, resumes, jobs, applications, interviews, ai, ats

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(ats.router, prefix="/ats", tags=["ats"])
