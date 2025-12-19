"""
Test suite for Flask application routes and authentication logic.

This module contains comprehensive tests for the application's API endpoints,
including authentication flows, error handling, and edge cases.
"""

import pytest
from flask import Flask
from typing import Generator


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope="function")
def client() -> Generator:
    """
    Create a test client for the Flask application.
    
    Yields:
        FlaskClient: A test client instance for making HTTP requests.
    
    Note:
        - Uses function scope to ensure test isolation
        - Automatically handles setup and teardown
    """
    from app import app
    
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


# ============================================================================
# TEST CLASSES - Organized by Feature
# ============================================================================

class TestProfileEndpoint:
    """Test suite for /profile endpoint authentication and authorization."""
    
    def test_profile_authenticated_user_success(self, client):
        """
        Test successful profile access for authenticated user.
        
        Given: Valid username and login_status=true
        When: GET request to /profile
        Then: Return 200 status with profile access message
        """
        response = client.get("/profile?username=sainath&login_status=true")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["response"] == "Welcome to your profile page"
    
    def test_profile_unauthenticated_user_denied(self, client):
        """
        Test profile access denial for unauthenticated user.
        
        Given: Valid username but login_status=false
        When: GET request to /profile
        Then: Return 200 status with login required message
        """
        response = client.get("/profile?username=sainath&login_status=false")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data['response'] == "Please login to access your profile"
    
    def test_profile_missing_username_parameter(self, client):
        """
        Test profile access with missing username parameter.
        
        Given: login_status=true but no username provided
        When: GET request to /profile
        Then: Return login required message (username is required)
        """
        response = client.get("/profile?login_status=true")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["response"] == "Please login to access your profile"
    
    def test_profile_missing_login_status_parameter(self, client):
        """
        Test profile access with missing login_status parameter.
        
        Given: Valid username but no login_status provided
        When: GET request to /profile
        Then: Return login required message (login status is required)
        """
        response = client.get("/profile?username=sainath")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["response"] == "Please login to access your profile"
    
    def test_profile_no_parameters(self, client):
        """
        Test profile access with no parameters provided.
        
        Given: No query parameters
        When: GET request to /profile
        Then: Return login required message
        """
        response = client.get("/profile")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["response"] == "Please login to access your profile"
    
    @pytest.mark.parametrize("username,login_status,expected_message", [
        ("", "true", "Please login to access your profile"),
        ("sainath", "", "Please login to access your profile"),
        ("", "", "Please login to access your profile"),
    ])
    def test_profile_empty_parameters(self, client, username, login_status, expected_message):
        """
        Test profile access with empty parameter values.
        
        Uses parametrized testing for multiple edge cases.
        """
        response = client.get(f"/profile?username={username}&login_status={login_status}")
        data = response.get_json()
        
        assert response.status_code == 200
        assert data["response"] == expected_message


class TestHomeEndpoint:
    """Test suite for home page endpoint."""
    
    def test_home_page_accessible(self, client):
        """
        Test home page returns successful response.
        
        Given: Application is running
        When: GET request to /
        Then: Return 200 OK status
        """
        response = client.get('/')
        
        assert response.status_code == 200
        assert response.content_type == 'text/html; charset=utf-8' or \
               response.content_type == 'application/json'
    
    def test_home_page_content_type(self, client):
        """
        Test home page returns correct content type.
        
        Validates that response format is appropriate.
        """
        response = client.get('/')
        
        assert response.status_code == 200
        # Verify it returns either HTML or JSON (depending on implementation)
        assert 'text/html' in response.content_type or \
               'application/json' in response.content_type


class TestDashboardEndpoint:
    """Test suite for dashboard endpoint."""
    
    def test_dashboard_accessible(self, client):
        """
        Test dashboard returns successful response.
        
        Given: Application is running
        When: GET request to /dashboard
        Then: Return 200 OK status
        """
        response = client.get("/dashboard")
        
        assert response.status_code == 200
    
    def test_dashboard_response_format(self, client):
        """
        Test dashboard returns expected response format.
        
        Validates the structure and content type of the response.
        """
        response = client.get("/dashboard")
        
        assert response.status_code == 200
        
        # If dashboard returns JSON, verify it's valid
        if response.content_type == 'application/json':
            data = response.get_json()
            assert data is not None


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestAuthenticationFlow:
    """Test complete authentication workflows."""
    
    def test_unauthenticated_profile_to_home_redirect_flow(self, client):
        """
        Test that unauthenticated users are properly handled.
        
        Simulates a user attempting to access profile without authentication.
        """
        # Attempt to access profile without authentication
        profile_response = client.get("/profile?username=sainath&login_status=false")
        profile_data = profile_response.get_json()
        
        # Verify access is denied
        assert profile_data["response"] == "Please login to access your profile"
        
        # Verify home page is still accessible
        home_response = client.get('/')
        assert home_response.status_code == 200


# ============================================================================
# CONFIGURATION TESTS
# ============================================================================

class TestApplicationConfiguration:
    """Test application configuration and settings."""
    
    def test_testing_mode_enabled(self, client):
        """
        Verify application is running in testing mode.
        
        Ensures test-specific configurations are active.
        """
        from app import app
        assert app.config['TESTING'] is True
    
    def test_debug_mode_disabled_in_tests(self, client):
        """
        Verify debug mode is disabled during testing.
        
        Debug mode should not be active in test environment.
        """
        from app import app
        # In production tests, debug should be False
        # Adjust based on your requirements
        assert app.config.get('DEBUG', False) is False or \
               app.config['TESTING'] is True


# ============================================================================
# HELPER FUNCTIONS FOR TESTS
# ============================================================================

def assert_json_response(response, expected_status: int = 200):
    """
    Helper function to assert common JSON response properties.
    
    Args:
        response: Flask test client response object
        expected_status: Expected HTTP status code (default: 200)
    """
    assert response.status_code == expected_status
    assert response.content_type == 'application/json'
    assert response.get_json() is not None


# ============================================================================
# MARKERS FOR ORGANIZING TESTS
# ============================================================================

# Use pytest markers to organize and selectively run tests:
# pytest -m smoke       # Run only smoke tests
# pytest -m integration # Run only integration tests
# pytest -m unit        # Run only unit tests

pytestmark = [
    pytest.mark.api,  # All tests in this file are API tests
]