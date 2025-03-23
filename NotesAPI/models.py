from .database import Base,engine
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,nullable=False)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,unique=True,nullable=False)
    hashed_password = Column(String)    
    is_active = Column(Boolean,default=True)
    role = Column(String)

class Notes(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    category = Column(String,nullable=False)
    completed = Column(Boolean,default=False)
    owner_id = Column(Integer,ForeignKey(Users.id))
    