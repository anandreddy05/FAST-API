from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,HTTPException,status,Path
from ..database import SessionLocal
from ..models import Todos,Users
from pydantic import BaseModel,Field
from .auth import get_current_user
from passlib.context import CryptContext

router = APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)

@router.get("/{user_id}")
async def get_user(db:db_dependency,
                   user_id:int = Path(gt=0)):
    user_details = db.query(Users).filter(Users.id == user_id).first()
    if not user_details:
        raise HTTPException(status_code=401,detail="User Not Found")
    return user_details

@router.put("/password")
async def change_password(
    db: db_dependency,
    user: user_dependency,
    user_verification: UserVerification
):
    if not user or "id" not in user:
        raise HTTPException(status_code=401, detail="Authentication required")

    user_details = db.query(Users).filter(Users.id == user["id"]).first()

    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt_context.verify(user_verification.password, user_details.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect current password")

    user_details.hashed_password = bcrypt_context.hash(user_verification.new_password)
    
    db.add(user_details)
    db.commit()
    db.refresh(user_details) 

    return {"message": "Password updated successfully"}

@router.put("/phone_number/{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(db:db_dependency,
                              user:user_dependency,
                              phone_number: str):
    if not user:
        raise HTTPException(status_code=402,detail="Authentication Failed")
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()