from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from datetime import datetime

class User(UserMixin, db.Model):
    """
    User model for the Smart Port platform.
    Handles authentication and role-based access.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='Logistics Officer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Allowed Roles: 'Admin', 'Port Manager', 'Logistics Officer'

    def set_password(self, password):
        """Hashes the password and sets it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'Admin'

    def is_port_manager(self):
        return self.role == 'Port Manager'

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
