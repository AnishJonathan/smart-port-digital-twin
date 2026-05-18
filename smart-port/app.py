import os
from flask import Flask, redirect, url_for, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from config import get_config
from database import db
from models.user import User
from utils.logging_setup import setup_logging
from utils.seeding import seed_users
from utils.filters import time_ago
from services.simulation import run_simulation
from apscheduler.schedulers.background import BackgroundScheduler

# Load environment variables
load_dotenv()

# Setup structured logging
setup_logging()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Initialize Migrate
migrate = Migrate()

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
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Register blueprints (to be created next)
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.health import health_bp
    from routes.ships import ships_bp
    from routes.containers import containers_bp
    from routes.cranes import cranes_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(ships_bp, url_prefix='/ships')
    app.register_blueprint(containers_bp, url_prefix='/containers')
    app.register_blueprint(cranes_bp, url_prefix='/cranes')
    
    # Register Jinja filters
    app.jinja_env.filters['time_ago'] = time_ago
    
    # Default route
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
        
    # Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500
        
    # Attempt to seed users (will safely fail if DB migrations haven't run)
    seed_users(app)
    
    # Start Background Scheduler for Simulation
    # Ensure it only runs once in a production environment (Gunicorn often forks, so locking/Redis might be needed later)
    # For Phase 2, a simple BackgroundScheduler is sufficient.
    if not hasattr(app, 'scheduler_started'):
        scheduler = BackgroundScheduler()
        # Pass app to the job so it has the context
        scheduler.add_job(func=run_simulation, args=[app], trigger="interval", seconds=10)
        scheduler.start()
        app.scheduler_started = True
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', True))
