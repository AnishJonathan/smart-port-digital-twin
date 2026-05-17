import multiprocessing

# Gunicorn configuration file for production
# https://docs.gunicorn.org/en/stable/settings.html

# Socket binding
bind = "0.0.0.0:8000"

# Worker management
# Recommended formula for workers: (2 x $num_cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync" # Change to 'gthread', 'gevent' if async needed
threads = 2

# Timeouts
timeout = 120
keepalive = 5

# Logging setup (handled mostly by utils/logging_setup.py to output JSON)
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Preload application to save memory and boot faster
preload_app = True
