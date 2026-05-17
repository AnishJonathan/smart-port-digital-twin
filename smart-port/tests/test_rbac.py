import pytest
from app import create_app
from database import db
from models.user import User

@pytest.fixture
def client():
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'test'
        WTF_CSRF_ENABLED = False

    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        # Create test users
        admin = User(name='Admin', email='admin@test.com', role='Admin')
        admin.set_password('pass')
        manager = User(name='Manager', email='manager@test.com', role='Port Manager')
        manager.set_password('pass')
        officer = User(name='Officer', email='officer@test.com', role='Logistics Officer')
        officer.set_password('pass')
        
        db.session.add_all([admin, manager, officer])
        db.session.commit()
        
        yield app.test_client()
        
        db.session.remove()
        db.drop_all()

def login(client, email, password):
    return client.post('/auth/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def test_admin_access_cranes(client):
    login(client, 'admin@test.com', 'pass')
    response = client.get('/cranes/')
    assert response.status_code == 200

def test_manager_access_ships(client):
    login(client, 'manager@test.com', 'pass')
    response = client.post('/ships/add', data=dict(ship_name='Test Ship', destination='Test', cargo_capacity=100))
    # Should redirect on success
    assert response.status_code == 302

def test_officer_denied_ship_add(client):
    login(client, 'officer@test.com', 'pass')
    response = client.post('/ships/add', data=dict(ship_name='Test Ship', destination='Test', cargo_capacity=100))
    # Logistics Officer is NOT allowed to add ships
    assert response.status_code == 403
