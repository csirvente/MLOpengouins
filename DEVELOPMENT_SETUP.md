# Development Setup & Workflow

Complete guide for setting up the MLOpengouins development environment with testing, linting, and pre-commit hooks.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Testing](#testing)
4. [Code Quality](#code-quality)
5. [Pre-commit Hooks](#pre-commit-hooks)
6. [Makefile Commands](#makefile-commands)
7. [Development Workflow](#development-workflow)

## Quick Start

```bash
# 1. Install development dependencies
make install-dev

# 2. Install pre-commit hooks
make pre-commit-install

# 3. Run tests
make test

# 4. Format code
make format

# 5. Run all checks
make check-all
```

## Installation

### Test Dependencies Only
```bash
make install-test
# or
pip install -r requirements-test.txt
```

### Full Development Setup
```bash
make install-dev
# or
pip install -r requirements-dev.txt
```

This installs:
- pytest, pytest-cov, pytest-mock (testing)
- black (code formatting)
- isort (import sorting)
- flake8 (linting)
- mypy (type checking)
- pylint (additional linting)
- pre-commit (git hooks)

## Testing

### Run All Tests
```bash
make test
```

### Run Specific Test Modules
```bash
make test-data          # Data processing tests
make test-model         # Model training tests
make test-registry      # Model persistence tests
make test-integration   # Integration tests
```

### Run with Coverage
```bash
make test-coverage
```
Coverage report will be generated in `htmlcov/index.html`

### Run Quick Tests
```bash
make test-quick
```
Skips tests marked with `@pytest.mark.slow`

### Direct Pytest Commands
```bash
pytest -v                              # All tests, verbose
pytest tests/test_data.py              # Specific file
pytest tests/test_data.py::TestLoadData  # Specific class
pytest -k "test_load"                  # Tests matching pattern
pytest -m integration                  # Tests with marker
pytest -x                              # Stop at first failure
pytest --pdb                           # Debug on failure
```

## Code Quality

### Format Code
```bash
make format
```
Runs:
- Black (code formatter, line-length: 100)
- isort (import sorter)

### Check Formatting (No Changes)
```bash
make lint
```
Checks:
- Black formatting
- isort import order
- flake8 code quality

### Type Checking
```bash
make type-check
```
Runs mypy on source code (tests excluded)

### Run All Quality Checks
```bash
make check-all
```
Equivalent to: `lint + type-check + test`

### Manual Tool Usage

**Black:**
```bash
black src/ tests/ main.py              # Format
black --check src/ tests/              # Check only
black --diff src/                      # Show diff
```

**isort:**
```bash
isort src/ tests/ main.py              # Sort imports
isort --check-only src/ tests/         # Check only
isort --diff src/                      # Show diff
```

**flake8:**
```bash
flake8 src/ tests/                     # Lint all
flake8 src/pengouins/data.py           # Lint file
```

**mypy:**
```bash
mypy src/                              # Type check
mypy --strict src/                     # Strict mode
```

## Pre-commit Hooks

### Installation
```bash
make pre-commit-install
```

### What Gets Checked

**On Every Commit:**
1. File checks (trailing whitespace, large files, etc.)
2. Black auto-formatting
3. isort auto-sorting
4. flake8 linting
5. mypy type checking
6. pytest (all tests)

**On Push:**
- Quick tests only (non-slow tests)

### Manual Pre-commit Run
```bash
make pre-commit-run
# or
pre-commit run --all-files
```

### Update Hooks
```bash
make pre-commit-update
```

### Skip Hooks (Emergency Only)
```bash
git commit --no-verify -m "Emergency fix"
```

See [PRE_COMMIT_SETUP.md](PRE_COMMIT_SETUP.md) for detailed pre-commit documentation.

## Makefile Commands

Run `make help` to see all available commands.

### Setup Commands
| Command | Description |
|---------|-------------|
| `make setup` | Set up development environment with pyenv |
| `make install-test` | Install test dependencies only |
| `make install-dev` | Install all development dependencies |
| `make pre-commit-install` | Install pre-commit git hooks |

### Testing Commands
| Command | Description |
|---------|-------------|
| `make test` | Run all tests |
| `make test-data` | Run data module tests |
| `make test-model` | Run model module tests |
| `make test-registry` | Run registry module tests |
| `make test-integration` | Run integration tests |
| `make test-coverage` | Run tests with coverage report |
| `make test-quick` | Run quick tests (skip slow) |

### Code Quality Commands
| Command | Description |
|---------|-------------|
| `make lint` | Check code formatting and quality |
| `make format` | Auto-format code with black and isort |
| `make type-check` | Run mypy type checking |
| `make pre-commit-run` | Run pre-commit on all files |
| `make pre-commit-update` | Update pre-commit hooks |
| `make check-all` | Run all checks (lint, type-check, test) |

## Development Workflow

### Starting New Work
```bash
# 1. Create a new branch
git checkout -b feature/my-feature

# 2. Make sure environment is up to date
make install-dev
make pre-commit-install
```

### While Developing
```bash
# 1. Write code
vim src/pengouins/model.py

# 2. Format code
make format

# 3. Run relevant tests
make test-model

# 4. Run all checks before committing
make check-all
```

### Committing Changes
```bash
# 1. Stage changes
git add .

# 2. Commit (pre-commit hooks run automatically)
git commit -m "Add new feature"

# If pre-commit modifies files:
git add .
git commit -m "Add new feature"

# If pre-commit fails:
# Fix issues, then:
git add .
git commit -m "Add new feature"
```

### Before Pushing
```bash
# Run full check suite
make check-all

# Push
git push origin feature/my-feature
```

### Continuous Development Loop
```bash
# Quick feedback loop during development:
1. Edit code
2. make format          # Auto-format
3. make test-quick      # Fast tests
4. make lint            # Check quality
5. Repeat

# Before committing:
make check-all          # Full check
git add . && git commit -m "message"
```

## Configuration Files

| File | Purpose |
|------|---------|
| [.pre-commit-config.yaml](.pre-commit-config.yaml) | Pre-commit hooks configuration |
| [pyproject.toml](pyproject.toml) | Black, isort, pytest, coverage config |
| [setup.cfg](setup.cfg) | flake8, mypy additional configuration |
| [pytest.ini](pytest.ini) | Pytest configuration (deprecated in favor of pyproject.toml) |
| [requirements-test.txt](requirements-test.txt) | Testing dependencies |
| [requirements-dev.txt](requirements-dev.txt) | All development dependencies |
| [Makefile](Makefile) | Development task automation |

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_data.py             # Data loading/preprocessing tests
├── test_model.py            # Model training/evaluation tests
├── test_registry.py         # Model persistence tests
├── test_integration.py      # End-to-end integration tests
└── README.md               # Test documentation
```

See [tests/README.md](tests/README.md) for detailed test documentation.

## Code Style Guidelines

### Line Length
- Maximum: 100 characters (configured in all tools)

### Import Order (isort)
```python
# Standard library
import os
import sys

# Third party
import pandas as pd
import numpy as np

# Local
from pengouins.data import load_data
from pengouins.model import train_model
```

### Type Hints (Optional but Recommended)
```python
def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> object:
    """Train a model on the training data."""
    pass
```

### Docstrings
```python
def load_data(path: str) -> pd.DataFrame:
    """Load data from CSV file.

    Args:
        path: Path to CSV file

    Returns:
        DataFrame with loaded data
    """
    pass
```

## Troubleshooting

### Tests Failing
```bash
# Run with more verbose output
pytest -vv

# Run specific failing test
pytest tests/test_data.py::TestLoadData::test_load_data_returns_dataframe -vv

# Debug on failure
pytest --pdb
```

### Linting Errors
```bash
# See what needs to be fixed
make lint

# Auto-fix formatting issues
make format

# Check specific file
flake8 src/pengouins/data.py
```

### Pre-commit Issues
```bash
# Reinstall hooks
pre-commit uninstall
make pre-commit-install

# Run manually to see issues
make pre-commit-run

# Run specific hook
pre-commit run black --all-files
```

### Import Errors in Tests
Make sure you're in the project root and have installed the package:
```bash
pip install -e .
```

## Best Practices

1. ✅ **Always format before committing**: `make format`
2. ✅ **Run tests frequently**: `make test-quick`
3. ✅ **Use pre-commit hooks**: They catch issues early
4. ✅ **Write tests for new code**: Maintain >80% coverage
5. ✅ **Type hints for public APIs**: Helps with documentation
6. ✅ **Small, focused commits**: Easier to review and revert
7. ✅ **Run full checks before PR**: `make check-all`

## Resources

- [Pre-commit Setup Guide](PRE_COMMIT_SETUP.md) - Detailed pre-commit documentation
- [Test Documentation](tests/README.md) - Test suite documentation
- [Black Documentation](https://black.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [pre-commit Documentation](https://pre-commit.com/)

## Getting Help

```bash
# Show all make commands
make help

# Pytest help
pytest --help

# Pre-commit help
pre-commit --help

# Tool-specific help
black --help
isort --help
flake8 --help
mypy --help
```

## Summary

This project uses modern Python development tools to ensure code quality:

- 🧪 **pytest** for comprehensive testing (933+ lines of tests)
- 🎨 **Black** for consistent code formatting
- 📦 **isort** for organized imports
- 🔍 **flake8** for code quality checks
- 🔒 **mypy** for type safety
- 🪝 **pre-commit** for automated quality gates

Happy coding!
