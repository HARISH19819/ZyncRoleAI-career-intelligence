import os
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # App & Environment
    PROJECT_NAME: str = "ZyncRole AI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]

    # Database
    # Defaults to local SQLite if Supabase Postgres isn't provided
    SUPABASE_DB_URL: str = "sqlite+aiosqlite:///./zyncrole.db"
    SUPABASE_URL: str = "https://your-project.supabase.co"
    SUPABASE_ANON_KEY: str = "your-supabase-anon-key"
    SUPABASE_SERVICE_ROLE_KEY: str = "your-supabase-service-role-key"

    # Auth & JWT Security (for local fallback / Supabase validation)
    JWT_SECRET: str = "super-secret-zyncrole-jwt-key-minimum-32-chars-hackathon-2026"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # AI & Machine Learning Configuration
    GEMINI_API_KEY: str = ""
    GEMINI_TEXT_MODEL: str = "gemini-3.8-flash"
    GEMINI_EMBEDDING_MODEL: str = "gemini-embedding-2"
    EMBEDDING_DIMENSION: int = 768

    # ATS Resume Builder External Integration
    ATS_RESUME_BUILDER_URL: str = "https://www.open-resume.com"

    # Matching Weights (must sum to 1.0)
    SKILLS_WEIGHT: float = 0.25
    ROLE_WEIGHT: float = 0.15
    DOMAIN_WEIGHT: float = 0.15
    EXPERIENCE_WEIGHT: float = 0.15
    EDUCATION_WEIGHT: float = 0.10
    LOCATION_WEIGHT: float = 0.05
    PREFERENCE_WEIGHT: float = 0.05
    SEMANTIC_WEIGHT: float = 0.10

    # ATS Scoring Weights (must sum to 1.0)
    ATS_KEYWORD_WEIGHT: float = 0.25
    ATS_ROLE_WEIGHT: float = 0.20
    ATS_SECTION_WEIGHT: float = 0.15
    ATS_PROJECT_WEIGHT: float = 0.15
    ATS_FORMATTING_WEIGHT: float = 0.10
    ATS_ACHIEVEMENT_WEIGHT: float = 0.10
    ATS_CONTACT_WEIGHT: float = 0.05

    # Job Sources API Keys
    ADZUNA_APP_ID: str = ""
    ADZUNA_APP_KEY: str = ""
    ADZUNA_COUNTRY: str = "us"
    JOOBLE_API_KEY: str = ""
    THE_MUSE_API_KEY: str = ""
    REMOTIVE_API_ENABLED: bool = False

    # Gated platforms
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    INDEED_CLIENT_ID: str = ""
    INDEED_CLIENT_SECRET: str = ""
    NAUKRI_API_KEY: str = ""
    INTERNSHALA_API_KEY: str = ""

    # Internal ingestion secret
    INTERNAL_INGESTION_SECRET: str = "zyncrole-secure-internal-ingestion-token-2026"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    def validate_weights(self):
        """Validate that all weights sum to 1.0 within floating point precision."""
        matching_sum = round(
            self.SKILLS_WEIGHT + self.ROLE_WEIGHT + self.DOMAIN_WEIGHT +
            self.EXPERIENCE_WEIGHT + self.EDUCATION_WEIGHT + self.LOCATION_WEIGHT +
            self.PREFERENCE_WEIGHT + self.SEMANTIC_WEIGHT,
            4
        )
        if matching_sum != 1.0:
            raise ValueError(f"Matching weights must sum to 1.0, got: {matching_sum}")

        ats_sum = round(
            self.ATS_KEYWORD_WEIGHT + self.ATS_ROLE_WEIGHT + self.ATS_SECTION_WEIGHT +
            self.ATS_PROJECT_WEIGHT + self.ATS_FORMATTING_WEIGHT + self.ATS_ACHIEVEMENT_WEIGHT +
            self.ATS_CONTACT_WEIGHT,
            4
        )
        if ats_sum != 1.0:
            raise ValueError(f"ATS weights must sum to 1.0, got: {ats_sum}")


settings = Settings()
settings.validate_weights()
