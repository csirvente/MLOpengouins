import os

import seaborn as sns
from loguru import logger
from pengouins.data import get_X_y, load_data, preprocess_data, split_data
from pengouins.model import evaluate_model, train_model
from pengouins.registry import load_model, save_model


logger.add("logs/main.log", rotation="1 MB")

url_file = "./data/penguins.csv"
url_model = "./models/trained_model.pkl"
url_preprocessing_model = "./models/preprocessing_model.pkl"
model_path = "./models/"
data_path = "./data/"
target_column = "species"
dataset_name = "penguins"
dataset_file = "penguins.csv"
model_name = "penguin_classifier"


def create_folders(path):

    if not os.path.exists(path):
        os.makedirs(path)


def create_sample_data():
    create_folders(data_path)
    df_penguins = sns.load_dataset(dataset_name)
    df_penguins.to_csv(f"{data_path}{dataset_file}", index=False)


if __name__ == "__main__":

    create_sample_data()
    logger.info("Sample data created.")
    # Load data
    data = load_data(f"{data_path}{dataset_file}")
    logger.info("Data loaded.")
    # # Split data into features and target
    X, y = get_X_y(data, target_column=target_column)
    logger.info("Data split into features and target.")
    # split data into learning and validation sets (validation data will NEVER be used during training)
    X_learn, X_val, y_learn, y_val = split_data(X, y, test_size=0.4, random_state=42)
    logger.info("Data split into learning and validation sets.")
    # # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X_learn, y_learn, test_size=0.2, random_state=42)
    logger.info("Data split into training and testing sets.")
    # # Preprocess data
    preprocessing_model = preprocess_data(
        X_train, fit=True
    )  # on entraine le preprocess sur le train
    logger.info("Preprocessing model trained on training data.")
    X_train = preprocess_data(
        X_train, fit=False, preprocessing_model=preprocessing_model
    )  # on applique le preprocess sur le train
    logger.info("Training data preprocessed.")
    X_test = preprocess_data(
        X_test, fit=False, preprocessing_model=preprocessing_model
    )  # on applique le preprocess sur le test
    logger.info("Testing data preprocessed.")

    # # Train model
    model = train_model(X_train, y_train)
    logger.info("Model trained on training data.")

    # # Evaluate model
    evaluation_results = evaluate_model(model, X_test, y_test)
    logger.info(f"Evaluation Results on test dataset: {evaluation_results}")
    print(f"Evaluation Results on test dataset: {evaluation_results}")

    # # Save model
    create_folders(model_path)
    save_model(model, url_model)
    save_model(preprocessing_model, url_preprocessing_model)
    logger.info("Trained model and preprocessing model saved.")

    # # Load model (for demonstration)
    loaded_model = load_model(url_model)
    loaded_preprocessing_model = load_model(url_preprocessing_model)
    logger.info("Trained model and preprocessing model loaded.")

    X_val_transformed = loaded_preprocessing_model.transform(X_val)
    logger.info("Validation data preprocessed.")
    evaluation_results = evaluate_model(loaded_model, X_val_transformed, y_val)
    logger.info(f"Evaluation Results on validation dataset: {evaluation_results}")
    print(f"Evaluation Results on validation dataset: {evaluation_results}")
    print("Process completed. Check logs/main.log for details.")