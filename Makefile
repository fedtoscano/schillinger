.PHONY: install install-dev test lint format clean run docs setup-dev

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Development
setup-dev: install-dev
	pre-commit install

# Testing
test:
	pytest src/tests/ -v --cov=src/schillinger --cov-report=html --cov-report=term-missing

test-unit:
	pytest src/tests/unit/ -v

test-integration:
	pytest src/tests/integration/ -v

test-e2e:
	pytest src/tests/e2e/ -v

# Code Quality
lint:
	flake8 src/
	mypy src/

format:
	black src/
	isort src/

check-format:
	black --check src/
	isort --check-only src/

# Cleaning
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf dist/ build/ .eggs/

# Running
run:
	python -m schillinger.main

run-old:
	python main.py

# Documentation
docs:
	@echo "Documentation generation not yet implemented"

# Development utilities
update-deps:
	pip-compile --upgrade pyproject.toml
	pip-compile --upgrade --extra dev pyproject.toml

shell:
	python -c "from schillinger.infrastructure.config.container import Container; c = Container(); print('Container loaded successfully')"

# CI/CD
ci: lint test
	@echo "CI checks passed!"

# Help
help:
	@echo "Available commands:"
	@echo "  install          - Install package"
	@echo "  install-dev      - Install with development dependencies"
	@echo "  setup-dev        - Setup development environment"
	@echo "  test             - Run all tests with coverage"
	@echo "  test-unit        - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-e2e         - Run end-to-end tests only"
	@echo "  lint             - Run linting and type checking"
	@echo "  format           - Format code"
	@echo "  check-format     - Check code formatting"
	@echo "  clean            - Clean build artifacts"
	@echo "  run              - Run the application"
	@echo "  run-old          - Run the old application"
	@echo "  docs             - Generate documentation"
	@echo "  update-deps      - Update dependencies"
	@echo "  shell            - Start Python shell with container"
	@echo "  ci               - Run CI checks"
	@echo "  help             - Show this help"