
import pandas as pd
import joblib

# Define the restricted ranges for each input feature
restricted_ranges = {
    'MW 1,3-BD IR Analyser (mol%)': {'min': 16.0, 'max': 50.0},
    'MW Tray Temperature (degree celsius)': {'min': 55.0, 'max': 63.0},
    'MW Bottom Temperature (degree celsius)': {'min': 58.0, 'max': 63.0},
    'Solvent Feed Temperature (degree celsius)': {'min': 37.0, 'max': 45.0},
    'MW Overhead Analyser (mol%)': {'min': 0.0, 'max': 10.0},
    'Feed Analyser (mol%)': {'min': 40.0, 'max': 52.0}
}

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
    # Load the trained model
    model = joblib.load('random_forest_model.joblib')

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
