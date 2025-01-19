# Single import statement for logging module
import logging

# Configure logging with optimized settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Optimize date format
)

# Get logger instance for current module
logger = logging.getLogger(__name__)
