# Pre-commit Hooks Setup Guide

This guide explains how to set up and use pre-commit hooks with tests, linting, and code formatting for the MLOpengouins project.

## What are Pre-commit Hooks?

Pre-commit hooks automatically run checks before each commit to ensure code quality. This project uses:
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting (PEP 8 compliance)
- **mypy** - Static type checking
- **pytest** - Running tests

## Quick Start

### 1. Install Development Dependencies

```bash
# Install all development dependencies (includes test dependencies)
make install-dev
```

Or manually:
```bash
pip install -r requirements-dev.txt
```

### 2. Install Pre-commit Hooks

```bash
make pre-commit-install
```

Or manually:
```bash
pre-commit install
```

### 3. You're Done!

Now every time you run `git commit`, the hooks will automatically:
1. Format your code with Black
2. Sort your imports with isort
3. Check code quality with flake8
4. Run type checking with mypy
5. Run all tests with pytest

## Manual Commands

### Run Pre-commit on All Files

```bash
make pre-commit-run
```

Or:
```bash
pre-commit run --all-files
```

### Format Code

```bash
make format
```

This will:
- Format code with Black (line length: 100)
- Sort imports with isort

### Run Linters

```bash
make lint
```

This checks (without modifying):
- Black formatting
- isort import order
- flake8 code quality

### Run Type Checking

```bash
make type-check
```

### Run All Checks

```bash
make check-all
```

This runs: lint + type-check + test

## Configuration Files

### .pre-commit-config.yaml

Main configuration file for pre-commit hooks. Defines which hooks to run and their versions.

### pyproject.toml

Configuration for:
- Black formatting (line-length: 100)
- isort settings (profile: black)
- pytest settings
- Coverage settings

### setup.cfg

Additional configuration for:
- flake8 linting rules
- mypy type checking
- pytest

## Pre-commit Hook Behavior

### On Commit

When you run `git commit`, the following happens automatically:

1. **File checks**: trailing whitespace, end-of-file, large files, etc.
2. **Black**: Auto-formats Python files
3. **isort**: Auto-sorts imports
4. **flake8**: Checks code quality (fails if issues found)
5. **mypy**: Type checking (fails if issues found)
6. **pytest**: Runs all tests (fails if tests fail)

If any check fails:
- The commit is **blocked**
- Files modified by formatters (Black/isort) are **staged automatically**
- You need to review changes and commit again

### On Push

When you run `git push`, quick tests run:
- Only non-slow tests (`-m "not slow"`)
- Stops at first failure (`-x`)

## Common Workflows

### Making a Commit

```bash
# Make your changes
vim src/pengouins/data.py

# Try to commit
git add .
git commit -m "Add new feature"

# If pre-commit modifies files (Black/isort):
# - Review the changes
# - Add them: git add .
# - Commit again: git commit -m "Add new feature"

# If pre-commit fails (flake8/mypy/tests):
# - Fix the issues
# - Add fixes: git add .
# - Commit again: git commit -m "Add new feature"
```

### Skip Pre-commit Hooks (Not Recommended)

```bash
git commit --no-verify -m "Skip hooks"
```

**Warning**: Only use this in emergencies. You'll still need to pass CI/CD checks.

### Update Pre-commit Hooks

```bash
make pre-commit-update
```

This updates hooks to their latest versions.

## Troubleshooting

### Pre-commit Not Running

```bash
# Reinstall hooks
pre-commit uninstall
make pre-commit-install
```

### Tests Taking Too Long

The pre-commit runs all tests. If tests are slow:

1. Mark slow tests with `@pytest.mark.slow` decorator
2. Pre-commit will run them on commit but only run fast tests on push

Example:
```python
import pytest

@pytest.mark.slow
def test_large_dataset():
    # This test will run on commit but not on push
    pass
```

### Formatting Conflicts

If Black and your editor's formatter conflict:
1. Configure your editor to use Black
2. Set line length to 100 in editor settings
3. Or disable editor's auto-formatter

### Type Checking Issues

If mypy fails:
1. Add type hints to function signatures
2. Or add `# type: ignore` comment for specific lines
3. Or exclude files in `setup.cfg` under `[mypy]`

## Best Practices

1. **Run pre-commit before committing**: `make pre-commit-run`
2. **Format code regularly**: `make format`
3. **Run tests locally**: `make test`
4. **Check all before pushing**: `make check-all`
5. **Update hooks monthly**: `make pre-commit-update`

## Integration with CI/CD

Pre-commit hooks provide fast local feedback, but:
- CI/CD should run the same checks
- Pre-commit ensures most issues are caught before push
- Reduces CI/CD failures and speeds up development

## Disabling Specific Hooks

Edit `.pre-commit-config.yaml` and comment out hooks you don't want:

```yaml
# - repo: https://github.com/pre-commit/mirrors-mypy
#   rev: v1.8.0
#   hooks:
#     - id: mypy
```

Then update:
```bash
make pre-commit-install
```

## Getting Help

```bash
# Show make commands
make help

# Pre-commit help
pre-commit --help

# Run specific hook
pre-commit run black --all-files
pre-commit run pytest --all-files
```

## Summary

Pre-commit hooks help maintain code quality by:
- ✅ Auto-formatting code (Black, isort)
- ✅ Catching code issues early (flake8, mypy)
- ✅ Running tests before commit (pytest)
- ✅ Preventing bad commits from reaching the repository
- ✅ Making code reviews faster and easier

Happy coding!
