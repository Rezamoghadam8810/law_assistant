from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.case import CaseStatus


# -----------------------------
# 1️⃣ پایه‌ی مشترک همه اسکیم‌ها
# -----------------------------
class CaseBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[CaseStatus] = CaseStatus.OPEN


# -----------------------------
# 2️⃣ اسکیمای ایجاد پرونده
# -----------------------------
class CaseCreate(CaseBase):
    client_id: int # پرونده باید به یک موکل متصل باشد

# -----------------------------
# 3️⃣ اسکیمای ویرایش پرونده
# -----------------------------
class CaseUpdate(BaseModel):
    title: Optional[str] =None
    description: Optional[str]=None
    status:Optional[CaseStatus]=None
    end_date: Optional[datetime]=None

# -----------------------------
# 4️⃣ اسکیمای پاسخ (نمایش پرونده)
# -----------------------------
class CaseRead(CaseBase):
    id: int
    created_at : datetime
    update_at : Optional[datetime]=None
    start_date :datetime
    end_date: Optional[datetime]= None

class Config:
    from_attributes = True 
