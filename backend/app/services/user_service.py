from sqlalchemy.orm import Session
from app.models.user import User


class UserService:

    @staticmethod
    def create_user(db: Session, email: str,password_hash: str, role: str = "user"):

        user = User(
            email=email,
            password=password_hash,
            role=role,
            is_deleted=False
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user


   
    @staticmethod
    def get_by_email(db: Session, email: str):

        return db.query(User).filter(
            User.email == email,
            User.is_deleted == False
        ).first()


  
    @staticmethod
    def get_by_id(db: Session, user_id: int):

        return db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()


   
    @staticmethod
    def get_all(db: Session):

        return db.query(User).filter(
            User.is_deleted == False
        ).all()


  
    @staticmethod
    def update_role(db: Session, user_id: int, role: str):

        user = db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()

        if not user:
            return None

        user.role = role
        db.commit()
        db.refresh(user)

        return user



    @staticmethod
    def delete_user(db: Session, user_id: int):

        user = db.query(User).filter(
            User.id == user_id,
            User.is_deleted == False
        ).first()

        if not user:
            return None

        user.is_deleted = True
        db.commit()

        return True