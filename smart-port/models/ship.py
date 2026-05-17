from database import db
from datetime import datetime

class Ship(db.Model):
    __tablename__ = 'ships'

    id = db.Column(db.Integer, primary_key=True)
    ship_name = db.Column(db.String(100), nullable=False, index=True)
    arrival_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    destination = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Arriving') # Docked, Arriving, Departed, Delayed
    fuel_level = db.Column(db.Float, nullable=False, default=100.0) # percentage
    cargo_capacity = db.Column(db.Integer, nullable=False) # max containers
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    containers = db.relationship('Container', backref='ship', lazy=True)

    def __repr__(self):
        return f'<Ship {self.ship_name} ({self.status})>'
