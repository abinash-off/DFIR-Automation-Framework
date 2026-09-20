from datetime import datetime,timedelta,timezone
from jose import jwt
from passlib.context import CryptContext
from .config import settings

ALGORITHM="HS256"
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str)->str:
    return pwd_context.hash(password)

def verify_password(password:str,password_hash:str)->bool:
    return pwd_context.verify(password,password_hash)

def create_access_token(subject:str)->str:
    expires=datetime.now(timezone.utc)+timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub":subject,"exp":expires},settings.secret_key,algorithm=ALGORITHM)

def decode_token(token:str)->str:
    payload=jwt.decode(token,settings.secret_key,algorithms=[ALGORITHM])
    subject=payload.get("sub")
    if not subject:
        raise ValueError("Invalid token")
    return subject
