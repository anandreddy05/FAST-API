from typing import Annotated
from fastapi import FastAPI,Depends,HTTPException,Path,APIRouter
from ..database import Base,SessionLocal,engine
from sqlalchemy.orm import Session
from ..models import Notes
from pydantic import BaseModel,Field
from starlette import status

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

class NotesMaking(BaseModel):
    title: str = Field(min_length=3)
    content: str = Field(min_length=10,max_length=300)
    category: str = Field(min_length=3,max_length=20)
    completed: bool = False

@router.get("/")
def get_all_notes(db:db_depedndency):
    notes_model = db.query(Notes).all()
    return notes_model

@router.get('/{notes_id}',status_code=status.HTTP_200_OK)
def get_notes_by_id(db:db_depedndency,
                    notes_id:int=Path(gt=0)):
    notes_model = db.query(Notes).filter(Notes.id == notes_id).first()
    if not notes_model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return notes_model

@router.post("/create_notes",status_code=status.HTTP_201_CREATED)
def create_notes(db:db_depedndency,
                 insert_notes: NotesMaking):
    notes_model = Notes(**insert_notes.model_dump())
    db.add(notes_model)
    db.commit()
    db.refresh(notes_model)
    return notes_model

@router.put("/update_note/{notes_id}", status_code=status.HTTP_200_OK)
def update_notes(
    db: db_depedndency,
    notes_update: NotesMaking,
    notes_id: int = Path(gt=0)
):
    notes_model = db.query(Notes).filter(Notes.id == notes_id).first()
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
async def delete_notes(db: db_depedndency, notes_id: int = Path(gt=0)):
    notes_model = db.query(Notes).filter(Notes.id == notes_id).first()
    if not notes_model:
        raise HTTPException(status_code=404, detail="Id not found")
    
    db.delete(notes_model)
    db.commit()
    
    return {"message": "Note deleted successfully"}