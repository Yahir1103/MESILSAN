#!/usr/bin/env python3
"""
Development helper script for MESILSAN project.
Provides common development tasks in a single script.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description=""):
    """Run a command and handle errors."""
    print(f"{'='*50}")
    print(f"Running: {description or command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=False, text=True)
        print(f"✅ Success: {description or command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {description or command}")
        print(f"Error: {e}")
        return False

def setup_environment():
    """Set up the development environment."""
    print("🚀 Setting up MESILSAN development environment...")
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("📝 Creating .env file from template...")
        if os.path.exists('.env.example'):
            run_command('cp .env.example .env', 'Copy environment template')
            print("⚠️  Please edit .env file with your actual configuration!")
        else:
            print("❌ .env.example not found!")
            return False
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if not run_command('pip install -r requirements.txt', 'Install Python dependencies'):
        return False
    
    print("✅ Environment setup complete!")
    return True

def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    
    # Run basic tests
    if not run_command('python tests/test_basic.py', 'Run basic tests'):
        return False
    
    # Run all tests in tests directory
    print("\n🔍 Running all tests...")
    if not run_command('python -m unittest discover tests/', 'Run all tests'):
        print("⚠️  Some tests failed or no additional tests found")
    
    print("✅ Tests completed!")
    return True

def lint_code():
    """Run code linting."""
    print("🔍 Running code linting...")
    
    # Check if flake8 is available
    try:
        subprocess.run(['flake8', '--version'], capture_output=True, check=True)
        run_command('flake8 app/', 'Lint application code')
        run_command('flake8 tests/', 'Lint test code')
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  flake8 not installed. Install with: pip install flake8")
        print("💡 Using basic Python syntax check instead...")
        run_command('python -m py_compile app/*.py', 'Check Python syntax')
    
    return True

def start_development_server():
    """Start the development server."""
    print("🌐 Starting development server...")
    
    # Check environment
    if not os.path.exists('.env'):
        print("❌ .env file not found! Run 'python dev.py setup' first.")
        return False
    
    print("🚀 Starting Flask development server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        os.environ['FLASK_ENV'] = 'development'
        subprocess.run(['python', 'run.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def show_status():
    """Show project status and health checks."""
    print("📊 MESILSAN Project Status")
    print("="*40)
    
    # Check Python version
    print(f"🐍 Python version: {sys.version}")
    
    # Check if virtual environment is active
    venv = os.environ.get('VIRTUAL_ENV')
    if venv:
        print(f"📦 Virtual environment: {venv}")
    else:
        print("⚠️  No virtual environment detected")
    
    # Check required files
    required_files = ['.env', 'requirements.txt', 'run.py', 'app/routes.py']
    for file in required_files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"{status} {file}")
    
    # Check if app can be imported
    try:
        sys.path.insert(0, os.getcwd())
        from app.routes import app
        print("✅ Application imports successfully")
        print(f"🔑 Secret key configured: {bool(app.secret_key)}")
    except Exception as e:
        print(f"❌ Application import failed: {e}")
    
    # Check database connectivity
    try:
        from app.db import test_database_connection
        if test_database_connection():
            print("✅ Database connection working")
        else:
            print("⚠️  Database connection issues (using SQLite fallback)")
    except Exception as e:
        print(f"⚠️  Database check failed: {e}")
    
    print("\n💡 Use 'python dev.py --help' for available commands")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='MESILSAN Development Helper')
    parser.add_argument('command', choices=['setup', 'test', 'lint', 'serve', 'status'], 
                       help='Command to run')
    
    args = parser.parse_args()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    if args.command == 'setup':
        setup_environment()
    elif args.command == 'test':
        run_tests()
    elif args.command == 'lint':
        lint_code()
    elif args.command == 'serve':
        start_development_server()
    elif args.command == 'status':
        show_status()

if __name__ == '__main__':
    main()