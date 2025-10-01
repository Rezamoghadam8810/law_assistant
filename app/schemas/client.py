from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# پایه
class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)

# برای ایجاد موکل جدید
class ClientCreate(ClientBase):
    pass

# برای بروزرسانی موکل
class ClientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(default=None, max_length=50)

# برای نمایش خروجی
class ClientOut(ClientBase):
    id: int

    class Config:
        from_attributes = True  # برای پشتیبانی مستقیم از ORM
