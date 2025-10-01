import random
import time

from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash
from app.schemas.user import UserCreate

def create_user(db: Session, user_in: UserCreate):
    hashed_pw = get_password_hash(user_in.password)
    otp = str(random.randint(1000,9999))
    expiry = int(time.time()) + 120


    user = User(
        username=user_in.username,
        email=user_in.email,
        phone_number = user_in.phone_number,
        full_name=user_in.full_name,
        hashed_password=hashed_pw,
        otp_code = otp,
        otp_expiry=expiry,
        is_verified = False
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # اینجا جای ارسال SMS است (فعلاً کامنت می‌کنیم)
    # send_sms(user.phone_number, f"Your verification code is {otp}")

    print(f"[DEBUG] OTP for {user.phone_number}: {otp}")  # برای تست


    return user

def verify_user_otp(db: Session, phone_number: str, otp_code: str):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return None

    now = int(time.time())
    if user.otp_code == otp_code and user.otp_expiry and now <= user.otp_expiry:
        user.is_verified = True
        user.otp_code = None
        user.otp_expiry = None
        db.commit()
        db.refresh(user)
        return user
    return None

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_phone(db: Session, phone_number: str):
    return db.query(User).filter(User.phone_number == phone_number).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return user

def update_user(db: Session, user_id: int, **kwargs):
    user = get_user(db, user_id)
    if not user:
        return None

    if "password" in kwargs and kwargs["password"]:
        kwargs["hashed_password"] = get_password_hash(kwargs["password"])
        del kwargs["password"]

    for key, value in kwargs.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def create_password_reset_otp(db: Session, phone_number: str):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return None

    otp = str(random.randint(1000, 9999))
    expiry = int(time.time()) + 120  # انقضا ۲ دقیقه بعد

    user.otp_code = otp
    user.otp_expiry = expiry
    db.commit()
    db.refresh(user)

    # 👇 اینجا بعداً با SMS می‌فرستیم
    print(f"[DEBUG] Reset OTP for {user.phone_number}: {otp}")

    return user

def reset_password(db: Session, phone_number: str, otp_code: str, new_password: str):
    user = db.query(User).filter(User.phone_number == phone_number).first()
    if not user:
        return None

    now = int(time.time())
    if user.otp_code == otp_code and user.otp_expiry and now <= user.otp_expiry:
        user.hashed_password = get_password_hash(new_password)
        user.otp_code = None
        user.otp_expiry = None
        db.commit()
        db.refresh(user)
        return user
    return None