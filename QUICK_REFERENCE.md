# Quick Reference Guide

## One-Time Setup
```bash
make install-dev          # Install all dependencies
make pre-commit-install   # Install git hooks
```

## Daily Development Commands

### Testing
```bash
make test                 # Run all tests
make test-quick           # Run fast tests only
make test-coverage        # Run tests with coverage report
```

### Code Quality
```bash
make format               # Auto-format code (Black + isort)
make lint                 # Check code quality (no changes)
make type-check           # Run type checking
make check-all            # Run ALL checks (lint + type + test)
```

### Pre-commit
```bash
make pre-commit-run       # Run pre-commit on all files
make pre-commit-update    # Update pre-commit hooks
```

### Git Workflow
```bash
# 1. Make changes
vim src/pengouins/model.py

# 2. Format
make format

# 3. Test
make test-quick

# 4. Check all
make check-all

# 5. Commit (hooks run automatically)
git add .
git commit -m "Add feature"

# 6. Push
git push
```

## Common pytest Commands
```bash
pytest -v                              # Verbose output
pytest -k "test_load"                  # Run tests matching pattern
pytest tests/test_data.py              # Run specific file
pytest -x                              # Stop at first failure
pytest --pdb                           # Debug on failure
pytest -m integration                  # Run tests with marker
pytest -m "not slow"                   # Skip slow tests
```

## Common Issues

### Pre-commit modifies files
```bash
# After pre-commit auto-formats:
git add .
git commit -m "Your message"
```

### Tests fail
```bash
pytest -vv                # More verbose
pytest --pdb              # Debug mode
```

### Import errors
```bash
pip install -e .          # Reinstall package
```

### Skip pre-commit (emergency)
```bash
git commit --no-verify -m "Emergency fix"
```

## File Locations
- Tests: `tests/`
- Source: `src/pengouins/`
- Config: `.pre-commit-config.yaml`, `pyproject.toml`, `setup.cfg`
- Docs: `tests/README.md`, `PRE_COMMIT_SETUP.md`, `DEVELOPMENT_SETUP.md`

## Help
```bash
make help                 # All make commands
pytest --help             # Pytest help
pre-commit --help         # Pre-commit help
```

## Coverage Report
After `make test-coverage`, open: `htmlcov/index.html`
