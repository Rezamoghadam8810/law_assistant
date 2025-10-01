from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional

from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


def get_clients(db: Session, lawyer_id: int, skip: int = 0, limit: int = 50) -> List[Client]:
    """لیست همه‌ی موکل‌های یک وکیل"""
    stmt = select(Client).where(Client.lawyer_id == lawyer_id).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()


def get_client(db: Session, lawyer_id: int, client_id: int) -> Optional[Client]:
    """گرفتن یک موکل خاص با id"""
    stmt = select(Client).where(Client.lawyer_id == lawyer_id, Client.id == client_id)
    return db.execute(stmt).scalar_one_or_none()


def create_client(db: Session, lawyer_id: int, data: ClientCreate) -> Client:
    """ایجاد موکل جدید برای یک وکیل"""
    obj = Client(
        lawyer_id=lawyer_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_client(db: Session, lawyer_id: int, client_id: int, data: ClientUpdate) -> Optional[Client]:
    """به‌روزرسانی اطلاعات یک موکل"""
    obj = get_client(db, lawyer_id, client_id)
    if not obj:
        return None

    if data.name is not None:
        obj.name = data.name
    if data.email is not None:
        obj.email = data.email
    if data.phone is not None:
        obj.phone = data.phone

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def delete_client(db: Session, lawyer_id: int, client_id: int) -> bool:
    """حذف یک موکل"""
    obj = get_client(db, lawyer_id, client_id)
    if not obj:
        return False

    db.delete(obj)
    db.commit()
    return True
