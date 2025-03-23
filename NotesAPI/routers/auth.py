from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models import Users
from ..database import Base, SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta, datetime, timezone



router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# JWT Config
SECRET_KEY = "dkndgbdvndovdivsd876mjhfn5w34jb33tn4kjbt4tn4ktb4tb54bwio5jyf9ovu"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class UserReq(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Username not found")
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return user  # Return user object

def create_access_token(username: str, user_id: int,role:str, expires_delta: timedelta = None):
    encode = {"sub": username, "id": user_id,'role':role}
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=20))
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role:str = payload.get('role')
        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
            )
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
        return {"id": user.id, "username": user.username, "role": user.role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

        

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_req: UserReq):
    user_model = Users(
        email=user_req.email,
        username=user_req.username,
        first_name=user_req.first_name,
        last_name=user_req.last_name,
        hashed_password=bcrypt_context.hash(user_req.password),
        is_active=user_req.is_active,
        role=user_req.role,
    )  
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return {"message": "User created successfully", "user": user_model}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.username, user.id,user.role,timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
