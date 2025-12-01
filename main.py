from pengouins.data import load_data,get_X_y,split_data, preprocess_data
from pengouins.model import train_model,evaluate_model
from pengouins.registry import save_model, load_model
import seaborn as sns


url_file = "./data/penguins.csv"
url_model = "./models/trained_model.pkl"
url_preprocessing_model = "./models/preprocessing_model.pkl"
target_column = "species"
model_name = "penguin_classifier"

def create_folders(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)

def create_sample_data():
    create_folders('./data')
    df_penguins = sns.load_dataset("penguins")
    df_penguins.to_csv('./data/penguins.csv', index=False)

if __name__ == "__main__":

    create_sample_data()

    # Load data
    data = load_data(url_file)


    # # Split data into features and target
    X, y = get_X_y(data, target_column=target_column)

    # split data into learning and validation sets (validation data will NEVER be used during training)
    X_learn, X_val, y_learn, y_val = split_data(X, y, test_size=0.4, random_state=42)

    # # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(X_learn, y_learn, test_size=0.2, random_state=42)


    # # Preprocess data
    preprocessing_model = preprocess_data(X_train, fit=True) #on entraine le preprocess sur le train

    X_train = preprocess_data(X_train, fit=False, preprocessing_model = preprocessing_model) #on applique le preprocess sur le train
    X_test = preprocess_data(X_test, fit=False, preprocessing_model = preprocessing_model) #on applique le preprocess sur le test

    # # Train model
    model = train_model(X_train, y_train)

    # # Evaluate model
    evaluation_results = evaluate_model(model, X_test, y_test)
    print("Evaluation Results on test dataset:", evaluation_results)

    # # Save model
    create_folders('./models')
    save_model(model,url_model)
    save_model(preprocessing_model, url_preprocessing_model)

    # # Load model (for demonstration)
    loaded_model = load_model(url_model)
    loaded_preprocessing_model = load_model(url_preprocessing_model)
    
    X_val_transformed = loaded_preprocessing_model.transform(X_val)
    evaluation_results = evaluate_model(loaded_model, X_val_transformed, y_val)
    print("Evaluation Results on validation dataset:", evaluation_results)

