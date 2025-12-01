"""Tests for data module."""

import os
import tempfile

import numpy as np
import pandas as pd
import pytest

from pengouins.data import get_X_y, load_data, preprocess_data, split_data


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame(
        {
            "species": ["Adelie", "Gentoo", "Chinstrap", "Adelie", "Gentoo"],
            "bill_length_mm": [39.1, 46.1, 50.0, None, 45.0],
            "bill_depth_mm": [18.7, 13.0, 19.0, 17.8, 14.0],
            "flipper_length_mm": [181.0, 210.0, 195.0, 186.0, 200.0],
            "body_mass_g": [3750.0, 4500.0, 3800.0, 3625.0, 4200.0],
            "sex": ["Male", "Female", "Male", "Female", None],
            "island": ["Torgersen", "Biscoe", "Dream", "Torgersen", "Biscoe"],
        }
    )


@pytest.fixture
def sample_csv_file(sample_dataframe):
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
        sample_dataframe.to_csv(f.name, index=False)
        yield f.name
    os.unlink(f.name)


class TestLoadData:
    """Tests for load_data function."""

    def test_load_data_returns_dataframe(self, sample_csv_file):
        """Test that load_data returns a DataFrame."""
        result = load_data(sample_csv_file)
        assert isinstance(result, pd.DataFrame)

    def test_load_data_drops_island_column(self, sample_csv_file):
        """Test that island column is dropped."""
        result = load_data(sample_csv_file)
        assert "island" not in result.columns

    def test_load_data_removes_duplicates(self):
        """Test that duplicates are removed."""
        df_with_duplicates = pd.DataFrame(
            {
                "species": ["Adelie", "Adelie", "Gentoo"],
                "bill_length_mm": [39.1, 39.1, 46.1],
                "island": ["Torgersen", "Torgersen", "Biscoe"],
            }
        )

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            df_with_duplicates.to_csv(f.name, index=False)
            result = load_data(f.name)
            os.unlink(f.name)

        assert len(result) == 2

    def test_load_data_file_not_found(self):
        """Test that FileNotFoundError is raised for non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_data("non_existent_file.csv")


class TestGetXY:
    """Tests for get_X_y function."""

    def test_get_X_y_returns_tuple(self, sample_dataframe):
        """Test that get_X_y returns a tuple."""
        result = get_X_y(sample_dataframe, target_column="species")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_get_X_y_correct_shapes(self, sample_dataframe):
        """Test that X and y have correct shapes."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        assert len(X) == len(y)
        assert len(X.columns) == len(sample_dataframe.columns) - 1

    def test_get_X_y_target_not_in_X(self, sample_dataframe):
        """Test that target column is not in X."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        assert "species" not in X.columns

    def test_get_X_y_target_in_y(self, sample_dataframe):
        """Test that y contains the target values."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        assert y.name == "species"
        assert list(y) == ["Adelie", "Gentoo", "Chinstrap", "Adelie", "Gentoo"]

    def test_get_X_y_invalid_column(self, sample_dataframe):
        """Test that KeyError is raised for invalid column."""
        with pytest.raises(KeyError):
            get_X_y(sample_dataframe, target_column="invalid_column")


class TestSplitData:
    """Tests for split_data function."""

    def test_split_data_returns_four_elements(self, sample_dataframe):
        """Test that split_data returns four elements."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        result = split_data(X, y)
        assert len(result) == 4

    def test_split_data_correct_sizes(self, sample_dataframe):
        """Test that split sizes are correct."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.4)

        total_size = len(X)
        test_size = len(X_test)
        train_size = len(X_train)

        assert train_size + test_size == total_size
        assert test_size == pytest.approx(total_size * 0.4, abs=1)

    def test_split_data_random_state_reproducible(self, sample_dataframe):
        """Test that same random_state produces same split."""
        X, y = get_X_y(sample_dataframe, target_column="species")

        X_train1, X_test1, y_train1, y_test1 = split_data(X, y, random_state=42)
        X_train2, X_test2, y_train2, y_test2 = split_data(X, y, random_state=42)

        pd.testing.assert_frame_equal(X_train1, X_train2)
        pd.testing.assert_series_equal(y_train1, y_train2)

    def test_split_data_different_random_states(self, sample_dataframe):
        """Test that different random_states produce different splits."""
        X, y = get_X_y(sample_dataframe, target_column="species")

        X_train1, X_test1, y_train1, y_test1 = split_data(X, y, random_state=42)
        X_train2, X_test2, y_train2, y_test2 = split_data(X, y, random_state=123)

        assert not X_train1.equals(X_train2) or not y_train1.equals(y_train2)


class TestPreprocessData:
    """Tests for preprocess_data function."""

    def test_preprocess_data_fit_returns_pipeline(self, sample_dataframe):
        """Test that preprocess_data with fit=True returns a pipeline."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        preprocessing_model = preprocess_data(X, fit=True)
        assert preprocessing_model is not None
        assert hasattr(preprocessing_model, "transform")

    def test_preprocess_data_transform_returns_array(self, sample_dataframe):
        """Test that preprocess_data with fit=False returns an array."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        preprocessing_model = preprocess_data(X, fit=True)
        X_transformed = preprocess_data(X, fit=False, preprocessing_model=preprocessing_model)

        assert isinstance(X_transformed, np.ndarray)

    def test_preprocess_data_handles_missing_values(self, sample_dataframe):
        """Test that preprocessing handles missing values."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        preprocessing_model = preprocess_data(X, fit=True)
        X_transformed = preprocess_data(X, fit=False, preprocessing_model=preprocessing_model)

        assert not np.isnan(X_transformed).any()

    def test_preprocess_data_shape(self, sample_dataframe):
        """Test that transformed data has correct number of rows."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        preprocessing_model = preprocess_data(X, fit=True)
        X_transformed = preprocess_data(X, fit=False, preprocessing_model=preprocessing_model)

        assert X_transformed.shape[0] == len(X)

    def test_preprocess_data_consistent_transform(self, sample_dataframe):
        """Test that same data produces same transformation."""
        X, y = get_X_y(sample_dataframe, target_column="species")
        preprocessing_model = preprocess_data(X, fit=True)

        X_transformed1 = preprocess_data(X, fit=False, preprocessing_model=preprocessing_model)
        X_transformed2 = preprocess_data(X, fit=False, preprocessing_model=preprocessing_model)

        np.testing.assert_array_equal(X_transformed1, X_transformed2)

    def test_preprocess_data_without_model_raises_error(self, sample_dataframe):
        """Test that fit=False without preprocessing_model raises error."""
        X, y = get_X_y(sample_dataframe, target_column="species")

        with pytest.raises((AttributeError, TypeError)):
            preprocess_data(X, fit=False, preprocessing_model=None)


class TestIntegration:
    """Integration tests for data pipeline."""

    def test_full_data_pipeline(self, sample_csv_file):
        """Test the full data processing pipeline."""
        data = load_data(sample_csv_file)
        X, y = get_X_y(data, target_column="species")
        X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.4, random_state=42)

        preprocessing_model = preprocess_data(X_train, fit=True)
        X_train_transformed = preprocess_data(
            X_train, fit=False, preprocessing_model=preprocessing_model
        )
        X_test_transformed = preprocess_data(
            X_test, fit=False, preprocessing_model=preprocessing_model
        )

        assert X_train_transformed.shape[0] == len(X_train)
        assert X_test_transformed.shape[0] == len(X_test)
        assert X_train_transformed.shape[1] == X_test_transformed.shape[1]
        assert not np.isnan(X_train_transformed).any()
        assert not np.isnan(X_test_transformed).any()
