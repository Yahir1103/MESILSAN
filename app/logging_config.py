"""
Logging configuration for MESILSAN application.
Provides centralized logging setup with different levels and handlers.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

def setup_logging(app):
    """Set up logging for the Flask application."""
    
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure logging level
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    app.logger.setLevel(getattr(logging, log_level.upper()))
    
    # File handler for general logs
    file_handler = RotatingFileHandler(
        'logs/mesilsan.log',
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # File handler for errors
    error_handler = RotatingFileHandler(
        'logs/mesilsan_errors.log',
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    
    # Console handler for development
    console_handler = logging.StreamHandler()
    
    # Formatters
    detailed_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s'
    )
    
    # Apply formatters
    file_handler.setFormatter(detailed_formatter)
    error_handler.setFormatter(detailed_formatter)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to app logger
    if not app.debug:  # Don't add file handlers in debug mode
        app.logger.addHandler(file_handler)
        app.logger.addHandler(error_handler)
    
    app.logger.addHandler(console_handler)
    
    # Log startup
    app.logger.info(f'MESILSAN application startup - {datetime.now()}')

def log_database_error(app, error, operation="database operation"):
    """Log database-related errors with context."""
    app.logger.error(f"Database error during {operation}: {str(error)}")
    if app.debug:
        app.logger.debug(f"Database error details: {repr(error)}")

def log_security_event(app, event_type, user_info=None, additional_info=None):
    """Log security-related events."""
    message = f"Security event - {event_type}"
    if user_info:
        message += f" - User: {user_info}"
    if additional_info:
        message += f" - Details: {additional_info}"
    
    app.logger.warning(message)

def log_performance_metric(app, operation, duration_ms, additional_data=None):
    """Log performance metrics for monitoring."""
    message = f"Performance - {operation}: {duration_ms}ms"
    if additional_data:
        message += f" - Data: {additional_data}"
    
    app.logger.info(message)