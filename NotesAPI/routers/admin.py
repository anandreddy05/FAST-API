from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException,Path,APIRouter
from ..database import Base,SessionLocal,engine
from sqlalchemy.orm import Session
from ..models import Notes,Users
from starlette import status
from .auth import get_current_user


router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depedndency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/notes", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_depedndency):
    if not user or user.get('role').lower() != 'admin': 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    return db.query(Notes).all()

@router.delete("/notes/{notes_id}",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_depedndency,notes_id:int=Path(gt=0)):
    if not user or user.get('role').lower() != 'admin': 
        raise HTTPException(status_code=401, detail="Authentication Failed")
    notes_model = db.query(Notes).filter(Notes.id == notes_id).first()
    if notes_model is None:
        raise HTTPException(status_code=404,detail="Notes not found.")
    db.delete(notes_model)

    db.commit()