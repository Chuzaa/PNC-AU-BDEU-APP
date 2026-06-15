
import pandas as pd
import joblib
import os
import gdown

# Define the restricted ranges for each input feature
restricted_ranges = {
    'MW 1,3-BD IR Analyser (mol%)': {'min': 16.0, 'max': 50.0},
    'MW Tray Temperature (degree celsius)': {'min': 55.0, 'max': 63.0},
    'MW Bottom Temperature (degree celsius)': {'min': 58.0, 'max': 63.0},
    'Solvent Feed Temperature (degree celsius)': {'min': 37.0, 'max': 45.0},
    'MW Overhead Analyser (mol%)': {'min': 0.0, 'max': 10.0},
    'Feed Analyser (mol%)': {'min': 40.0, 'max': 52.0}
}

# Placeholder for Google Drive URL - USER WILL NEED TO UPDATE THIS
# Get a shareable link for 'random_forest_model.joblib' from Google Drive
# Example: https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing
# Replace YOUR_FILE_ID with the actual ID from your shared link.
# Ensure the file is shared publicly or with 'Anyone with the link can view'.
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

def load_model_and_predict(input_data_dict):
    # Check if the model exists locally, if not, download it
    if not os.path.exists(MODEL_FILENAME):
        print(f"Model '{MODEL_FILENAME}' not found locally. Attempting to download from Google Drive...")
        try:
            gdown.download(MODEL_URL, MODEL_FILENAME, quiet=False)
            print("Model downloaded successfully.")
        except Exception as e:
            raise ConnectionError(f"Failed to download model from Google Drive. Please ensure MODEL_FILE_ID is correct and the file is publicly accessible. Error: {e}")

    # Load the trained model
    model = joblib.load(MODEL_FILENAME)

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
