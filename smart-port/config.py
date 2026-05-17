import os
import socket
from pathlib import Path

# Base directory of the application
BASE_DIR = Path(__file__).resolve().parent

def is_mysql_available(host, port):
    """
    Check if MySQL is available by attempting a socket connection.
    This provides an automatic fallback to SQLite for local development.
    """
    if not host or not port:
        return False
    try:
        with socket.create_connection((host, int(port)), timeout=1):
            return True
    except (OSError, ValueError):
        return False

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session config
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_pass = os.environ.get('MYSQL_PASSWORD')
        mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
        mysql_port = os.environ.get('MYSQL_PORT', '3306')
        mysql_db = os.environ.get('MYSQL_DB')
        
        # Try to use MySQL if it's available and configured
        if mysql_user and mysql_pass and mysql_db and is_mysql_available(mysql_host, mysql_port):
            return f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}"
        
        # Fallback to SQLite for development convenience
        print("WARNING: MySQL is unavailable or not fully configured. Falling back to SQLite.")
        sqlite_path = os.path.join(BASE_DIR, 'instance', 'smartport_dev.sqlite')
        # Ensure instance directory exists
        os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
        return f"sqlite:///{sqlite_path}"

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # In production, we strictly require MySQL. No SQLite fallback.
        mysql_user = os.environ.get('MYSQL_USER')
        mysql_pass = os.environ.get('MYSQL_PASSWORD')
        mysql_host = os.environ.get('MYSQL_HOST')
        mysql_port = os.environ.get('MYSQL_PORT', '3306')
        mysql_db = os.environ.get('MYSQL_DB')
        
        if not all([mysql_user, mysql_pass, mysql_host, mysql_db]):
            raise ValueError("MySQL configuration is missing in the production environment.")
            
        return f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}"

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Dictionary to map environment name to config class
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

def get_config():
    env = os.environ.get('FLASK_ENV', 'development').lower()
    return config_by_name.get(env, DevelopmentConfig)()
