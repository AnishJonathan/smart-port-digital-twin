from models.user import User
from models.ship import Ship
from models.container import Container
from models.crane import Crane
from models.audit import AuditLog
from database import db
import random

def seed_users(app):
    """Seed initial demo users, ships, containers, cranes, and audit logs."""
    
    with app.app_context():
        try:
            # 1. Seed Users
            if not User.query.first():
                users = [
                    User(name='Admin', email='admin@smartport.com', role='Admin'),
                    User(name='Port Manager', email='manager@smartport.com', role='Port Manager'),
                    User(name='Logistics Officer', email='logistics@smartport.com', role='Logistics Officer')
                ]
                
                users[0].set_password('admin123')
                users[1].set_password('manager123')
                users[2].set_password('logistics123')
                
                db.session.add_all(users)
                db.session.commit()
                print("Demo Users seeded.")
                
            # 2. Seed Ships
            if not Ship.query.first():
                ship_names = ['MV Atlantic', 'Ocean Titan', 'Harbor Queen', 'Nordic Voyager', 'Pacific Star', 
                              'Evergreen Titan', 'Baltic Horizon', 'PortLink Express', 'Ocean Vanguard', 'MSC Aurora']
                destinations = ['Rotterdam', 'Singapore', 'Shanghai', 'Los Angeles', 'Hamburg']
                statuses = ['Arrived', 'Docked', 'Loading', 'Unloading', 'Departed', 'Delayed']
                
                ships = []
                for name in ship_names:
                    ship = Ship(
                        ship_name=name,
                        destination=random.choice(destinations),
                        cargo_capacity=random.randint(50, 500),
                        status=random.choice(statuses),
                        fuel_level=round(random.uniform(20.0, 100.0), 1)
                    )
                    ships.append(ship)
                
                db.session.add_all(ships)
                db.session.commit()
                print("Demo Ships seeded.")
                
                # 3. Seed Containers
                if not Container.query.first():
                    locations = ['Yard A', 'Yard B', 'Dock 1', 'Dock 2']
                    c_statuses = ['Received', 'In Yard', 'Loading', 'In Transit', 'Delivered']
                    priorities = ['Standard', 'High', 'Critical']
                    
                    containers = []
                    for i in range(1, 31):
                        # Optionally assign to a random ship
                        assign_ship = random.choice([True, False])
                        ship_id = random.choice(ships).id if assign_ship else None
                        
                        c = Container(
                            container_id=f"CONT-{1000+i}",
                            location=random.choice(locations),
                            destination=random.choice(destinations),
                            status=random.choice(c_statuses),
                            priority=random.choice(priorities),
                            weight=round(random.uniform(500.0, 5000.0), 2),
                            ship_id=ship_id
                        )
                        containers.append(c)
                        
                    db.session.add_all(containers)
                    db.session.commit()
                    print("Demo Containers seeded.")
                    
            # 4. Seed Cranes
            if not Crane.query.first():
                crane_names = ['Crane Alpha', 'Crane Beta', 'Crane Gamma', 'Crane Delta', 'Crane Epsilon']
                crane_statuses = ['Active', 'Idle', 'Maintenance', 'Fault']
                
                cranes = []
                for name in crane_names:
                    c = Crane(
                        crane_name=name,
                        status=random.choice(crane_statuses),
                        temperature=random.randint(30, 85),
                        health_score=random.randint(60, 100)
                    )
                    cranes.append(c)
                    
                db.session.add_all(cranes)
                db.session.commit()
                print("Demo Cranes seeded.")
                
            # 5. Seed initial Audit Logs for activity feed realism
            if not AuditLog.query.first():
                logs = [
                    AuditLog(user='System', action='System Initialized', target='Smart Port Platform'),
                    AuditLog(user='Admin', action='Created Ship', target='MSC Aurora'),
                    AuditLog(user='Port Manager', action='Updated Ship Status (Docked → Loading)', target='Ocean Titan'),
                    AuditLog(user='Logistics Officer', action='Updated Container Status (In Yard → Loading)', target='CONT-1015'),
                    AuditLog(user='Admin', action='Registered Crane', target='Crane Alpha')
                ]
                db.session.add_all(logs)
                db.session.commit()
                print("Demo Audit Logs seeded.")
                
        except Exception as e:
            # Safely catch missing tables before migration runs
            print(f"Skipping seeding: {e}")
