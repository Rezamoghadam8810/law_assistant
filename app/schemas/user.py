from typing import Optional
from pydantic import BaseModel,EmailStr,ConfigDict


# ورودی ساخت کاربر
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    # اجازه بده آبجکت‌های ORM (SQLAlchemy) به JSON تبدیل بشن
    model_config = ConfigDict(from_attributes=True)

