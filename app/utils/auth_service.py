from jose import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM
from app.core.logger import logger

# Generate email verification token
def generate_email_verification_token(user_id: int):
    """Generate a token for email verification (valid for 24 hours)"""
    logger.debug(f"Generating email verification token for user: {user_id}")
    
    now = datetime.utcnow()
    data = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(hours=24),
        "type": "email_verification",
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Email verification token generated successfully")
    return token

def verify_email_verification_token(token: str):
    """Verify the email verification token and return the user ID"""
    logger.debug("Verifying email verification token")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "email_verification":
            logger.warning("Invalid token type for email verification")
            return None
        user_id = payload.get("sub")
        logger.debug(f"Email verification token valid for user: {user_id}")
        return user_id
    except jwt.ExpiredSignatureError:
        logger.warning("Email verification token has expired")
        return None
    except jwt.JWTError as e:
        logger.error(f"Error decoding email verification token: {str(e)}")
        return None