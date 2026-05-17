import logging
import random
from datetime import datetime
from database import db
from models.crane import Crane
from models.ship import Ship
from models.audit import AuditLog
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
            
            # Run congestion logic to trigger alerts internally
            congestion_data = congestion_engine.calculate_congestion()
            if congestion_data['level'] in ['High', 'Critical']:
                logger.warning(f"SIMULATION ALERT: {congestion_data['alert']}")
                
                # Check if we should log it to audit (to avoid spamming, only if last log wasn't this)
                last_log = AuditLog.query.order_by(AuditLog.timestamp.desc()).first()
                if not last_log or last_log.action != f"Congestion Alert: {congestion_data['level']}":
                    audit = AuditLog(user="System (Simulation)", action=f"Congestion Alert: {congestion_data['level']}", target="Smart Port")
                    db.session.add(audit)
                    
            else:
                logger.info(f"Simulation tick. Congestion Level: {congestion_data['level']}")
                
            db.session.commit()
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
                crane.health_score = max(0, crane.health_score - 5)
                if crane.status != 'Fault':
                    crane.status = 'Fault'
                    audit = AuditLog(user="System (Simulation)", action="Crane Fault Detected", target=crane.crane_name)
                    db.session.add(audit)
            else:
                # Slowly recover health if normal
                crane.health_score = min(100, crane.health_score + 1)
                if crane.status == 'Fault' and crane.temperature < 70.0:
                    crane.status = 'Idle'
                    audit = AuditLog(user="System (Simulation)", action="Crane Recovered", target=crane.crane_name)
                    db.session.add(audit)

def _simulate_ships():
    ships = Ship.query.filter(Ship.status.in_(['Arrived', 'Docked', 'Loading', 'Unloading'])).all()
    for ship in ships:
        # Decrease fuel
        ship.fuel_level = max(0.0, ship.fuel_level - random.uniform(0.1, 1.0))
        
        # Random status progression
        old_status = ship.status
        
        if ship.status == 'Arrived' and random.random() < 0.2:
            ship.status = 'Docked'
        elif ship.status == 'Docked' and random.random() < 0.2:
            ship.status = 'Loading'
        elif ship.status == 'Loading' and random.random() < 0.2:
            ship.status = 'Departed'
        elif ship.status == 'Unloading' and random.random() < 0.2:
            ship.status = 'Departed'
            
        if old_status != ship.status:
            audit = AuditLog(user="System (Simulation)", action=f"Auto-Progressed Status ({old_status} → {ship.status})", target=ship.ship_name)
            db.session.add(audit)
