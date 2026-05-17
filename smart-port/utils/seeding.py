from database import db
from models.user import User
from sqlalchemy.exc import OperationalError

def seed_users(app):
    """
    Seeds default users if the database is empty.
    Should be called within the application context.
    """
    with app.app_context():
        try:
            # Check if any user exists
            if User.query.first() is None:
                print("Database is empty. Seeding default users...")
                
                users_data = [
                    {"name": "System Admin", "email": "admin@smartport.com", "password": "admin123", "role": "Admin"},
                    {"name": "Port Manager", "email": "manager@smartport.com", "password": "manager123", "role": "Port Manager"},
                    {"name": "Logistics Officer", "email": "logistics@smartport.com", "password": "logistics123", "role": "Logistics Officer"}
                ]
                
                for data in users_data:
                    user = User(name=data['name'], email=data['email'], role=data['role'])
                    user.set_password(data['password'])
                    db.session.add(user)
                    
                db.session.commit()
                print("Successfully seeded Admin, Port Manager, and Logistics Officer.")
        except OperationalError:
            # Tables might not be created yet (before migrations run)
            pass
        except Exception as e:
            print(f"Error during seeding: {e}")
