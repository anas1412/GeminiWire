import logging
from logging.handlers import TimedRotatingFileHandler

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log format
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# File handler with rotation
file_handler = TimedRotatingFileHandler(
    filename="app.log",  # Base log file name
    when="midnight",     # Rotate logs daily at midnight
    interval=1,          # Rotate every day
    backupCount=0,       # Keep 0 backup logs (only today's logs)
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)