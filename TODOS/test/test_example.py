import pytest

def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1
    
class Student:
    def __init__(self,first_name:str,last_name:str,major:str,years:int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def default_employee():
    return Student('Anand','Reddy','Artificial Intelligence',2)

def test_person_initialization(default_employee):
    p = Student('Anand','Reddy','Artificial Intelligence',2)
    # assert p.first_name == 'Anand','First Name'
    # assert p.last_name == 'Reddy','Last Name'
    # assert p.major == 'Artificial Intelligence'
    # assert p.years == 2    
    assert default_employee.first_name == 'Anand','First Name'
    assert default_employee.last_name == 'Reddy','Last Name'
    assert default_employee.major == 'Artificial Intelligence'
    assert default_employee.years == 2
