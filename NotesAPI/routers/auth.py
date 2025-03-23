from typing import Annotated
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from ..models import Users
from ..database import Base,SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserReq(BaseModel):
    email : str
    username : str
    first_name : str
    last_name : str
    password : str 
    is_active : bool
    role : str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@router.get("/auth",status_code=status.HTTP_200_OK)
async def get_all_users(db:db_dependency):
    return db.query(Users).all()


@router.post("/auth/",status_code=status.HTTP_201_CREATED)
async def create_user(
                      db:db_dependency,
                      user_req:UserReq
                      ):
    user_model = Users(
    email = user_req.email,
    username  = user_req.username,
    first_name = user_req.first_name, 
    last_name  = user_req.last_name,
    hashed_password  = bcrypt_context.hash(user_req.password), 
    is_active = user_req.is_active, 
    role  = user_req.role,
    )  
    db.add(user_model)
    db.commit()
    db.refresh(user_model)

