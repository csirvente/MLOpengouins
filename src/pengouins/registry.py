import pickle


def save_model(model, filepath):
    """Saves the model to the specified filepath using pickle."""
    with open(filepath, "wb") as f:
        pickle.dump(model, f)


def load_model(filepath):
    """Loads the model from the specified filepath using pickle."""
    with open(filepath, "rb") as f:
        model = pickle.load(f)
    return model
