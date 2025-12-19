from app import app
from flask import Flask
from typing import Generator
import pytest

@pytest.fixture(scope="function")

def client()->Generator:
    """Create a test client for application"""

    app.config['TESTING']=True
    app.config['WTF_CSRF_ENABLED']=False
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

class TestProfileEndpoint:
    """Test suite for /profile endpoint authentication and authorization."""

    def test_profile_authenticated_user_success(self,client):
        """Test successfull profile access authenticated user"""
        response=client.get('/profile?username=admin&login_status=true')
        data=response.get_json()

        assert response.status_code==200
        assert data['response']=='Welcome to your profile page'

    def test_profile_unauthenticated_user_denied(self,client):
        "Test successfull profile access unauthenticates user"
        response=client.get('/profile?username=admin&login_status=false')
        data=response.get_json()

        assert response.status_code==200
        assert data['response']=='Please login to access your profile'

    def test_profile_missing_username_parameter(self,client):
        """Test profile access with missing username parameter"""
        response=client.get('/profile?status=true')
        data=response.get_json()

        assert response.status_code==200
        assert data['response']=="Please login to access your profile"

    def test_profile_missing_loginstatus_parameter(self,client):
        """Test profile access with missing username parameter"""
        response=client.get("/profile?username=admin")
        data=response.get_json()

        assert response.status_code==200
        assert data['response']=="Please login to access your profile"

    def test_profile_no_parameters(self, client):
        """
        Test profile access with no parameters provided.
        """
        response = client.get("/profile")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["response"] == "Please login to access your profile"


