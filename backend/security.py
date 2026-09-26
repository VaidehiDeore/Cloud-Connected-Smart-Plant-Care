from datetime import datetime, timedelta, timezone
import hashlib, hmac, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User, Device
from config import settings

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer = HTTPBearer(auto_error=False)

def hash_password(value): return pwd.hash(value)
def verify_password(value, hashed): return pwd.verify(value, hashed)

def token_for(user_id):
    exp = datetime.now(timezone.utc) + timedelta(hours=12)
    return jwt.encode({"sub": str(user_id), "exp": exp}, settings.secret_key, algorithm="HS256")

def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
                 db: Session = Depends(get_db)):
    if not credentials: raise HTTPException(401, "Authentication required")
    try:
        data = jwt.decode(credentials.credentials, settings.secret_key, algorithms=["HS256"])
        user = db.get(User, int(data["sub"]))
    except Exception:
        user = None
    if not user: raise HTTPException(401, "Invalid or expired token")
    return user

def device_hash(key): return hashlib.sha256(key.encode()).hexdigest()
def compare(a,b): return hmac.compare_digest(a,b)
def owner(device: Device, user: User):
    if not device or device.user_id != user.user_id:
        raise HTTPException(403, "Device access denied")
