
.PHONY: setup
setup :
	@echo "Setting up the development environment..."
	pyenv virtualenv pingouins
	pyenv local pingouins
	pip install -e .
	@echo "✅ Development environment setup complete."

.PHONY: install-test
install-test:
	@echo "Installing test dependencies..."
	pip install -r requirements-test.txt
	@echo "✅ Test dependencies installed."

.PHONY: install-dev
install-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt
	@echo "✅ Development dependencies installed."

.PHONY: pre-commit-install
pre-commit-install:
	@echo "Installing pre-commit hooks..."
	pre-commit install
	@echo "✅ Pre-commit hooks installed."

.PHONY: pre-commit-run
pre-commit-run:
	@echo "Running pre-commit on all files..."
	pre-commit run --all-files

.PHONY: pre-commit-update
pre-commit-update:
	@echo "Updating pre-commit hooks..."
	pre-commit autoupdate

.PHONY: test
test:
	@echo "Running all tests..."
	pytest -v

.PHONY: test-data
test-data:
	@echo "Running data tests..."
	pytest tests/test_data.py -v

.PHONY: test-model
test-model:
	@echo "Running model tests..."
	pytest tests/test_model.py -v

.PHONY: test-registry
test-registry:
	@echo "Running registry tests..."
	pytest tests/test_registry.py -v

.PHONY: test-integration
test-integration:
	@echo "Running integration tests..."
	pytest tests/test_integration.py -v

.PHONY: test-coverage
test-coverage:
	@echo "Running tests with coverage..."
	pytest --cov=src/pengouins --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/index.html"

.PHONY: test-quick
test-quick:
	@echo "Running quick tests (excluding slow tests)..."
	pytest -v -m "not slow"

.PHONY: lint
lint:
	@echo "Running linters..."
	@echo "Running black..."
	black --check src/ tests/
	@echo "Running isort..."
	isort --check-only src/ tests/
	@echo "Running flake8..."
	flake8 --verbose src/ tests/
	@echo "✅ All linting checks passed!"

.PHONY: format
format:
	@echo "Formatting code..."
	black src/ tests/ main.py
	isort src/ tests/ main.py
	@echo "✅ Code formatted!"

.PHONY: type-check
type-check:
	@echo "Running type checks..."
	mypy src/
	@echo "✅ Type checking complete!"

.PHONY: check-all
check-all: lint type-check test
	@echo "✅ All checks passed!"

.PHONY: help
help:
	@echo "Available make targets:"
	@echo ""
	@echo "Setup:"
	@echo "  setup              - Set up development environment"
	@echo "  install-test       - Install test dependencies"
	@echo "  install-dev        - Install development dependencies (includes test)"
	@echo "  pre-commit-install - Install pre-commit hooks"
	@echo ""
	@echo "Testing:"
	@echo "  test               - Run all tests"
	@echo "  test-data          - Run data module tests"
	@echo "  test-model         - Run model module tests"
	@echo "  test-registry      - Run registry module tests"
	@echo "  test-integration   - Run integration tests"
	@echo "  test-coverage      - Run tests with coverage report"
	@echo "  test-quick         - Run quick tests (skip slow ones)"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint               - Run all linters (black, isort, flake8)"
	@echo "  format             - Format code with black and isort"
	@echo "  type-check         - Run mypy type checking"
	@echo "  pre-commit-run     - Run pre-commit on all files"
	@echo "  pre-commit-update  - Update pre-commit hooks"
	@echo "  check-all          - Run lint, type-check, and test"
	@echo ""
	@echo "  help               - Show this help message"
