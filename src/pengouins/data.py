"""
Load and preprocess data.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import numpy as np

imputerModel = None
scalerModel = None
onehotencoderModel = None

def load_data(path: str) -> pd.DataFrame:
    """Load data from seaborn data,
    put it in cache and return a DataFrame."""
    df = pd.read_csv(path)
    df.drop(columns=["island"], inplace=True)
    df.drop_duplicates(inplace=True)
    return df
    pass


def get_X_y(
    df: pd.DataFrame, target_column: str, target:bool = True
) -> tuple[pd.DataFrame, pd.Series]:
    """Split DataFrame into features and target."""
    # y = df.pop(target_column)
    # X = df
    # Attention le pop fait u deux en un (revnoi la colonne et la supprime du df)
    
    y = df[target_column]
    X = df.drop(columns=[target_column])
    return X, y

def split_data(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Split data into training and testing sets."""
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def preprocess_data(X: pd.DataFrame
                    ,fit = True) -> pd.DataFrame:
    global imputerModel
    global scalerModel
    global onehotencoderModel
    
    
    """Preprocess data: handle missing values, encode categorical variables, scale numerical features."""
    X_categorical = X.select_dtypes(include=["object"])
    X_numerical = X.select_dtypes(include=["float64", "int64"])
    
    if fit == True:
   
        imputerModel = SimpleImputer(strategy="most_frequent")
        scalerModel = StandardScaler()
        onehotencoderModel = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
        
        imputerModel.fit(X_numerical)
        scalerModel.fit(imputerModel.transform(X_numerical) )
        onehotencoderModel.fit(X_categorical) 
        return None
    else: 
        X_numerical_imputed = imputerModel.transform(X_numerical)
        X_numerical_scaled = scalerModel.transform(X_numerical_imputed)
        X_categorical_encoded = onehotencoderModel.transform(X_categorical)

        #concaténation des deux X_numerical_scaled et X_categorical_encoded
        X_final =  np.concatenate((X_numerical_scaled, X_categorical_encoded), axis=1)
        return X_final
            


    
    