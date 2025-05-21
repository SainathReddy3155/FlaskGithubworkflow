import unittest
from app import app


def test_home():
    print("In Test")
    response = app.test_client().get('/')
    assert response.status_code == 200