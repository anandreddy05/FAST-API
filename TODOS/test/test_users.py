from .utils import *
from ..router.users import get_db,get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == "anand@123"
    assert response.json()['email'] == "anand@gmail.com"
    assert response.json()['first_name'] == "Anand"
    assert response.json()['last_name'] == "Reddy"
    assert response.json()['role'] == "admin"
    assert response.json()['phone_number'] == "8074500"

def test_change_password_success(test_user):
    response = client.put("/users/password",json={'password':'test1234',
                                                  "new_password":"newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/password",json={"password":"wrongpassword","new_password":"newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Incorrect current password'}
