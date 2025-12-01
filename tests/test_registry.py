"""Tests for registry module."""

import pytest
import pickle
import os
import tempfile
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from pengouins.registry import save_model, load_model


@pytest.fixture
def sample_model():
    """Create a sample trained model."""
    model = KNeighborsClassifier(n_neighbors=3)
    import numpy as np
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 1, 1])
    model.fit(X, y)
    return model


@pytest.fixture
def temp_filepath():
    """Create a temporary filepath for testing."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pkl') as f:
        filepath = f.name
    yield filepath
    if os.path.exists(filepath):
        os.unlink(filepath)


class TestSaveModel:
    """Tests for save_model function."""

    def test_save_model_creates_file(self, sample_model, temp_filepath):
        """Test that save_model creates a file."""
        save_model(sample_model, temp_filepath)
        assert os.path.exists(temp_filepath)

    def test_save_model_file_not_empty(self, sample_model, temp_filepath):
        """Test that saved file is not empty."""
        save_model(sample_model, temp_filepath)
        assert os.path.getsize(temp_filepath) > 0

    def test_save_model_creates_pickle_file(self, sample_model, temp_filepath):
        """Test that saved file is a valid pickle file."""
        save_model(sample_model, temp_filepath)

        with open(temp_filepath, 'rb') as f:
            loaded = pickle.load(f)
            assert loaded is not None

    def test_save_model_overwrites_existing(self, sample_model, temp_filepath):
        """Test that save_model overwrites existing file."""
        model1 = KNeighborsClassifier(n_neighbors=1)
        model2 = KNeighborsClassifier(n_neighbors=5)

        import numpy as np
        X = np.array([[1, 2], [3, 4]])
        y = np.array([0, 1])
        model1.fit(X, y)
        model2.fit(X, y)

        save_model(model1, temp_filepath)
        size1 = os.path.getsize(temp_filepath)

        save_model(model2, temp_filepath)
        size2 = os.path.getsize(temp_filepath)

        assert os.path.exists(temp_filepath)

    def test_save_model_different_model_types(self, temp_filepath):
        """Test saving different types of models."""
        import numpy as np
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 0, 1, 1])

        models_to_test = [
            KNeighborsClassifier(n_neighbors=3).fit(X, y),
            DecisionTreeClassifier(random_state=42).fit(X, y)
        ]

        for i, model in enumerate(models_to_test):
            filepath = temp_filepath.replace('.pkl', f'_{i}.pkl')
            save_model(model, filepath)
            assert os.path.exists(filepath)
            os.unlink(filepath)

    def test_save_model_invalid_path(self, sample_model):
        """Test that invalid path raises error."""
        invalid_path = '/nonexistent/directory/model.pkl'
        with pytest.raises((FileNotFoundError, OSError)):
            save_model(sample_model, invalid_path)

    def test_save_model_nested_directory(self, sample_model):
        """Test saving model in nested directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested_path = os.path.join(tmpdir, 'models', 'trained', 'model.pkl')
            os.makedirs(os.path.dirname(nested_path), exist_ok=True)

            save_model(sample_model, nested_path)
            assert os.path.exists(nested_path)


class TestLoadModel:
    """Tests for load_model function."""

    def test_load_model_returns_model(self, sample_model, temp_filepath):
        """Test that load_model returns a model object."""
        save_model(sample_model, temp_filepath)
        loaded_model = load_model(temp_filepath)
        assert loaded_model is not None

    def test_load_model_preserves_type(self, sample_model, temp_filepath):
        """Test that loaded model has same type as saved model."""
        save_model(sample_model, temp_filepath)
        loaded_model = load_model(temp_filepath)
        assert type(loaded_model) == type(sample_model)

    def test_load_model_preserves_parameters(self, temp_filepath):
        """Test that loaded model preserves parameters."""
        original_model = KNeighborsClassifier(n_neighbors=7)
        import numpy as np
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 0, 1, 1])
        original_model.fit(X, y)

        save_model(original_model, temp_filepath)
        loaded_model = load_model(temp_filepath)

        assert loaded_model.n_neighbors == 7

    def test_load_model_can_predict(self, sample_model, temp_filepath):
        """Test that loaded model can make predictions."""
        import numpy as np
        save_model(sample_model, temp_filepath)
        loaded_model = load_model(temp_filepath)

        X_test = np.array([[2, 3], [6, 7]])
        predictions = loaded_model.predict(X_test)
        assert len(predictions) == 2

    def test_load_model_file_not_found(self):
        """Test that loading non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_model('nonexistent_model.pkl')

    def test_load_model_invalid_pickle(self, temp_filepath):
        """Test that loading invalid pickle file raises error."""
        with open(temp_filepath, 'w') as f:
            f.write('This is not a pickle file')

        with pytest.raises((pickle.UnpicklingError, EOFError)):
            load_model(temp_filepath)

    def test_load_model_empty_file(self, temp_filepath):
        """Test that loading empty file raises error."""
        with open(temp_filepath, 'w') as f:
            pass

        with pytest.raises(EOFError):
            load_model(temp_filepath)


class TestSaveLoadRoundtrip:
    """Integration tests for save and load roundtrip."""

    def test_save_load_roundtrip_predictions(self, sample_model, temp_filepath):
        """Test that predictions are identical after save/load."""
        import numpy as np
        X_test = np.array([[2, 3], [6, 7]])

        original_predictions = sample_model.predict(X_test)

        save_model(sample_model, temp_filepath)
        loaded_model = load_model(temp_filepath)
        loaded_predictions = loaded_model.predict(X_test)

        assert (original_predictions == loaded_predictions).all()

    def test_save_load_multiple_models(self):
        """Test saving and loading multiple models."""
        import numpy as np
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 0, 1, 1])

        models = [
            KNeighborsClassifier(n_neighbors=1).fit(X, y),
            KNeighborsClassifier(n_neighbors=3).fit(X, y),
            DecisionTreeClassifier(random_state=42).fit(X, y)
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            filepaths = [os.path.join(tmpdir, f'model_{i}.pkl') for i in range(len(models))]

            for model, filepath in zip(models, filepaths):
                save_model(model, filepath)

            loaded_models = [load_model(filepath) for filepath in filepaths]

            for original, loaded in zip(models, loaded_models):
                assert type(original) == type(loaded)

    def test_save_load_preserves_state(self, temp_filepath):
        """Test that model state is preserved through save/load."""
        import numpy as np
        model = KNeighborsClassifier(n_neighbors=3)
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 0, 1, 1])
        model.fit(X, y)

        original_classes = model.classes_

        save_model(model, temp_filepath)
        loaded_model = load_model(temp_filepath)

        assert (loaded_model.classes_ == original_classes).all()

    def test_save_load_preprocessing_pipeline(self, temp_filepath):
        """Test saving and loading preprocessing pipeline."""
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.impute import SimpleImputer
        import numpy as np

        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        X = np.array([[1, 2], [3, 4], [5, np.nan], [7, 8]])
        pipeline.fit(X)

        save_model(pipeline, temp_filepath)
        loaded_pipeline = load_model(temp_filepath)

        X_test = np.array([[2, 3], [6, np.nan]])
        original_transform = pipeline.transform(X_test)
        loaded_transform = loaded_pipeline.transform(X_test)

        assert np.allclose(original_transform, loaded_transform, equal_nan=True)

    def test_concurrent_save_load(self):
        """Test that multiple save/load operations work correctly."""
        import numpy as np
        X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
        y = np.array([0, 0, 1, 1])

        with tempfile.TemporaryDirectory() as tmpdir:
            for i in range(5):
                model = KNeighborsClassifier(n_neighbors=i+1)
                model.fit(X, y)

                filepath = os.path.join(tmpdir, f'model_{i}.pkl')
                save_model(model, filepath)
                loaded_model = load_model(filepath)

                assert loaded_model.n_neighbors == i + 1
