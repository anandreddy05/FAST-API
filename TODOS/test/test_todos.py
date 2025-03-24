import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from ..router.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from ..models import Todos

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'anand@123', 'id': 1, 'user_role': 'admin'}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))  # Cleanup first
        connection.commit()

    todo = Todos(
        title="Learn To Code",
        description="Need to learn everyday",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': test_todo.id,  
        'title': 'Learn To Code',
        'description': 'Need to learn everyday',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': test_todo.id,  
        'title': 'Learn To Code',
        'description': 'Need to learn everyday',
        'priority': 5,
        'complete': False,
        'owner_id': 1
    }

def read_one_authenticates_not_found():
    response = client.get("todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "TOdO Not Found"}
    
def test_create_todo(test_todo):
    request_data={
        'id':2,
        'title':'New Todo!',
        'description': 'New todo description',
        'priority': 4,
        'complete': True,
    }
    db = TestingSessionLocal()
    response = client.post('/todo',json=request_data)
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
 
def test_update_todo(test_todo):
    request_data = {
        'title':"Hey",
        "description": 'Need to learn everyday!',
        'priority': 3,
        'complete': False
    }   
    response = client.put("todo/1",json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Hey'

def test_update_todo_not_found(test_todo):
    request_data = {
        'title':"Hey",
        "description": 'Need to learn everyday!',
        'priority': 3,
        'complete': False
    }   
    response = client.put("todo/999",json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not found.'}
    
def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    
def test_delete_todo(test_todo):
    response = client.delete('/todo/1')
    assert response.status_code == 404
    assert response.json() == {'detail':'Todo not found'}
