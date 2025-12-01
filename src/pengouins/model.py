
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier


def train_model(  X_train : pd.DataFrame
                , y_train: pd.Series
                , model = KNeighborsClassifier(1)) -> object:
    """Train a model on the training data."""

    classifierModel = model
    classifierModel.fit(X_train,y_train)
    return classifierModel

def evaluate_model( model
                    , X_test: pd.DataFrame
                    , y_test: pd.Series) -> float:
    """Evaluate the model on the test data and return accuracy."""
    y_pred = model.predict(X_test)
    score = accuracy_score(y_test,y_pred)
    return score