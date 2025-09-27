from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.schemas.user import UserCreate, UserOut, UserVerifyOTP
from app.crud import user as crud_user
from app.db.session import get_db
from app.core.security import verify_password, create_access_token
from app.schemas.user import PasswordResetRequest, PasswordResetVerify

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserOut)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # بررسی یکتا بودن ایمیل و موبایل
    if crud_user.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="این ایمیل قبلاً ثبت شده است.")

    existing_user = db.query(crud_user.User).filter(crud_user.User.phone_number == user_in.phone_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="این شماره موبایل قبلاً ثبت شده است.")

    user = crud_user.create_user(db, user_in)
    return user

@router.post("/verify-otp", response_model=UserOut)
def verify_otp(data: UserVerifyOTP, db: Session = Depends(get_db)):
    user = crud_user.verify_user_otp(db, data.phone_number, data.otp_code)
    if not user:
        raise HTTPException(status_code=400, detail="کد OTP نامعتبر یا منقضی شده است.")
    return user



@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)):
    # ۱. پیدا کردن کاربر
    user = crud_user.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=401, detail="کاربر پیدا نشد")

    # ۲. بررسی پسورد
    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")

    # ۳. بررسی تأیید شماره (اختیاری)
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="کاربر هنوز تایید نشده است")

    # ۴. ساخت توکن
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=30
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = crud_user.create_password_reset_otp(db, payload.phone_number)
    if not user:
        raise HTTPException(status_code=404, detail="کاربری با این شماره پیدا نشد")
    return {"msg": "کد بازیابی ارسال شد"}

@router.post("/reset-password")
def reset_password(payload: PasswordResetVerify, db: Session = Depends(get_db)):
    user = crud_user.reset_password(db, payload.phone_number, payload.otp_code, payload.new_password)
    if not user:
        raise HTTPException(status_code=400, detail="کد نادرست یا منقضی شده است")
    return {"msg": "رمز عبور با موفقیت تغییر کرد"}