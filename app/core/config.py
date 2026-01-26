import os
from typing import Optional

# Environment Configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()  # development, staging, production
DEBUG = ENVIRONMENT != "production"

# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Database Configuration
"""
DATABASE CONFIGURATION GUIDE:

DEVELOPMENT (default):
    export ENVIRONMENT=development
    Uses SQLite automatically: sqlite:///./app.db

STAGING:
    export ENVIRONMENT=staging
    Uses PostgreSQL: postgresql://qna_user:qna_pass@localhost:5432/qna_db_staging
    Or override: export DATABASE_URL=postgresql://user:pass@host:port/db

PRODUCTION (AWS RDS):
    export ENVIRONMENT=production
    export DB_HOST=your-rds-endpoint.us-east-1.rds.amazonaws.com
    export DB_PORT=5432
    export DB_USER=dbadmin
    export DB_PASSWORD=secure_password
    export DB_NAME=production_db
    
    This creates: postgresql://dbadmin:password@endpoint:5432/production_db
    With connection pooling optimized for AWS RDS.
"""
def get_database_url() -> str:
    """
    Get database URL based on environment.
    
    For Production:
        AWS RDS PostgreSQL via environment variables:
        - DB_HOST: RDS endpoint
        - DB_PORT: Database port
        - DB_USER: Database username
        - DB_PASSWORD: Database password
        - DB_NAME: Database name
    
    For Development/Staging:
        - DATABASE_URL: Full database URL (overrides other settings)
        - Falls back to SQLite if no URL provided
    """
    
    # If DATABASE_URL is explicitly set, use it (for development/testing)
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    
    # Production: AWS RDS PostgreSQL
    if ENVIRONMENT == "production":
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")
        
        if not all([db_host, db_user, db_password, db_name]):
            raise ValueError(
                "Production environment requires DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME"
            )
        
        # AWS RDS PostgreSQL connection string
        database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return database_url
    
    # Development/Staging: Local PostgreSQL or SQLite
    if ENVIRONMENT == "staging":
        # Staging can use a local PostgreSQL or the one provided in DATABASE_URL
        return os.getenv(
            "DATABASE_URL",
            "postgresql://qna_user:qna_pass@localhost:5432/qna_db_staging"
        )
    
    # Default: Local SQLite for development
    return "sqlite:///./app.db"


DATABASE_URL = get_database_url()
