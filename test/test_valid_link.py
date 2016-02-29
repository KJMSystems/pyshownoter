import pytest
from app.url_parser import tld
from app.url_parser import check_tld

def test_tld_contains_info():
    assert tld

@pytest.fixture
def test_var():
    test_var = 'asd'
    return test_var

def test_tld_doesnt_contain_test_variables(test_var):
    assert test_var not in tld
    
    
def test_tlds_not_in_check_tld(test_var):
    assert check_tld(test_var) == False

def test_actual_tld_returns_true():
    print(check_tld('com'))
    assert check_tld('com') == True
