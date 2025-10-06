# app/crud/case.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate


# -------------------------------
# 1️⃣ گرفتن پرونده بر اساس id
# -------------------------------
def get(db: Session, case_id: int) -> Optional[Case]:
    """
    یک پرونده را بر اساس id از دیتابیس برمی‌گرداند.
    """
    return db.query(Case).filter(Case.id == case_id).first()


# -------------------------------
# 2️⃣ گرفتن چند پرونده (لیست)
# -------------------------------
def get_multi(db: Session, skip: int = 0, limit: int = 100) -> List[Case]:
    """
    تعدادی پرونده را (مثلاً برای نمایش در لیست) برمی‌گرداند.
    """
    return db.query(Case).offset(skip).limit(limit).all()


# -------------------------------
# 3️⃣ ساخت پرونده جدید
# -------------------------------
def create(db: Session, obj_in: CaseCreate) -> Case:
    """
    پرونده‌ی جدیدی ایجاد می‌کند.
    """
    db_obj = Case(
        title=obj_in.title,
        description=obj_in.description,
        client_id=obj_in.client_id,
        status=obj_in.status,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)  # دوباره از دیتابیس می‌خونه تا مقدار id و تاریخ‌ها هم بیاد
    return db_obj


# -------------------------------
# 4️⃣ ویرایش پرونده
# -------------------------------
def update(db: Session, db_obj: Case, obj_in: CaseUpdate) -> Case:
    """
    پرونده‌ی موجود را به‌روزرسانی می‌کند.
    """
    update_data = obj_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)  # هر فیلدی که در obj_in آمده، مقدارش را عوض می‌کند
    db.commit()
    db.refresh(db_obj)
    return db_obj


# -------------------------------
# 5️⃣ حذف پرونده
# -------------------------------
def remove(db: Session, case_id: int) -> Optional[Case]:
    """
    پرونده را حذف می‌کند.
    """
    obj = db.query(Case).filter(Case.id == case_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
