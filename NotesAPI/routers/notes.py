from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException,Path,APIRouter
from ..database import Base,SessionLocal,engine
from sqlalchemy.orm import Session
from ..models import Notes,Users
from pydantic import BaseModel,Field
from starlette import status
from .auth import get_current_user

router = APIRouter(
    tags=['notes']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_depedndency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


class NotesMaking(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=10,max_length=300)
    category: str = Field(min_length=3,max_length=20)
    completed: bool = False

@router.get("/")
def get_all_notes(  
                  user:user_dependency,
                  db:db_depedndency
                  ):
    if not user:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    notes_model = db.query(Notes).filter(Notes.id == user.get('id')).all()
    return notes_model

@router.get('/{notes_id}',status_code=status.HTTP_200_OK)
def get_notes_by_id(
                    user:user_dependency,
                    db:db_depedndency,
                    notes_id:int=Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    notes_model = db.query(Notes).filter(Notes.id == notes_id).filter(Notes.owner_id == user.get('id')).first()
    if not notes_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return notes_model

@router.post("/create_notes",status_code=status.HTTP_201_CREATED)
def create_notes(
                user:user_dependency,
                db:db_depedndency,
                insert_notes: NotesMaking
                ):
    if not user:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    notes_model = Notes(**insert_notes.model_dump(),owner_id=user.get('id'))
    db.add(notes_model)
    db.commit()
    db.refresh(notes_model)
    return notes_model

@router.put("/update_note/{notes_id}", status_code=status.HTTP_200_OK)
def update_notes(
    user:user_dependency,
    db: db_depedndency,
    notes_update: NotesMaking,
    notes_id: int = Path(gt=0)
):
    if not user:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    notes_model = db.query(Notes).filter(Notes.id == notes_id).filter(Notes.owner_id == user.get('id')).first()
    if not notes_model:
        raise HTTPException(status_code=404, detail="Id Not Found")

    notes_model.title = notes_update.title
    notes_model.content = notes_update.content
    notes_model.category = notes_update.category
    notes_model.completed = notes_update.completed

    db.commit()
    db.refresh(notes_model)

    return notes_model

@router.delete('/delete_note/{notes_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_notes(
    user: user_dependency,
    db: db_depedndency,
    notes_id: int = Path(gt=0)
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    notes_model = db.query(Notes).filter(Notes.id == notes_id).filter(Notes.owner_id == user.get('id')).first()
    
    if not notes_model:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(notes_model)
    db.commit()
    
    return {"message": "Note deleted successfully"}
