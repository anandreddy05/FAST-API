from fastapi import FastAPI
from .database import Base,SessionLocal,engine
from .routers import notes,auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(notes.router)
