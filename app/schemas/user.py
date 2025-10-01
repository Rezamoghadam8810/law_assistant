from pydantic import BaseModel, EmailStr
from typing import Optional

# ✅ پایه برای اشتراک بین مدل‌ها
class UserBase(BaseModel):
    username: str
    email: EmailStr
    phone_number : str
    full_name: Optional[str] = None

# ✅ ساخت کاربر جدید → شامل password
class UserCreate(UserBase):
    password: str  # 👈 کاربر خام ارسال می‌کنه

class UserVerifyOTP(BaseModel):
    phone_number : str
    otp_code : str


# ✅ آپدیت کاربر → همه فیلدها اختیاری
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

# ✅ خروجی کاربر → هیچ‌وقت password نشون داده نمی‌شه
class UserOut(UserBase):
    id: int
    is_active: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:str
    phone_number: Optional[str] = None
    password: str

class PasswordResetRequest(BaseModel):
    phone_number: str

class PasswordResetVerify(BaseModel):
    phone_number: str
    otp_code: str
    new_password: str

class TokenRefreshRequest(BaseModel):
    refresh_token: str