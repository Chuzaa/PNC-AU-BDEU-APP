
import streamlit as st
import pandas as pd
from PIL import Image
import prediction_logic # Our refactored prediction logic

# --- Page Configuration ---
st.set_page_config(
    page_title="Refinery Column Predictor",
    page_icon=":oil_drum:",
    layout="wide"
)

st.title("🚧 Refinery Column Performance Predictor")
st.markdown("Predict MW 1,3-BD IR Analyser (mol%) based on process parameters.")

# --- Load Image for Visual Guide ---
# Make sure to upload a refinery column image (e.g., 'refinery_column.png') to your environment.
# For demonstration, we'll use a placeholder or assume an image is available.
# You can upload an image by clicking the folder icon on the left sidebar.

try:
    # Placeholder for a refinery column image. Replace 'refinery_column.png' with your actual image file.
    # For a more robust solution, host the image online or provide upload instructions.
    image = Image.open('refinery_column.png') # Assumes you have an image named refinery_column.png
    st.image(image, caption='Simplified Main Washer Column', use_column_width=True)
except FileNotFoundError:
    st.warning("Refinery column image 'refinery_column.png' not found. Please upload it for a visual guide.")
    st.info("You can use a placeholder diagram or description for now.")

st.markdown("### Adjust Process Parameters")

# --- Input Widgets (Placeholders for now, actual placement will be in next steps) ---
# These are just placeholders to define variables. Their visual placement will be done next.

# MW Bottom Temperature
bot_temp = st.sidebar.slider(
    'MW Bottom Temperature (degree celsius)',
    min_value=prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['min'],
    max_value=prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['max'],
    value= (prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['min'] + prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['max']) / 2,
    step=0.01
)

# MW Tray Temperature
tray_temp = st.sidebar.slider(
    'MW Tray Temperature (degree celsius)',
    min_value=prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['min'],
    max_value=prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['max'],
    value= (prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['min'] + prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['max']) / 2,
    step=0.01
)

# Solvent Feed Temperature
solvent_feed_temp = st.sidebar.slider(
    'Solvent Feed Temperature (degree celsius)',
    min_value=prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['min'],
    max_value=prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['max'],
    value= (prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['min'] + prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['max']) / 2,
    step=0.01
)

# MW Overhead Analyser
overhead_analyser = st.sidebar.slider(
    'MW Overhead Analyser (mol%)',
    min_value=prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['min'],
    max_value=prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['max'],
    value= (prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['min'] + prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['max']) / 2,
    step=0.01
)

# Feed Analyser
feed_analyser = st.sidebar.slider(
    'Feed Analyser (mol%)',
    min_value=prediction_logic.restricted_ranges['Feed Analyser (mol%)']['min'],
    max_value=prediction_logic.restricted_ranges['Feed Analyser (mol%)']['max'],
    value= (prediction_logic.restricted_ranges['Feed Analyser (mol%)']['min'] + prediction_logic.restricted_ranges['Feed Analyser (mol%)']['max']) / 2,
    step=0.01
)

# --- Prediction Button ---
if st.button("Predict MW 1,3-BD IR Analyser"):
    input_data = {
        'MW Tray Temperature (degree celsius)': tray_temp,
        'MW Bottom Temperature (degree celsius)': bot_temp,
        'Solvent Feed Temperature (degree celsius)': solvent_feed_temp,
        'MW Overhead Analyser (mol%)': overhead_analyser,
        'Feed Analyser (mol%)': feed_analyser
    }

    try:
        predicted_value, prediction_in_range, target_min, target_max = prediction_logic.load_model_and_predict(input_data)

        st.subheader("
Prediction Result:")
        st.success(f"Predicted MW 1,3-BD IR Analyser (mol%): **{predicted_value:.4f}**")

        if not prediction_in_range:
            st.warning(f"Warning: Predicted value ({predicted_value:.4f}) is outside the specified target range [{target_min}, {target_max}].")

        st.markdown("""---
**Input Parameters Used:**""")
        for key, value in input_data.items():
            st.write(f"- {key}: {value:.2f}")

    except ValueError as e:
        st.error(f"Input Error: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred during prediction: {e}")

