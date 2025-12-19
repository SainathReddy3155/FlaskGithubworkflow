import unittest
from app import app
import pytest



@pytest.fixture
def client():
    with app.test_client() as client:
        yield client



def test_profile_sucess(client):
    response=client.get("/profile?username=sainath&login_status=true")
    data=response.get_json()
    assert response.status_code==200
    assert data["response"]=="Welcome to your profile page"

def test_profile_failure(client):
    response=client.get("/profile?username=sainath&login_status=false")
    data=response.get_json()
    assert response.status_code==200
    assert data['response'] == "Please login to access your profile"

def test_username_notfound(client):
    response=client.get("/profile?login_status=true")
    data=response.get_json()
    assert response.status_code==200
    assert data["response"]=="Please login to access your profile"

def test_login_status_notfound(client):
    response=client.get("/profile?username=sainath")
    data=response.get_json()
    assert response.status_code==200
    assert data["response"]=="Please login to access your profile"

def test_home():
    print("In Test")
    response = app.test_client().get('/')
    assert response.status_code == 200

def test_dashboard_route():
    client=app.test_client()
    response=client.get("/dashboard")
    assert response.status_code==200

