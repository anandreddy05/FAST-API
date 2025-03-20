from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException,status,Path
from database import engine,SessionLocal
import models
from models import Todos
from pydantic import BaseModel,Field
from router import auth,todos

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

