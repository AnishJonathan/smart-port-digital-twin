import os
from flask import Flask, redirect, url_for
from flask_login import LoginManager
from dotenv import load_dotenv

from config import get_config
from database import db
from models.user import User

# Load environment variables
load_dotenv()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_class=None):
    """
    Application factory for the Smart Port Digital Twin Platform.
    Initializes Flask, extensions, and blueprints.
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_class is None:
        app.config.from_object(get_config())
    else:
        app.config.from_object(config_class)
        
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints (to be created next)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    
    # Default route
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
        
    # Create tables automatically for development convenience
    with app.app_context():
        try:
            db.create_all()
            # Optionally create a default admin user if none exists
            if not User.query.filter_by(email='admin@smartport.com').first():
                admin = User(
                    name='System Admin',
                    email='admin@smartport.com',
                    role='Admin'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Default admin user created: admin@smartport.com / admin123")
        except Exception as e:
            print(f"Error initializing database: {e}")
            
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', True))
