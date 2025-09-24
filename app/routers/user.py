from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.crud import user as crud_user
from app.schemas.user import UserOut,UserCreate
from app.core.logging import logger



router = APIRouter(prefix="/users", tags=["users"])

# وابستگی برای گرفتن Session
def get_db():
    db = SessionLocal()
    try:
        yield db   # 👈 حتماً yield (نه return)
    finally:
        db.close()


@router.post("/",response_model=UserOut)
def create_user(payload:UserCreate, db:Session=Depends(get_db)):
    logger.info(f"Creating user: {payload.username}")
    try:
        user = crud_user.create_user(db, **payload.model_dump())
        return user
    except Exception as e:
        logger.error(f"Error creating user : {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/",response_model=list[UserOut])
def read_users(user_id: int=0 ,limit:int=10, db:Session=Depends(get_db)):
    logger.info("Fetching users list")
    user = crud_user.get_users(db,user_id=user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user



@router.get("/{user_id}",response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_user(db,user_id=user_id)
    if not user:
        logger.warning(f"User {user_id} not found")
        raise HTTPException(status_code=404,detail="User not found")
    return user



@router.delete("/{user_id}",response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user= crud_user.delete_user(db, user_id=user_id)
    if not user:
        logger.warning(f"Tried to delete missing user {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Deleted user {user_id}")
    return user

