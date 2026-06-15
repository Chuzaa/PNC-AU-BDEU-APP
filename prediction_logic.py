
import pandas as pd
import joblib
import os
import gdown
from sklearn.ensemble import RandomForestRegressor

# Define the restricted ranges for each input feature
restricted_ranges = {
    'MW 1,3-BD IR Analyser (mol%)': {'min': 16.0, 'max': 50.0},
    'MW Tray Temperature (degree celsius)': {'min': 55.0, 'max': 63.0},
    'MW Bottom Temperature (degree celsius)': {'min': 58.0, 'max': 63.0},
    'Solvent Feed Temperature (degree celsius)': {'min': 37.0, 'max': 45.0},
    'MW Overhead Analyser (mol%)': {'min': 0.0, 'max': 10.0},
    'Feed Analyser (mol%)': {'min': 40.0, 'max': 52.0}
}

# Google Drive ID for the model file
MODEL_FILE_ID = '1iqoT2sAeDdACKI3h-KuJO_YdgNTLo_FJ' # <-- UPDATE THIS WITH YOUR MODEL'S FILE ID
MODEL_URL = f'https://drive.google.com/uc?id={MODEL_FILE_ID}'
MODEL_FILENAME = 'random_forest_model.joblib'

def validate_data_ranges(data, ranges):
    for col, limits in ranges.items():
        if col != 'MW 1,3-BD IR Analyser (mol%)': # Exclude target variable from input validation
            if isinstance(data, pd.DataFrame):
                value = data[col].iloc[0]
            else:
                value = data[col]

            if not (value >= limits['min'] and value <= limits['max']):
                raise ValueError(f"Input value for '{col}' ({value}) is outside the restricted range [{limits['min']}, {limits['max']}].")
    return True

_model_cache = None # Cache the model to avoid reloading on every request

def load_model():
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    # Check if the model exists locally, if not, download it
    if not os.path.exists(MODEL_FILENAME):
        print(f"Model '{MODEL_FILENAME}' not found locally. Attempting to download from Google Drive...")
        try:
            gdown.download(MODEL_URL, MODEL_FILENAME, quiet=False)
            print("Model downloaded successfully.")
        except Exception as e:
            raise ConnectionError(f"Failed to download model from Google Drive. Please ensure MODEL_FILE_ID is correct and the file is publicly accessible. Error: {e}")

    # Load the trained model
    _model_cache = joblib.load(MODEL_FILENAME)
    return _model_cache

def load_model_and_predict(input_data_dict):
    model = load_model() # Use the new load_model function

    # Convert input dictionary to DataFrame
    input_df = pd.DataFrame([input_data_dict])

    # Validate input data
    validate_data_ranges(input_df, restricted_ranges)

    # Make prediction
    predicted_value = model.predict(input_df)[0]

    # Validate predicted value against target range
    target_min = restricted_ranges['MW 1,3-BD IR Analyser (mol%)']['min']
    target_max = restricted_ranges['MW 1,3-BD IR Analyser (mol%)']['max']
    prediction_in_range = target_min <= predicted_value <= target_max

    return predicted_value, prediction_in_range, target_min, target_max
