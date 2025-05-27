from datetime import datetime, timedelta
import jwt
import os
import logging

logger = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_secret_key_for_development')
if SECRET_KEY == 'default_secret_key_for_development':
    logger.warning("Using default JWT secret key. Set JWT_SECRET_KEY environment variable in production.")

ALGORITHM = 'HS256'
# Get token expiration times from environment variables with fallbacks
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
REFRESH_TOKEN_EXPIRE_SECONDS = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 604800))

def create_access_token(identity, expires_delta: timedelta = None):
    data = {"sub": identity}
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    data.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(identity):
    data = {"sub": identity}
    expire = datetime.now(datetime.timezone.utc) + timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS)
    data.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None
        return payload
    except jwt.PyJWTError:
        return None
        
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None
        return payload
    except jwt.PyJWTError:
        return None