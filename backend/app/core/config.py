import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "SynapseHR"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://synapse_user:synapse_pass@localhost:5432/synapse_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "groq")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    VITE_API_URL: str = os.getenv("VITE_API_URL", "")
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
