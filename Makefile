# MESILSAN Development Makefile
# Provides common development tasks

.PHONY: help setup test lint serve status clean install

# Default target
help:
	@echo "MESILSAN Development Commands:"
	@echo "  setup    - Set up development environment"
	@echo "  install  - Install dependencies"
	@echo "  test     - Run tests"
	@echo "  lint     - Run code linting"
	@echo "  serve    - Start development server"
	@echo "  status   - Show project status"
	@echo "  clean    - Clean up build artifacts"
	@echo ""
	@echo "Alternative: Use python dev.py <command>"

# Set up development environment
setup:
	python dev.py setup

# Install dependencies
install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Run tests
test:
	python dev.py test

# Run linting
lint:
	python dev.py lint

# Start development server
serve:
	python dev.py serve

# Show project status
status:
	python dev.py status

# Clean up build artifacts
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	@echo "✅ Build artifacts cleaned"

# Quick setup for new developers
quick-start: setup test
	@echo "🚀 Quick start complete! Run 'make serve' to start the server."