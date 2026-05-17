import logging
from flask import Blueprint, jsonify
from database import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    Verifies that the application is running and the database is reachable.
    """
    status = {
        "status": "healthy",
        "database": "connected"
    }
    
    try:
        # Simple ping to database
        db.session.execute(text('SELECT 1'))
        logger.info("Health check passed.")
        return jsonify(status), 200
    except Exception as e:
        status["status"] = "unhealthy"
        status["database"] = "disconnected"
        logger.error(f"Health check failed: {str(e)}")
        return jsonify(status), 503
