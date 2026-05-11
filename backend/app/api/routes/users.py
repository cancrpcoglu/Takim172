from fastapi import APIRouter, Depends, HTTPException, Header
from jose import JWTError,jwt
from sqlalchemy.orm import Session

from backend.app.core.database import SessionLocal
from backend.app.models.user import User
from backend.app.schemas.user_schema import UserCreate, UserLogin
from backend.app.services.user_service import UserService

from backend.app.core.security import ALGORITHM, SECRET_KEY, hash_password, verify_password, create_token
from backend.app.core.security import get_current_user, require_role

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = UserService.get_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserService.create_user(
        db,
        email=user.email,
        password_hash=hash_password(user.password),
        role="user"
    )

    return {
        "success": True,
        "message": "User created",
        "data": new_user
    }


@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = UserService.get_by_email(db, data.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_token(user)
    
    print(f"Login successful: {data.email} - Role: {user.role}")
    
    # BURAYI GÜNCELLEDİK: Kullanıcı bilgilerini de ekledik
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role  # İşte kritik nokta burası!
        }
    }

@router.get("/me")
def me(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token yok")

    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token bozuk")

        user = db.query(User).filter(User.id == int(user_id)).first()

        if not user:
            raise HTTPException(status_code=404, detail="User bulunamadı")

        return {
            "success": True,
            "data": {
                "id": user.id,
                "email": user.email,
                "role": user.role
            }
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Token geçersiz")
@router.get("/")
def get_users(db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    users = UserService.get_all(db)
    return {"success": True, "data": users}

@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    user_data = UserService.get_by_id(db, id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return {"success": True, "data": user_data}

@router.put("/{id}/role")
def update_role(id: int, role: str, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    updated = UserService.update_role(db, id, role)
    return {"success": True, "message": "Role updated", "data": updated}

@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    UserService.delete_user(db, id)
    return {"success": True, "message": "User deleted"}