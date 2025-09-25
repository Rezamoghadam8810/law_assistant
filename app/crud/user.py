from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db:Session, username:str,email:str,full_name: str=None):
    user = User(username=username,email=email,full_name=full_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db:Session,user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user

def update_user(db: Session,user_id:int, **kwargs):
    user = get_user(db,user_id)
    if not user:
        return None
    for key,value in kwargs.items():
        if value is not None:
            setattr(user,key,value)
    db.commit()
    db.refresh(user)
    return user