from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:postgres@db:5432/ai_resume"
    
    # JWT
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 15  # 15 minutes
    refresh_token_expire_days: int = 7     # 1 week
    
    # Cookie Settings
    cookie_domain: Optional[str] = None
    cookie_secure: bool = True  # Set to False for HTTP in development
    cookie_httponly: bool = True
    cookie_samesite: str = "lax"
    
    # Development mode
    development_mode: bool = False
    
    # API Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    
    # Custom Model Configuration
    use_custom_model: bool = False
    custom_model_type: str = "openai"  # "openai", "anthropic", "huggingface", "local", "custom"
    custom_model_config: Optional[dict] = None
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # File Upload
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "./uploads"
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Check for development mode environment variable
        dev_mode = os.getenv("DEVELOPMENT_MODE", "false").lower() == "true"
        self.development_mode = dev_mode
        
        # Override cookie settings for development
        if self.development_mode:
            print(f"🔧 Development mode enabled - setting cookie_secure=False")
            self.cookie_secure = False
        else:
            print(f"🔒 Production mode - cookie_secure=True")
    
    class Config:
        env_file = ".env"


settings = Settings()
