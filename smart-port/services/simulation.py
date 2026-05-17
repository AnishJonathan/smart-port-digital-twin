import logging
import random
from datetime import datetime
from database import db
from models.crane import Crane
from models.ship import Ship
from services.congestion import congestion_engine

logger = logging.getLogger(__name__)

def run_simulation(app):
    """
    Simulates live port operations.
    Runs within the application context.
    """
    with app.app_context():
        try:
            _simulate_cranes()
            _simulate_ships()
            db.session.commit()
            
            # Run congestion logic to trigger alerts internally
            congestion_data = congestion_engine.calculate_congestion()
            if congestion_data['level'] in ['High', 'Critical']:
                logger.warning(f"SIMULATION ALERT: {congestion_data['alert']}")
            else:
                logger.info(f"Simulation tick. Congestion Level: {congestion_data['level']}")
                
        except Exception as e:
            logger.error(f"Simulation Error: {e}")
            db.session.rollback()

def _simulate_cranes():
    cranes = Crane.query.all()
    for crane in cranes:
        if crane.status != 'Maintenance':
            # Fluctuate temperature
            temp_change = random.uniform(-2.0, 5.0)
            crane.temperature = max(10.0, min(120.0, crane.temperature + temp_change))
            
            # Fluctuate load
            if crane.status == 'Active':
                crane.load_capacity = random.uniform(20.0, 100.0)
            
            # Determine health and faults
            if crane.temperature > 95.0:
                crane.health_score -= 5.0
                crane.status = 'Fault'
            else:
                # Slowly recover health if normal
                crane.health_score = min(100.0, crane.health_score + 1.0)
                if crane.status == 'Fault' and crane.temperature < 70.0:
                    crane.status = 'Idle'

def _simulate_ships():
    ships = Ship.query.filter(Ship.status.in_(['Arriving', 'Docked'])).all()
    for ship in ships:
        # Decrease fuel
        ship.fuel_level = max(0.0, ship.fuel_level - random.uniform(0.1, 1.0))
        
        # Randomly change Arriving to Docked
        if ship.status == 'Arriving' and random.random() < 0.2:
            ship.status = 'Docked'
            
        # Randomly depart
        elif ship.status == 'Docked' and random.random() < 0.1:
            ship.status = 'Departed'
