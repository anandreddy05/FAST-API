from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
# engine = create_engine(SQLALCHEMY_DATABASE_URL,connect_args= {'check_same_thread':False})
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1234@localhost/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
