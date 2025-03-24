from .utils import *
from ..router.auth import get_db,authenticate_user

app.dependency_overrides[get_db] = override_get_db

def test_authentication_user(test_user):
    db = TestingSessionLocal()
    
    authenticated_user = authenticate_user(test_user.username,"test1234",db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    
def test_authentication_wrong_user(test_user):
    db = TestingSessionLocal()
    
    authenticated_user = authenticate_user(test_user.username,"test1234",db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    
    non_existent_user = authenticate_user('WrongUserName',"testpassword",db)
    assert non_existent_user is False
    wrong_password_user = authenticate_user(test_user.username,"wrongpass",db)
    assert wrong_password_user is False
