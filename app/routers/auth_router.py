from app.schema.user_schema import UserCreate, UserLogin
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth_controller import (
    create_user,
    authenticate_user,
    activate_user_email,
    verify_user_email_request,
)
from app.core.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"User registration attempt: {user.email}")
    try:
        result = create_user(user, db)
        logger.info(f"User registered successfully: {user.email}")
        return result
    except Exception as e:
        logger.error(f"User registration failed for {user.email}: {str(e)}")
        raise


@router.post("/login", status_code=200)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    logger.info(f"User login attempt: {user.email}")
    try:
        result = authenticate_user(user, db)
        logger.info(f"User logged in successfully: {user.email}")
        return result
    except Exception as e:
        logger.warning(f"User login failed for {user.email}: {str(e)}")
        raise


@router.post("/activate", status_code=200)
def request_to_activate_user(email: str, db: Session = Depends(get_db)):
    logger.info(f"User activation request: {email}")
    try:
        result = verify_user_email_request(email, db)
        logger.info(f"Activation email sent: {email}")
        return result
    except Exception as e:
        logger.error(f"Activation request failed for {email}: {str(e)}")
        raise


@router.get("/verify-email", status_code=200)
def verify_email(token: str, db: Session = Depends(get_db)):
    logger.info("Email verification token received")
    try:
        result = activate_user_email(token, db)
        logger.info("Email verified successfully")
        return result
    except Exception as e:
        logger.warning(f"Email verification failed: {str(e)}")
        raise
