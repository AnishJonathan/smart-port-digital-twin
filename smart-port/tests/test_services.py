import pytest
from services.weather import weather_service
from services.congestion import congestion_engine
from app import create_app
from database import db
from models.ship import Ship

@pytest.fixture
def app_context():
    class TestConfig:
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        SECRET_KEY = 'test'
        
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_weather_fallback():
    # Remove API key to force fallback
    weather_service.api_key = None
    data = weather_service.get_weather()
    assert 'temperature' in data
    assert 'wind_speed' in data
    assert 'condition' in data
    assert 'risk_level' in data
    assert data['risk_level'] in ['Low', 'Medium', 'High']

def test_congestion_engine_calculation(app_context):
    # Base congestion with no entities should be Low or dependent purely on weather mock
    data = congestion_engine.calculate_congestion()
    assert 'score' in data
    assert 'level' in data
    
    # Add a lot of ships to force high congestion
    for i in range(12):
        s = Ship(ship_name=f"Ship{i}", destination="Dest", cargo_capacity=100, status="Docked")
        db.session.add(s)
    db.session.commit()
    
    new_data = congestion_engine.calculate_congestion()
    assert new_data['score'] >= 30 # At least 30 from the >10 ships rule
