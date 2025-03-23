from typing import Annotated
from ..database import Base,SessionLocal,engine
from ..models import Users,Notes
from sqlalchemy.orm import Session
from fastapi import APIRouter,Depends,Path,HTTPException
from pydantic import BaseModel,Field
from starlette import status


router = APIRouter(
    prefix="/users",
    tags = ["users"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

