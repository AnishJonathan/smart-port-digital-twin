from database import db
from datetime import datetime

class Crane(db.Model):
    __tablename__ = 'cranes'

    id = db.Column(db.Integer, primary_key=True)
    crane_name = db.Column(db.String(100), nullable=False, unique=True)
    temperature = db.Column(db.Float, nullable=False, default=40.0) # in Celsius
    load_capacity = db.Column(db.Float, nullable=False, default=0.0) # percentage 0-100
    status = db.Column(db.String(50), nullable=False, default='Idle') # Active, Idle, Maintenance, Fault
    health_score = db.Column(db.Float, nullable=False, default=100.0) # 0-100 scale
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Crane {self.crane_name} ({self.status})>'
