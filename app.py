
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

# Create columns for layout: Left inputs, Center image, Right inputs
# The prediction result will be displayed at the top, conceptually as an output of the column.
prediction_placeholder = st.empty() # Placeholder for the prediction result at the top

# Create a main layout using columns
col_left, col_center, col_right = st.columns([1, 2, 1])

# --- Left Side Inputs ---
with col_left:
    st.markdown("### Feed & Solvent Inlets")
    # Solvent Feed Temperature (over the 'Solvent' input line)
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True) # Vertical spacer
    solvent_feed_temp = st.slider(
        'Solvent Feed Temperature (degree celsius)',
        min_value=prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['min'],
        max_value=prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['max'],
        value= (prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['min'] + prediction_logic.restricted_ranges['Solvent Feed Temperature (degree celsius)']['max']) / 2,
        step=0.01,
        key='solvent_feed_temp_slider'
    )
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True) # Vertical spacer
    # Feed Analyser (on the 'Feed' input line)
    feed_analyser = st.slider(
        'Feed Analyser (mol%)',
        min_value=prediction_logic.restricted_ranges['Feed Analyser (mol%)']['min'],
        max_value=prediction_logic.restricted_ranges['Feed Analyser (mol%)']['max'],
        value= (prediction_logic.restricted_ranges['Feed Analyser (mol%)']['min'] + prediction_logic.restricted_ranges['Feed Analyser (mol%)']['max']) / 2,
        step=0.01,
        key='feed_analyser_slider'
    )

# --- Center Column for Image ---
with col_center:
    try:
        image = Image.open('refinery_column.png') # Assumes you have an image named refinery_column.png
        st.image(image, caption='Simplified Main Washer Column', use_column_width=True)
    except FileNotFoundError:
        st.warning("Refinery column image 'refinery_column.png' not found. Please upload it for a visual guide.")
        st.info("You can use a placeholder diagram or description for now.")

# --- Right Side Inputs ---
with col_right:
    st.markdown("### Overhead & Tray Conditions")
    # MW Overhead Analyser (on the 'Main Washer Overhead' output line)
    overhead_analyser = st.slider(
        'MW Overhead Analyser (mol%)',
        min_value=prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['min'],
        max_value=prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['max'],
        value= (prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['min'] + prediction_logic.restricted_ranges['MW Overhead Analyser (mol%)']['max']) / 2,
        step=0.01,
        key='overhead_analyser_slider'
    )
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True) # Vertical spacer
    # MW Tray Temperature (in the middle right)
    tray_temp = st.slider(
        'MW Tray Temperature (degree celsius)',
        min_value=prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['min'],
        max_value=prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['max'],
        value= (prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['min'] + prediction_logic.restricted_ranges['MW Tray Temperature (degree celsius)']['max']) / 2,
        step=0.01,
        key='tray_temp_slider'
    )

# --- Bottom Input (outside the columns for better horizontal spacing) ---
st.markdown("### Bottom Section Parameters")
bot_temp = st.slider(
    'MW Bottom Temperature (degree celsius)',
    min_value=prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['min'],
    max_value=prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['max'],
    value= (prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['min'] + prediction_logic.restricted_ranges['MW Bottom Temperature (degree celsius)']['max']) / 2,
    step=0.01,
    key='bot_temp_slider'
)

# --- Prediction Button ---
if st.button("Predict MW 1,3-BD IR Analyser"): # This button can be placed anywhere, let's keep it below for now
    input_data = {
        'MW Tray Temperature (degree celsius)': tray_temp,
        'MW Bottom Temperature (degree celsius)': bot_temp,
        'Solvent Feed Temperature (degree celsius)': solvent_feed_temp,
        'MW Overhead Analyser (mol%)': overhead_analyser,
        'Feed Analyser (mol%)': feed_analyser
    }

    try:
        predicted_value, prediction_in_range, target_min, target_max = prediction_logic.load_model_and_predict(input_data)

        with prediction_placeholder.container(): # Display prediction result in the placeholder at the top
            st.subheader("Prediction Result:")
            st.success(f"Predicted MW 1,3-BD IR Analyser (mol%): **{predicted_value:.4f}**")

            if not prediction_in_range:
                st.warning(f"Warning: Predicted value ({predicted_value:.4f}) is outside the specified target range [{target_min}, {target_max}].")

            st.markdown("""---
**Input Parameters Used:**""") # Corrected to use triple quotes
            for key, value in input_data.items():
                st.write(f"- {key}: {value:.2f}")

    except ValueError as e:
        with prediction_placeholder.container(): # Display error in the placeholder
            st.error(f"Input Error: {e}")
    except Exception as e:
        with prediction_placeholder.container(): # Display error in the placeholder
            st.error(f"An unexpected error occurred during prediction: {e}")

