from database import db
from datetime import datetime

class Container(db.Model):
    __tablename__ = 'containers'

    id = db.Column(db.Integer, primary_key=True)
    container_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    location = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Received') # Received, In Yard, Loading, In Transit, Delivered
    destination = db.Column(db.String(100), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Standard') # Standard, High, Critical
    weight = db.Column(db.Float, nullable=False) # in tons
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Container {self.container_id} ({self.status})>'
