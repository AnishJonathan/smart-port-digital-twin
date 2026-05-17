import logging
import json
import sys
from datetime import datetime

class JSONFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.
    Ideal for Docker and cloud logging aggregators (e.g. AWS CloudWatch, ELK).
    """
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

def setup_logging():
    """
    Configures the root logger to output structured JSON to stdout.
    """
    root_logger = logging.getLogger()
    # Set default level
    root_logger.setLevel(logging.INFO)
    
    # Remove any existing handlers
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)
            
    # Create console handler for stdout (standard for Docker)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    
    root_logger.addHandler(console_handler)
    
    # Configure gunicorn loggers to use this format if running under gunicorn
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger.handlers:
        app_logger = logging.getLogger('werkzeug')
        app_logger.setLevel(gunicorn_logger.level)
        for handler in gunicorn_logger.handlers:
            handler.setFormatter(JSONFormatter())
