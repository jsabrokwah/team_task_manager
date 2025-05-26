from datetime import datetime, timedelta
import jwt
import os

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default_secret_key_for_development')
if SECRET_KEY == 'default_secret_key_for_development':
    print("WARNING: Using default JWT secret key. Set JWT_SECRET_KEY environment variable in production.")

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_access_token(identity, expires_delta: timedelta = None):
    data = {"sub": identity}
    if expires_delta:
        expire = datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(identity):
    data = {"sub": identity}
    expire = datetime.now(datetime.timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
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