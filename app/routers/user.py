from fastapi import APIRouter,Depends,HTTPException,Query,Path
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import user as crud_user
from app.schemas.user import UserOut,UserCreate,UserUpdate
from app.core.logging import logger



router = APIRouter(prefix="/users", tags=["users"])


# @router.get("/ping")
# def ping():
#     return {"msg": "pong"}



# وابستگی برای گرفتن Session
def get_db():
    db = SessionLocal()
    try:
        yield db   # 👈 حتماً yield (نه return)
    finally:
        db.close()


@router.post("/",response_model=UserOut,status_code=201)
def create_user(payload:UserCreate, db:Session=Depends(get_db)):
    logger.info(f"Creating user: {payload.username}")
    try:
        user = crud_user.create_user(db, **payload.model_dump())
        return user
    except Exception as e:
        logger.error(f"Error creating user : {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/",response_model=list[UserOut])
def read_users(
        skip: int = Query(0,ge=0,description="چند آیتم اول رو رد کن"),
        limit: int = Query(10,ge=1, le=100, description="چند آیتم برگردان"),
        db:Session=Depends(get_db),
):
    logger.info("Fetching users list")
    user = crud_user.get_users(db, skip=skip, limit=limit)
    return user



@router.get("/{user_id}",response_model=UserOut)
def read_user(
        user_id: int = Path(..., ge=1,description="شناسه کاربر"),
        db: Session = Depends(get_db),
):
    user = crud_user.get_user(db,user_id=user_id)
    if not user:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404,detail="User not found")
    return user



@router.delete("/{user_id}",response_model=UserOut)
def delete_user(
        user_id: int = Path(...,ge=1,description="شناسه کاربر"),
        db: Session = Depends(get_db),
):
    user= crud_user.delete_user(db, user_id=user_id)
    if not user:
        logger.warning(f"Tried to delete missing user {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user {user_id}")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(
        user_id: int,
        payload: UserUpdate,
        db: Session = Depends(get_db),
):
    user = crud_user.update_user(db,user_id=user_id,**payload.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user