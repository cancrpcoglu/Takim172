from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.services.user_service import UserService
# get_current_user ve require_role artık security.py'deki yeni HTTPBearer yapısını kullanıyor
from app.core.security import hash_password, verify_password, create_token
from app.core.security import get_current_user, require_role

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
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = UserService.get_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

   
    if not verify_password(password, user.password): 
        raise HTTPException(status_code=401, detail="Wrong password")

    token = create_token(user)

   
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def me(user=Depends(get_current_user)):
    
    return {
        "success": True,
        "data": user
    }

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