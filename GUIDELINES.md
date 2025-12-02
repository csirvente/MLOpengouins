# Implementation Guidelines for MLOps Penguin Project

This document provides step-by-step guidelines for implementing the functions defined in the `src/pengouins/` module. Use the `notebooks/experimentation.ipynb` notebook as your reference for the code logic.

---

## 📁 Module Overview

The project is organized into three main modules:

1. **`data.py`** - Data loading, splitting, and preprocessing
2. **`model.py`** - Model training and evaluation
3. **`registry.py`** - Model persistence (saving/loading)

---

## 1️⃣ `src/pengouins/data.py`

### 🎯 `load_data(path: str) -> pd.DataFrame`

**Purpose:** Load penguin data from a CSV file and return it as a DataFrame.

**Reference:** See cell #4 in the notebook (`#VSC-3e52eac0`)

**Implementation Steps:**
1. Use `pd.read_csv()` to read the CSV file from the given path
2. Drop the `island` column (as shown in the notebook, it's basically the target in disguise)
3. Return the DataFrame

**Example from notebook:**
```python
pingouins = sns.load_dataset("penguins")
pingouins.drop(columns=["island"], inplace=True)
```

**Key Points:**
- The function should load data from the path: `data/pingouins.csv`
- Make sure to drop the `island` column
- Handle potential errors (file not found, etc.)

---

### 🎯 `get_X_y(df: pd.DataFrame, target_column: str, target: bool = True) -> tuple[pd.DataFrame, pd.Series]`

**Purpose:** Split the DataFrame into features (X) and target variable (y).

**Reference:** See cell #15 in the notebook (`#VSC-b1189fc3`)

**Implementation Steps:**
1. If `target=True`: Extract the target column using `df.pop(target_column)` to get y, remaining is X
2. If `target=False`: Return the entire DataFrame as X, and None for y (for inference time)
3. Return the tuple (X, y)

**Example from notebook:**
```python
y = pingouins.pop("species")
X = pingouins
```

**Key Points:**
- Use `.pop()` to remove the target column from the DataFrame
- The target column will typically be `"species"`
- Return type: `tuple[pd.DataFrame, pd.Series]` or `tuple[pd.DataFrame, None]`

---

### 🎯 `split_data(X, y, test_size=0.2, random_state=42) -> tuple`

**Purpose:** Split data into training and testing sets.

**Reference:** See cell #15 in the notebook (`#VSC-b1189fc3`)

**Implementation Steps:**
1. Import `train_test_split` from `sklearn.model_selection` (already imported)
2. Use `train_test_split()` with the specified parameters
3. Use `stratify=y` to ensure balanced class distribution
4. Return X_train, X_test, y_train, y_test

**Example from notebook:**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

**Key Points:**
- Use `stratify=y` for balanced splits
- Default test_size should be 0.2 (20% test data)
- Default random_state should be 42 for reproducibility

---

### 🎯 `preprocess_data(X: pd.DataFrame, fit=True) -> pd.DataFrame`

**Purpose:** Preprocess the data using a Pipeline with ColumnTransformer for numerical and categorical features.

**Reference:** See cells #32-34 in the notebook (`#VSC-46c50c79`, `#VSC-e7b9c231`)

**Implementation Steps:**
1. Create a numerical pipeline with:
   - `SimpleImputer(strategy='median')` for missing values
   - `StandardScaler()` for scaling
2. Create a categorical pipeline with:
   - `SimpleImputer(strategy='most_frequent')` for missing values
   - `OneHotEncoder(sparse_output=False, drop="first")` for encoding
3. Combine both pipelines using `ColumnTransformer` with `make_column_selector`
4. If `fit=True`: fit and transform the data (for training)
5. If `fit=False`: only transform the data (for testing/inference)
6. Store the fitted preprocessor globally or as a class attribute for reuse

**Example from notebook:**
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

num_pipe = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
cat_pipe = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(sparse_output=False, drop="first"))
])
preprocessor = ColumnTransformer(transformers=[
    ('num', num_pipe, make_column_selector(dtype_include="number")),
    ('cat', cat_pipe, make_column_selector(dtype_include=object))
])
```

**Key Points:**
- Use `make_column_selector(dtype_include="number")` for numerical columns
- Use `make_column_selector(dtype_include=object)` for categorical columns
- The preprocessor needs to be saved for later use in inference
- **Important:** You'll need to manage the preprocessor state (consider using a global variable or returning it)

**💡 Suggested Approach:**
```python
# At module level
_preprocessor = None

def preprocess_data(X: pd.DataFrame, fit=True) -> pd.DataFrame:
    global _preprocessor
    if fit:
        # Create and fit preprocessor
        _preprocessor = ColumnTransformer(...)
        _preprocessor.fit(X)
    return pd.DataFrame(_preprocessor.transform(X))
```

---

## 2️⃣ `src/pengouins/model.py`

### 🎯 `train_model(X_train: pd.DataFrame, y_train: pd.Series)`

**Purpose:** Train a Logistic Regression model on the training data.

**Reference:** See cells #27 and #34 in the notebook (`#VSC-df25ac92`, `#VSC-63dbfeed`)

**Implementation Steps:**
1. Import `LogisticRegression` from `sklearn.linear_model`
2. Create a LogisticRegression instance
3. Fit the model on X_train and y_train
4. Return the trained model

**Example from notebook:**
```python
from sklearn.linear_model import LogisticRegression

logi = LogisticRegression()
logi.fit(X_train_final, y_train)
```

**Key Points:**
- Use default parameters for LogisticRegression
- The model should be trained on preprocessed data
- Return the fitted model object

---

### 🎯 `evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series) -> float`

**Purpose:** Evaluate the model and return the accuracy score.

**Reference:** See cells #27 and #34 in the notebook (`#VSC-df25ac92`, `#VSC-63dbfeed`)

**Implementation Steps:**
1. Import `accuracy_score` from `sklearn.metrics`
2. Use the model to predict on X_test
3. Calculate accuracy by comparing predictions with y_test
4. Return the accuracy score

**Example from notebook:**
```python
from sklearn.metrics import accuracy_score

y_pred = logi.predict(X_test_final)
score = accuracy_score(y_test, y_pred)
```

**Key Points:**
- Use `accuracy_score()` from sklearn.metrics
- The function should work with any sklearn classifier
- Return a float representing the accuracy (0.0 to 1.0)

---

## 3️⃣ `src/pengouins/registry.py`

### 🎯 `save_model(model, filepath)`

**Purpose:** Save a trained model to disk using pickle or joblib.

**Reference:** See cell #35 in the notebook (`#VSC-5b5dfd21`)

**Implementation Steps:**
1. Import `pickle` (or use `joblib` for better performance with sklearn models)
2. Create the directory if it doesn't exist using `os.makedirs()`
3. Open the file in write-binary mode (`"wb"`)
4. Use `pickle.dump()` to save the model
5. Close the file

**Example from notebook:**
```python
import pickle
import os

if not os.path.exists("../models"):
    os.makedirs("../models")

with open("../models/logistic_regression_model.pkl", "wb") as f:
    pickle.dump(logi_final, f)
```

**Key Points:**
- Use `pickle` or `joblib` (joblib is recommended for sklearn models)
- Ensure the directory exists before saving
- Use `.pkl` or `.joblib` extension
- Handle potential errors (permission issues, disk space, etc.)

---

### 🎯 `load_model(filepath)`

**Purpose:** Load a saved model from disk.

**Reference:** See cell #36 in the notebook (`#VSC-38338089`)

**Implementation Steps:**
1. Open the file in read-binary mode (`"rb"`)
2. Use `pickle.load()` to load the model
3. Return the loaded model

**Example from notebook:**
```python
with open("../models/logistic_regression_model.pkl", "rb") as f:
    logi_loaded = pickle.load(f)
```

**Key Points:**
- Use the same library (pickle/joblib) that was used to save the model
- Handle file not found errors
- Return the loaded model object

---

## 🎓 Testing Your Implementation

Once you've implemented all functions, you can test them by creating a simple script:

```python
from src.pengouins.data import load_data, get_X_y, split_data, preprocess_data
from src.pengouins.model import train_model, evaluate_model
from src.pengouins.registry import save_model, load_model

# 1. Load data
df = load_data("data/pingouins.csv")

# 2. Split into X and y
X, y = get_X_y(df, target_column="species")

# 3. Train/test split
X_train, X_test, y_train, y_test = split_data(X, y)

# 4. Preprocess
X_train_processed = preprocess_data(X_train, fit=True)
X_test_processed = preprocess_data(X_test, fit=False)

# 5. Train
model = train_model(X_train_processed, y_train)

# 6. Evaluate
accuracy = evaluate_model(model, X_test_processed, y_test)
print(f"Model Accuracy: {accuracy:.2%}")

# 7. Save
save_model(model, "models/logistic_regression_model.pkl")

# 8. Load
loaded_model = load_model("models/logistic_regression_model.pkl")
```

---

## 📚 Key Imports You'll Need

```python
# data.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# model.py
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# registry.py
import pickle
import os
```

---

## ⚠️ Common Pitfalls to Avoid

1. **Preprocessor State:** Make sure the same preprocessor fitted on training data is used for test data
2. **Island Column:** Don't forget to drop it when loading data
3. **Stratification:** Use `stratify=y` in train_test_split for balanced classes
4. **OneHotEncoder:** Use `drop="first"` to avoid multicollinearity
5. **File Paths:** Handle both relative and absolute paths correctly
6. **Missing Values:** The notebook shows there are missing values - your pipeline must handle them

---

## 🎯 Success Criteria

Your implementation is complete when:
- ✅ All functions have proper implementations (no `pass` statements)
- ✅ The code follows the logic from the notebook
- ✅ You can successfully run the testing script above
- ✅ The model achieves similar accuracy to the notebook (~97-99%)
- ✅ Models can be saved and loaded without errors

---

## 💡 Tips

1. **Start with `data.py`** - Get data loading and preprocessing working first
2. **Test incrementally** - Test each function as you write it
3. **Use the notebook** - Copy relevant code snippets and adapt them to the function structure
4. **Handle the preprocessor** - Consider how to store and reuse the fitted preprocessor
5. **Print shapes** - Use `print(X.shape)` to verify data dimensions at each step

Good luck! 🐧🚀
