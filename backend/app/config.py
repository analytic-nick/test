from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Keys
    ANTHROPIC_API_KEY: str = ""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/focusgroup"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
    ]
    
    # WebSocket
    WS_HOST: str = "localhost"
    WS_PORT: int = 8000
    
    # App Settings
    MAX_PERSONAS_PER_SESSION: int = 6
    FREE_TIER_DAILY_LIMIT: int = 3
    
    # LLM Settings
    DEFAULT_MODEL: str = "claude-sonnet-4-20250514"
    MAX_TOKENS_PER_RESPONSE: int = 300
    
    class Config:
        env_file = ".env"

settings = Settings()
