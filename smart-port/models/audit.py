from database import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AuditLog {self.user} - {self.action} on {self.target}>'
