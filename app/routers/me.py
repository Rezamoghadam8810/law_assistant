from fastapi import APIRouter, Depends
from app.schemas.user import UserOut
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/me", tags=["me"])

@router.get("/", response_model=UserOut)
def read_profile(current_user: User = Depends(get_current_user)):
    return current_user
