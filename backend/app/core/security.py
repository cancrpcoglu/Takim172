import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Query, HTTPException
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext

# --- AYARLAR ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
ALGORITHM = "HS256"

# BURASI KRİTİK: OAuth2PasswordBearer yerine bunu kullanıyoruz.
# Bu sayede Swagger'da o karmaşık form yerine sadece tek bir kutu çıkar.
security_scheme = HTTPBearer()

# --- ŞİFRELEME FONKSİYONLARI ---
def hash_password(password: str):
    password = password.strip()
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password too long (bcrypt limit 72 bytes)"
        )
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# --- TOKEN OLUŞTURMA ---
def create_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# --- YETKİLENDİRME (SWAGGER İLE TAM UYUMLU) ---

def get_current_user(token: str = Query(..., description="Buraya login'den aldığın tokenı yapıştır")): 
    try:
        # URL'den gelen tokenı çözüyoruz
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")

def require_role(role: str):
    def wrapper(user=Depends(get_current_user)):
        if user.get("role") != role:
            raise HTTPException(status_code=403, detail="Bu işlem için yetkiniz yok")
        return user
    return wrapper