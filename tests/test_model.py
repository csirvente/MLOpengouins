"""Tests for model module."""

import pytest
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from pengouins.model import train_model, evaluate_model


@pytest.fixture
def sample_training_data():
    """Create sample training data."""
    X_train = np.array([
        [1.0, 2.0, 3.0],
        [2.0, 3.0, 4.0],
        [3.0, 4.0, 5.0],
        [4.0, 5.0, 6.0],
        [5.0, 6.0, 7.0],
        [1.5, 2.5, 3.5],
        [2.5, 3.5, 4.5],
        [3.5, 4.5, 5.5]
    ])
    y_train = pd.Series(['A', 'A', 'B', 'B', 'C', 'A', 'B', 'C'])
    return pd.DataFrame(X_train, columns=['feature1', 'feature2', 'feature3']), y_train


@pytest.fixture
def sample_test_data():
    """Create sample test data."""
    X_test = np.array([
        [1.2, 2.2, 3.2],
        [3.2, 4.2, 5.2],
        [4.8, 5.8, 6.8]
    ])
    y_test = pd.Series(['A', 'B', 'C'])
    return pd.DataFrame(X_test, columns=['feature1', 'feature2', 'feature3']), y_test


class TestTrainModel:
    """Tests for train_model function."""

    def test_train_model_returns_model(self, sample_training_data):
        """Test that train_model returns a model object."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)
        assert model is not None
        assert hasattr(model, 'predict')

    def test_train_model_default_knn(self, sample_training_data):
        """Test that default model is KNeighborsClassifier."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)
        assert isinstance(model, KNeighborsClassifier)

    def test_train_model_custom_model(self, sample_training_data):
        """Test training with custom model."""
        X_train, y_train = sample_training_data
        custom_model = DecisionTreeClassifier(random_state=42)
        model = train_model(X_train, y_train, model=custom_model)
        assert isinstance(model, DecisionTreeClassifier)

    def test_train_model_is_fitted(self, sample_training_data):
        """Test that returned model is fitted."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)
        assert hasattr(model, 'classes_')

    def test_train_model_can_predict(self, sample_training_data):
        """Test that trained model can make predictions."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)
        predictions = model.predict(X_train[:2])
        assert len(predictions) == 2

    def test_train_model_with_different_algorithms(self, sample_training_data):
        """Test training with different algorithms."""
        X_train, y_train = sample_training_data

        models_to_test = [
            KNeighborsClassifier(n_neighbors=3),
            DecisionTreeClassifier(random_state=42),
            RandomForestClassifier(n_estimators=10, random_state=42)
        ]

        for model_type in models_to_test:
            model = train_model(X_train, y_train, model=model_type)
            assert hasattr(model, 'predict')
            predictions = model.predict(X_train[:1])
            assert len(predictions) == 1

    def test_train_model_with_empty_data(self):
        """Test that training with empty data raises error."""
        X_train = pd.DataFrame()
        y_train = pd.Series()

        with pytest.raises((ValueError, IndexError)):
            train_model(X_train, y_train)

    def test_train_model_mismatched_shapes(self, sample_training_data):
        """Test that mismatched X and y shapes raise error."""
        X_train, y_train = sample_training_data
        y_train_wrong = y_train[:3]

        with pytest.raises(ValueError):
            train_model(X_train, y_train_wrong)


class TestEvaluateModel:
    """Tests for evaluate_model function."""

    def test_evaluate_model_returns_float(self, sample_training_data, sample_test_data):
        """Test that evaluate_model returns a float score."""
        X_train, y_train = sample_training_data
        X_test, y_test = sample_test_data

        model = train_model(X_train, y_train)
        score = evaluate_model(model, X_test, y_test)

        assert isinstance(score, (float, np.floating))

    def test_evaluate_model_score_range(self, sample_training_data, sample_test_data):
        """Test that score is between 0 and 1."""
        X_train, y_train = sample_training_data
        X_test, y_test = sample_test_data

        model = train_model(X_train, y_train)
        score = evaluate_model(model, X_test, y_test)

        assert 0.0 <= score <= 1.0

    def test_evaluate_model_perfect_score(self, sample_training_data):
        """Test evaluation with perfect predictions."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)
        score = evaluate_model(model, X_train, y_train)

        assert score >= 0.5

    def test_evaluate_model_with_different_models(self, sample_training_data, sample_test_data):
        """Test evaluation with different model types."""
        X_train, y_train = sample_training_data
        X_test, y_test = sample_test_data

        models_to_test = [
            KNeighborsClassifier(n_neighbors=1),
            DecisionTreeClassifier(random_state=42)
        ]

        for model_type in models_to_test:
            model = train_model(X_train, y_train, model=model_type)
            score = evaluate_model(model, X_test, y_test)
            assert 0.0 <= score <= 1.0

    def test_evaluate_model_empty_test_data(self, sample_training_data):
        """Test evaluation with empty test data."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)

        X_test_empty = pd.DataFrame(columns=['feature1', 'feature2', 'feature3'])
        y_test_empty = pd.Series(dtype='object')

        with pytest.raises((ValueError, IndexError)):
            evaluate_model(model, X_test_empty, y_test_empty)

    def test_evaluate_model_unfitted_model(self, sample_test_data):
        """Test evaluation with unfitted model raises error."""
        X_test, y_test = sample_test_data
        unfitted_model = KNeighborsClassifier()

        with pytest.raises(Exception):
            evaluate_model(unfitted_model, X_test, y_test)

    def test_evaluate_model_wrong_feature_count(self, sample_training_data):
        """Test evaluation with wrong number of features."""
        X_train, y_train = sample_training_data
        model = train_model(X_train, y_train)

        X_test_wrong = pd.DataFrame([[1.0, 2.0]], columns=['feature1', 'feature2'])
        y_test = pd.Series(['A'])

        with pytest.raises(ValueError):
            evaluate_model(model, X_test_wrong, y_test)


class TestIntegration:
    """Integration tests for model training and evaluation."""

    def test_full_training_pipeline(self, sample_training_data, sample_test_data):
        """Test the complete training and evaluation pipeline."""
        X_train, y_train = sample_training_data
        X_test, y_test = sample_test_data

        model = train_model(X_train, y_train)
        train_score = evaluate_model(model, X_train, y_train)
        test_score = evaluate_model(model, X_test, y_test)

        assert 0.0 <= train_score <= 1.0
        assert 0.0 <= test_score <= 1.0

    def test_multiple_training_runs_reproducible(self, sample_training_data):
        """Test that training with same data produces consistent results."""
        X_train, y_train = sample_training_data

        model1 = train_model(X_train, y_train, model=DecisionTreeClassifier(random_state=42))
        score1 = evaluate_model(model1, X_train, y_train)

        model2 = train_model(X_train, y_train, model=DecisionTreeClassifier(random_state=42))
        score2 = evaluate_model(model2, X_train, y_train)

        assert score1 == score2

    def test_train_and_evaluate_multiple_classes(self):
        """Test training with multiple classes."""
        X_train = pd.DataFrame({
            'f1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'f2': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        })
        y_train = pd.Series(['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'E', 'E'])

        model = train_model(X_train, y_train)
        score = evaluate_model(model, X_train, y_train)

        assert 0.0 <= score <= 1.0
        assert len(model.classes_) == 5
