"""Integration tests for the complete ML pipeline."""

import pytest
import pandas as pd
import numpy as np
import tempfile
import os
from pengouins.data import load_data, get_X_y, split_data, preprocess_data
from pengouins.model import train_model, evaluate_model
from pengouins.registry import save_model, load_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


@pytest.fixture
def sample_penguins_csv():
    """Create a sample penguins CSV file for integration testing."""
    data = {
        'species': ['Adelie', 'Gentoo', 'Chinstrap', 'Adelie', 'Gentoo',
                    'Chinstrap', 'Adelie', 'Gentoo', 'Chinstrap', 'Adelie'] * 3,
        'bill_length_mm': [39.1, 46.1, 50.0, 38.5, 45.0, 49.0, 40.0, 47.0, 51.0, 37.0] * 3,
        'bill_depth_mm': [18.7, 13.0, 19.0, 17.8, 14.0, 18.5, 19.0, 13.5, 19.5, 17.0] * 3,
        'flipper_length_mm': [181.0, 210.0, 195.0, 186.0, 200.0, 197.0, 183.0, 212.0, 196.0, 185.0] * 3,
        'body_mass_g': [3750.0, 4500.0, 3800.0, 3625.0, 4200.0, 3850.0, 3700.0, 4550.0, 3900.0, 3600.0] * 3,
        'sex': ['Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female'] * 3,
        'island': ['Torgersen', 'Biscoe', 'Dream', 'Torgersen', 'Biscoe',
                   'Dream', 'Torgersen', 'Biscoe', 'Dream', 'Torgersen'] * 3
    }
    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        df.to_csv(f.name, index=False)
        yield f.name
    os.unlink(f.name)


@pytest.mark.integration
class TestFullPipeline:
    """Integration tests for the complete ML pipeline."""

    def test_complete_training_pipeline(self, sample_penguins_csv):
        """Test the complete pipeline from data loading to model evaluation."""
        data = load_data(sample_penguins_csv)

        assert isinstance(data, pd.DataFrame)
        assert len(data) > 0
        assert 'island' not in data.columns

        X, y = get_X_y(data, target_column='species')
        assert len(X) == len(y)
        assert 'species' not in X.columns

        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3, random_state=42)
        assert len(X_train) > len(X_test)

        preprocessing_model = preprocess_data(X_train, fit=True)
        X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
        X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

        assert isinstance(X_train_transformed, np.ndarray)
        assert not np.isnan(X_train_transformed).any()

        model = train_model(X_train_transformed, y_train)
        assert hasattr(model, 'predict')

        test_score = evaluate_model(model, X_test_transformed, y_test)
        assert 0.0 <= test_score <= 1.0

    def test_pipeline_with_model_persistence(self, sample_penguins_csv):
        """Test pipeline including model saving and loading."""
        data = load_data(sample_penguins_csv)
        X, y = get_X_y(data, target_column='species')
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3, random_state=42)

        preprocessing_model = preprocess_data(X_train, fit=True)
        X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
        X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

        model = train_model(X_train_transformed, y_train)
        original_score = evaluate_model(model, X_test_transformed, y_test)

        with tempfile.TemporaryDirectory() as tmpdir:
            model_path = os.path.join(tmpdir, 'model.pkl')
            preprocessing_path = os.path.join(tmpdir, 'preprocessing.pkl')

            save_model(model, model_path)
            save_model(preprocessing_model, preprocessing_path)

            assert os.path.exists(model_path)
            assert os.path.exists(preprocessing_path)

            loaded_model = load_model(model_path)
            loaded_preprocessing = load_model(preprocessing_path)

            X_test_loaded = loaded_preprocessing.transform(X_test)
            loaded_score = evaluate_model(loaded_model, X_test_loaded, y_test)

            assert loaded_score == original_score

    def test_pipeline_with_different_splits(self, sample_penguins_csv):
        """Test pipeline with different train/test splits."""
        data = load_data(sample_penguins_csv)
        X, y = get_X_y(data, target_column='species')

        test_sizes = [0.2, 0.3, 0.4]
        scores = []

        for test_size in test_sizes:
            X_train, X_test, y_train, y_test = split_data(X, y, test_size=test_size, random_state=42)

            preprocessing_model = preprocess_data(X_train, fit=True)
            X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
            X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

            model = train_model(X_train_transformed, y_train)
            score = evaluate_model(model, X_test_transformed, y_test)

            scores.append(score)
            assert 0.0 <= score <= 1.0

        assert len(scores) == len(test_sizes)

    def test_pipeline_with_different_models(self, sample_penguins_csv):
        """Test pipeline with different model types."""
        data = load_data(sample_penguins_csv)
        X, y = get_X_y(data, target_column='species')
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3, random_state=42)

        preprocessing_model = preprocess_data(X_train, fit=True)
        X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
        X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

        models_to_test = [
            KNeighborsClassifier(n_neighbors=1),
            KNeighborsClassifier(n_neighbors=5),
            DecisionTreeClassifier(random_state=42)
        ]

        for model_type in models_to_test:
            model = train_model(X_train_transformed, y_train, model=model_type)
            score = evaluate_model(model, X_test_transformed, y_test)
            assert 0.0 <= score <= 1.0

    def test_pipeline_reproducibility(self, sample_penguins_csv):
        """Test that pipeline produces reproducible results."""
        scores = []

        for _ in range(2):
            data = load_data(sample_penguins_csv)
            X, y = get_X_y(data, target_column='species')
            X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3, random_state=42)

            preprocessing_model = preprocess_data(X_train, fit=True)
            X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
            X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

            model = train_model(X_train_transformed, y_train, model=KNeighborsClassifier(n_neighbors=3))
            score = evaluate_model(model, X_test_transformed, y_test)
            scores.append(score)

        assert scores[0] == scores[1]

    def test_pipeline_handles_validation_set(self, sample_penguins_csv):
        """Test pipeline with separate validation set."""
        data = load_data(sample_penguins_csv)
        X, y = get_X_y(data, target_column='species')

        X_learn, X_val, y_learn, y_val = split_data(X, y, test_size=0.4, random_state=42)
        X_train, X_test, y_train, y_test = split_data(X_learn, y_learn, test_size=0.2, random_state=42)

        preprocessing_model = preprocess_data(X_train, fit=True)
        X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
        X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)
        X_val_transformed = preprocess_data(X_val, fit=False, preprocessing_model=preprocessing_model)

        model = train_model(X_train_transformed, y_train)

        test_score = evaluate_model(model, X_test_transformed, y_test)
        val_score = evaluate_model(model, X_val_transformed, y_val)

        assert 0.0 <= test_score <= 1.0
        assert 0.0 <= val_score <= 1.0


@pytest.mark.integration
class TestEdgeCases:
    """Integration tests for edge cases."""

    def test_pipeline_with_minimal_data(self):
        """Test pipeline with minimal amount of data."""
        data = pd.DataFrame({
            'species': ['Adelie', 'Gentoo', 'Chinstrap'] * 4,
            'bill_length_mm': [39.1, 46.1, 50.0] * 4,
            'bill_depth_mm': [18.7, 13.0, 19.0] * 4,
            'flipper_length_mm': [181.0, 210.0, 195.0] * 4,
            'body_mass_g': [3750.0, 4500.0, 3800.0] * 4,
            'sex': ['Male', 'Female', 'Male'] * 4
        })

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            data.to_csv(f.name, index=False)
            csv_path = f.name

        try:
            loaded_data = load_data(csv_path)
            X, y = get_X_y(loaded_data, target_column='species')
            X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3, random_state=42)

            preprocessing_model = preprocess_data(X_train, fit=True)
            X_train_transformed = preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model)
            X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

            model = train_model(X_train_transformed, y_train)
            score = evaluate_model(model, X_test_transformed, y_test)

            assert 0.0 <= score <= 1.0
        finally:
            os.unlink(csv_path)

    def test_pipeline_predictions_consistency(self, sample_penguins_csv):
        """Test that predictions are consistent across multiple calls."""
        data = load_data(sample_penguins_csv)
        X, y = get_X_y(data, target_column='species')
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.3, random_state=42)

        preprocessing_model = preprocess_data(X_train, fit=True)
        X_test_transformed = preprocess_data(X_test, fit=False, preprocessing_model=preprocessing_model)

        model = train_model(
            preprocess_data(X_train, fit=False, preprocessing_model=preprocessing_model),
            y_train,
            model=DecisionTreeClassifier(random_state=42)
        )

        predictions1 = model.predict(X_test_transformed)
        predictions2 = model.predict(X_test_transformed)

        assert (predictions1 == predictions2).all()
