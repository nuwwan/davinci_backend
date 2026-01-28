from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from app.core.logger import logger
from app.core.config import DATABASE_URL, ENVIRONMENT

load_dotenv()

logger.info(f"Environment: {ENVIRONMENT}")
logger.info(f"Initializing database connection: {DATABASE_URL}")

# Create engine with different settings based on environment
if ENVIRONMENT == "production":
    # Production: Connection pooling for AWS RDS
    engine = create_engine(
        DATABASE_URL,
        pool_size=20,
        max_overflow=40,
        pool_pre_ping=True,  # Verify connections before using them
        pool_recycle=3600,  # Recycle connections every hour
        echo=False,
    )
    logger.info("Using production database connection pool configuration")
else:
    # Development/Staging: Standard configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args=(
            {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
        ),
        echo=False,
    )
    logger.info("Using development/staging database configuration")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
logger.debug("SQLAlchemy SessionLocal created")

Base = declarative_base()


def get_db():
    logger.debug("Creating database session")
    db = SessionLocal()
    try:
        yield db
    finally:
        logger.debug("Closing database session")
        db.close()
