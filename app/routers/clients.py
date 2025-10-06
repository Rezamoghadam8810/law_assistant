from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.client import ClientBase,ClientOut,ClientUpdate
from app.crud import client as crud_client
from app.db.session import get_db
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)


@router.get("/", response_model=List[ClientOut])
def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """لیست همه‌ی موکل‌های یک وکیل"""
    return crud_client.get_clients(db, lawyer_id=current_user.id, skip=skip, limit=limit)


@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """ایجاد موکل جدید"""
    return crud_client.create_client(db, lawyer_id=current_user.id, data=payload)


@router.get("/{client_id}", response_model=ClientOut)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = crud_client.get_client(db, lawyer_id=current_user.id, client_id=client_id)
    if not obj:
        raise HTTPException(status_code=404, detail="موکل یافت نشد")
    return obj


@router.patch("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: int,
    payload: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    obj = crud_client.update_client(db, lawyer_id=current_user.id, client_id=client_id, data=payload)
    if not obj:
        raise HTTPException(status_code=404, detail="موکل یافت نشد")
    return obj


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ok = crud_client.delete_client(db, lawyer_id=current_user.id, client_id=client_id)
    if not ok:
        raise HTTPException(status_code=404, detail="موکل یافت نشد")
    return None
