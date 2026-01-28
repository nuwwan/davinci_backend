from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.logger import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # bcrypt has a 72-byte limit, truncate if necessary
    logger.debug("Hashing password")
    return pwd_context.hash(password[:72])


def verify_password(password: str, hashed: str) -> bool:
    # bcrypt has a 72-byte limit, truncate if necessary
    logger.debug("Verifying password")
    return pwd_context.verify(password[:72], hashed)


def create_access_token(data: dict):
    logger.debug(f"Creating access token for user ID: {data.get('sub')}")
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.debug("Access token created successfully")
    return token
