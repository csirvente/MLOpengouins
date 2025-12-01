# Tests for MLOpengouins

This directory contains comprehensive tests for the MLOpengouins penguin classification project.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Shared pytest fixtures and configuration
├── test_data.py             # Tests for data loading and preprocessing
├── test_model.py            # Tests for model training and evaluation
├── test_registry.py         # Tests for model persistence
├── test_integration.py      # End-to-end integration tests
└── README.md               # This file
```

## Running Tests

### Install test dependencies
```bash
pip install -r requirements-test.txt
```

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_data.py
pytest tests/test_model.py
pytest tests/test_registry.py
pytest tests/test_integration.py
```

### Run tests with coverage
```bash
pytest --cov=src/pengouins --cov-report=html
```

### Run tests by marker
```bash
# Run only integration tests
pytest -m integration

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test class or function
```bash
pytest tests/test_data.py::TestLoadData
pytest tests/test_model.py::TestTrainModel::test_train_model_returns_model
```

## Test Coverage

The test suite covers:

### test_data.py
- **TestLoadData**: Tests for loading CSV files and data cleaning
  - File loading and DataFrame creation
  - Dropping island column
  - Removing duplicates
  - Error handling for missing files

- **TestGetXY**: Tests for feature/target splitting
  - Correct splitting of features and target
  - Target column removal from features
  - Error handling for invalid columns

- **TestSplitData**: Tests for train/test splitting
  - Correct split sizes
  - Reproducibility with random_state
  - Different random states produce different splits

- **TestPreprocessData**: Tests for preprocessing pipeline
  - Pipeline creation and fitting
  - Data transformation
  - Missing value handling
  - Consistency of transformations

- **TestIntegration**: Integration tests for complete data pipeline

### test_model.py
- **TestTrainModel**: Tests for model training
  - Model fitting and return types
  - Different model algorithms (KNN, Decision Tree, Random Forest)
  - Error handling for invalid data
  - Shape mismatches

- **TestEvaluateModel**: Tests for model evaluation
  - Score calculation and ranges
  - Different model types
  - Error handling for unfitted models
  - Feature count validation

- **TestIntegration**: Integration tests for training pipeline

### test_registry.py
- **TestSaveModel**: Tests for model saving
  - File creation and persistence
  - Overwriting existing files
  - Different model types
  - Nested directory structures

- **TestLoadModel**: Tests for model loading
  - Model reconstruction
  - Type and parameter preservation
  - Prediction capability
  - Error handling for invalid files

- **TestSaveLoadRoundtrip**: Integration tests for save/load cycle
  - Prediction consistency
  - Multiple models
  - State preservation
  - Preprocessing pipeline persistence

### test_integration.py
- **TestFullPipeline**: End-to-end pipeline tests
  - Complete workflow from loading to evaluation
  - Model persistence
  - Different data splits
  - Different model types
  - Reproducibility
  - Validation set handling

- **TestEdgeCases**: Edge case testing
  - Minimal data
  - Prediction consistency

## Test Fixtures

Common fixtures available in [conftest.py](conftest.py):
- Path configuration for imports
- Custom pytest markers (slow, integration, unit)

Test-specific fixtures:
- `sample_dataframe`: Sample penguin data
- `sample_csv_file`: Temporary CSV file
- `sample_training_data`: Sample training data for models
- `sample_test_data`: Sample test data for evaluation
- `sample_model`: Pre-trained model
- `temp_filepath`: Temporary file path for persistence tests
- `sample_penguins_csv`: Full penguin dataset for integration tests

## Contributing

When adding new tests:
1. Follow the existing test structure and naming conventions
2. Use appropriate fixtures to avoid code duplication
3. Add markers for integration tests (`@pytest.mark.integration`)
4. Ensure tests are isolated and don't depend on each other
5. Test both happy paths and error cases
6. Update this README if adding new test modules

## Notes

- All tests use temporary files/directories and clean up after themselves
- Random states are fixed for reproducibility
- Tests are designed to run in any order
- Each test class groups related functionality
