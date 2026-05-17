import pytest
from app import create_app
from database import db
from models.user import User

@pytest.fixture
def app():
    # Setup testing app configuration
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'test'
        WTF_CSRF_ENABLED = False

    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Test the /health endpoint"""
    response = client.get('/health/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['database'] == 'connected'

def test_login_page_renders(client):
    """Test that the login page renders successfully"""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Smart Port Platform' in response.data
    
def test_dashboard_redirects_if_unauthenticated(client):
    """Test dashboard route protection"""
    response = client.get('/dashboard/')
    assert response.status_code == 302 # Redirect to login
