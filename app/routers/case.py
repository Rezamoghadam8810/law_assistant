# app/api/v1/endpoints/case.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.schemas.case import CaseCreate, CaseUpdate, CaseRead
from app.db.session import get_db  # تابعی که session دیتابیس را برمی‌گرداند

router = APIRouter(prefix="/cases", tags=["Cases"])

# --------------------------------------
# 📥 ایجاد پرونده جدید
# --------------------------------------
@router.post("/", response_model=CaseRead)
def create_case(case_in: CaseCreate, db: Session = Depends(get_db)):
    case = crud.case.create(db=db, obj_in=case_in)
    return case


# --------------------------------------
# 📄 دریافت لیست پرونده‌ها
# --------------------------------------
@router.get("/", response_model=List[CaseRead])
def read_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cases = crud.case.get_multi(db=db, skip=skip, limit=limit)
    return cases


# --------------------------------------
# 🔍 دریافت پرونده با id
# --------------------------------------
@router.get("/{case_id}", response_model=CaseRead)
def read_case(case_id: int, db: Session = Depends(get_db)):
    case = crud.case.get(db=db, case_id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


# --------------------------------------
# ✏️ ویرایش پرونده
# --------------------------------------
@router.put("/{case_id}", response_model=CaseRead)
def update_case(case_id: int, case_in: CaseUpdate, db: Session = Depends(get_db)):
    db_case = crud.case.get(db=db, case_id=case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="Case not found")
    case = crud.case.update(db=db, db_obj=db_case, obj_in=case_in)
    return case


# --------------------------------------
# 🗑 حذف پرونده
# --------------------------------------
@router.delete("/{case_id}", response_model=CaseRead)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    case = crud.case.remove(db=db, case_id=case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
