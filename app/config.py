"""
Configuration management for MESILSAN MES Application.
This module provides centralized configuration for different environments.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui_mes_2024')
    
    # Database - MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'mesilsan_db')
    MYSQL_USERNAME = os.getenv('MYSQL_USERNAME', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    
    # Application Settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    
class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Use in-memory SQLite for testing
    MYSQL_DATABASE = ':memory:'

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on FLASK_ENV environment variable."""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default'])