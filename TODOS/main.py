from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException,status,Path
from database import engine,SessionLocal
import models
from models import Todos
from pydantic import BaseModel,Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session,Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,max_length=100)
    priority: int = Field(gt=1,lt=6)
    complete: bool

@app.get("/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model:
        return todo_model
    raise HTTPException(status_code=404,detail="To Do not found")

@app.post("/todo",status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency,insert_todo: TodoRequest):
    todo_model = Todos(**insert_todo.model_dump())
    
    db.add(todo_model)
    db.commit()
    
@app.put("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404,detail='To Do Not Found')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todo/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,
                      todo_id: int=Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404,detail="Id Not Found")
    db.delete(todo_model) 
    db.commit()