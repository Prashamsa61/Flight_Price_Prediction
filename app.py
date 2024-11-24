import base64
import streamlit as st
import pandas as pd
import numpy as np

# Load the precomputed predictions CSV
predictions_df = pd.read_csv("predicted_flight_prices.csv")

# Set page configuration
st.set_page_config(page_title="Flight Price Prediction",
                   page_icon="✈️", layout="centered")

# Function to encode the image to base64


def get_image_uri(image_path: str):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


# Apply background image
def apply_background(image_uri):
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{image_uri}");
            background-size: cover;
            background-position: top;
            background-repeat: no-repeat;
        }}
        .stMarkdown p, .stTitle, .stHeader, .stTextInput {{
            color: black !important;
        }}
        .stButton button {{
            color: white !important; /* Change button text color to white */
        }}
        .stSuccess {{
            color: white !important; /* Change success message color to white */
            font-size: 20px; /* Optional: adjust size for better visibility */
        }}
        </style>
    """, unsafe_allow_html=True)


# Load background image
image_path = "pic4.webp"
image_uri = get_image_uri(image_path)
apply_background(image_uri)

# Function to prepare input features


def prepare_features(selected_airline, selected_source, selected_destination, selected_stops, duration, additional_info, selected_date):
    day_of_journey = selected_date.day
    month_of_journey = selected_date.month

    airlines = ['Air Asia', 'Air India', 'GoAir', 'IndiGo', 'Jet Airways',
                'Jet Airways Business', 'Multiple carriers',
                'Multiple carriers Premium economy', 'SpiceJet',
                'Trujet', 'Vistara', 'Vistara Premium economy']

    sources = ['Banglore', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    destinations = ['Banglore', 'Cochin', 'Delhi',
                    'Hyderabad', 'Kolkata', 'New Delhi']

    features = {f'Airline_{airline}': 1 if airline ==
                selected_airline else 0 for airline in airlines}
    features.update({f'Source_{source}': 1 if source ==
                    selected_source else 0 for source in sources})
    features.update({f'Destination_{destination}': 1 if destination ==
                    selected_destination else 0 for destination in destinations})

    features['Total_Stops'] = ['Non-stop', '1 stop',
                               '2 stops', '3 stops', '4 stops'].index(selected_stops)
    features['Duration_min'] = duration
    features['Len_Route'] = len(selected_source + selected_destination)

    # Additional Info
    for key, value in additional_info.items():
        features[f'Additional_Info_{key}'] = 1 if value else 0

    # Month and Day features
    for month in range(1, 13):
        features[f'month_{month}'] = 1 if month == month_of_journey else 0
    for day in range(1, 32):
        features[f'day_{day}'] = 1 if day == day_of_journey else 0

    return pd.DataFrame([features])


# Streamlit UI
with st.container():
    st.title("Flight Price Prediction")
    st.write("Select the flight details to get the predicted price.")

    # Flight Details Inputs
    selected_airline = st.selectbox("Select Airline", ['Air Asia', 'Air India', 'GoAir', 'IndiGo',
                                                       'Jet Airways', 'Jet Airways Business',
                                                       'Multiple carriers',
                                                       'Multiple carriers Premium economy',
                                                       'SpiceJet', 'Trujet', 'Vistara',
                                                       'Vistara Premium economy'])

    selected_source = st.selectbox(
        "Select Source City", ['Banglore', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai'])
    selected_destination = st.selectbox("Select Destination City", ['Banglore', 'Cochin', 'Delhi',
                                                                    'Hyderabad', 'Kolkata', 'New Delhi'])
    selected_stops = st.selectbox("Select Number of Stops", [
                                  'Non-stop', '1 stop', '2 stops', '3 stops', '4 stops'])
    duration = st.slider("Select Duration (in minutes)", 0, 1000, 300)

    # Additional Info Checkboxes
    additional_info = {
        'Long_layover': st.checkbox("Long layover"),
        'Short_layover': st.checkbox("Short layover"),
        'Business_class': st.checkbox("Business class"),
        'Change_airports': st.checkbox("Change airports"),
        'In-flight_meal_not_included': st.checkbox("In-flight meal not included"),
        'No_check_in_baggage_included': st.checkbox("No check-in baggage included"),
        'Red_eye_flight': st.checkbox("Red-eye flight")
    }

    selected_date = st.date_input("Select Date of Journey", min_value=pd.to_datetime("2024-01-01"),
                                  max_value=pd.to_datetime("2024-12-31"))

    # Prepare features and fetch prediction
    if st.button("Predict Price"):
        with st.spinner("Calculating predicted price..."):
            input_df = prepare_features(selected_airline, selected_source, selected_destination,
                                        selected_stops, duration, additional_info, selected_date)

            # Find matching row for prediction
            matching_row = predictions_df.loc[
                (predictions_df['Airline_Air Asia'] == input_df['Airline_Air Asia'][0]) &
                (predictions_df['Source_Banglore'] == input_df['Source_Banglore'][0]) &
                (predictions_df['Destination_Banglore'] == input_df['Destination_Banglore'][0]) &
                (predictions_df['Total_Stops'] == input_df['Total_Stops'][0]) &
                (predictions_df['Duration_min'] == input_df['Duration_min'][0])
            ]

            # Display the predicted price or an error message
            if not matching_row.empty:
                predicted_price = matching_row['Predicted_Price'].values[0]
                st.success(f"Predicted Flight Price: ₹{predicted_price:.2f}")
            else:
                st.error("No matching flight details found.")
