from typing import Optional
import os


class Settings:
    # Database settings
    database_url: str = "sqlite:///./customer_registration.db"
    
    # API settings
    api_v1_str: str = "/api/v1"
    project_name: str = "Customer Registration System"
    
    # Security settings
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    def __init__(self):
        # Override with environment variables if they exist
        self.database_url = os.getenv("DATABASE_URL", self.database_url)
        self.api_v1_str = os.getenv("API_V1_STR", self.api_v1_str)
        self.project_name = os.getenv("PROJECT_NAME", self.project_name)
        self.secret_key = os.getenv("SECRET_KEY", self.secret_key)
        self.algorithm = os.getenv("ALGORITHM", self.algorithm)
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", self.access_token_expire_minutes))


settings = Settings() 