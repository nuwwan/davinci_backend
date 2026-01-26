from os import getenv
from app.schema.user_schema import UserCreate, UserLogin
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.auth_user import User
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from app.utils.email_service import send_email


# Signup user
def create_auth_controller(user: UserCreate, db: Session):
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user data")

    if db.query(User).filter_by(email=user.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    user_obj = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=hash_password(user.password),
        is_active=False,  # Set to inactive until email is verified
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    # Generate email verification token
    verification_token = generate_email_verification_token(user_obj.id)

    # Send Email for verification

    return {
        "user_id": user_obj.id,
        "email": user_obj.email,
        "message": "User created successfully. Please verify your email.",
    }


# Signin user
def authenticate_user(user_in: UserLogin, db: Session):
    user = db.query(User).filter_by(email=user_in.email).first()

    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid login data")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")

    # Create the JWT token
    now = datetime.utcnow()

    # Access token data (expires in 1 hour)
    access_data = {
        "sub": str(user.id),
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(hours=1),
        "type": "access",
    }
    access_token = create_access_token(data=access_data)

    # Refresh token data (expires in 7 days)
    refresh_data = {
        "sub": str(user.id),
        "iat": now,
        "exp": now + timedelta(days=7),
        "type": "refresh",
    }
    refresh_token = create_access_token(data=refresh_data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600,
    }


# Refresh token
def refresh_access_token(refresh_token: str, db: Session):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = payload.get("sub")
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        now = datetime.utcnow()
        access_data = {
            "sub": str(user.id),
            "role": user.role,
            "iat": now,
            "exp": now + timedelta(hours=1),
            "type": "access",
        }
        new_access_token = create_access_token(data=access_data)

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": 3600,
        }
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        )


# Signout user
def signout_user(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Here you would typically handle token invalidation (e.g., blacklisting)
    return {"message": "User signed out successfully"}


# Activate user email
def activate_user_email(token: str, db: Session):
    """Activate user email by verifying the email verification token"""
    try:
        # Decode and validate the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Verify token type
        if payload.get("type") != "email_verification":
            raise HTTPException(status_code=400, detail="Invalid token type")

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid token")

        # Find user and activate
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if already activated
        if user.is_active:
            raise HTTPException(
                status_code=400, detail="User email already activated"
            )

        # Activate user
        user.is_active = True
        db.commit()
        db.refresh(user)

        return {
            "message": "User email activated successfully",
            "user_id": user.id,
            "email": user.email,
        }

    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid or expired verification token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error activating email: {str(e)}"
        )


# Change user password
def change_user_password(user_id: int, new_password: str, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password changed successfully"}


# Forget user password
def forget_user_password(email: str, new_password: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(new_password)
    db.commit()
    db.refresh(user)

    return {"message": "Password reset successfully"}


def verify_user_email_request(email: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    send_user_verification_email(user.email, str(user.id))
    return {"message": "Verification email sent successfully"}


def send_user_verification_email(to_email: str, user_id: str):
    verification_token = generate_email_verification_token(user_id)
    base_url = getenv("DOMAIN_NAME", "localhost:8000")

    verification_link = (
        f"{base_url}/auth/verify-email?token={verification_token}"
    )

    subject = "Verify your email"
    body = f"Please verify your email by clicking on the following link: {verification_link}"
    # Call the email service to send the email
    send_email(to_email, subject, body)


# Generate email verification token
def generate_email_verification_token(user_id: int):
    """Generate a token for email verification (valid for 24 hours)"""
    now = datetime.utcnow()
    data = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(hours=24),
        "type": "email_verification",
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token
