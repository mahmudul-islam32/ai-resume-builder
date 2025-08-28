from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, SessionLocal
from app.models import base
from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)
    
    # Create uploads directory
    os.makedirs("uploads", exist_ok=True)
    
    yield
    
    # Shutdown
    pass


app = FastAPI(
    title="AI Resume Builder API",
    description="AI-powered resume tailoring and job application tracking system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://frontend:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "AI Resume Builder API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
