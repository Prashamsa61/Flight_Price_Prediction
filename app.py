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


# Path to your local image
image_path = "pic2.jpeg"

# Convert the image to base64
image_uri = get_image_uri(image_path)

# Apply the background image
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_uri}");
        background-size: cover;
        background-position: top;
        background-repeat: no-repeat;
    }}
    </style>
""", unsafe_allow_html=True)

with st.container():

    # Display title and instructions
    st.title("Flight Price Prediction")
    st.write("Select the flight details to get the predicted price.")

    # Inputs for the user
    st.header("Select Flight Information")

    # Airline Selection
    airlines = ['Air Asia', 'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
                'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet', 'Trujet', 'Vistara', 'Vistara Premium economy']
    selected_airline = st.selectbox("Select Airline", airlines)

    # Source City Selection
    sources = ['Banglore', 'Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    selected_source = st.selectbox("Select Source City", sources)

    # Destination City Selection
    destinations = ['Banglore', 'Cochin', 'Delhi',
                    'Hyderabad', 'Kolkata', 'New Delhi']
    selected_destination = st.selectbox(
        "Select Destination City", destinations)

    # Number of Stops Selection
    stops = ['Non-stop', '1 stop', '2 stops', '3 stops', '4 stops']
    selected_stops = st.selectbox("Select Number of Stops", stops)

    # Duration Slider (minutes)
    duration = st.slider("Select Duration (in minutes)", 0, 1000, 300)

    # Additional Info (Checkboxes for different features)
    long_layover = st.checkbox("Long layover")
    short_layover = st.checkbox("Short layover")
    business_class = st.checkbox("Business class")
    change_airports = st.checkbox("Change airports")
    meal_included = st.checkbox("In-flight meal not included")
    no_check_in_baggage = st.checkbox("No check-in baggage included")
    red_eye_flight = st.checkbox("Red-eye flight")

    # Date Selection (User can pick a date from the calendar)
    selected_date = st.date_input("Select Date of Journey", min_value=pd.to_datetime(
        "2024-01-01"), max_value=pd.to_datetime("2024-12-31"))

    # Convert date to day of the month and month
    day_of_journey = selected_date.day
    month_of_journey = selected_date.month

    # Prepare the input features (encode selections)
    features = {
        'Airline_Air Asia': 1 if selected_airline == 'Air Asia' else 0,
        'Airline_Air India': 1 if selected_airline == 'Air India' else 0,
        'Airline_GoAir': 1 if selected_airline == 'GoAir' else 0,
        'Airline_IndiGo': 1 if selected_airline == 'IndiGo' else 0,
        'Airline_Jet Airways': 1 if selected_airline == 'Jet Airways' else 0,
        'Airline_Jet Airways Business': 1 if selected_airline == 'Jet Airways Business' else 0,
        'Airline_Multiple carriers': 1 if selected_airline == 'Multiple carriers' else 0,
        'Airline_Multiple carriers Premium economy': 1 if selected_airline == 'Multiple carriers Premium economy' else 0,
        'Airline_SpiceJet': 1 if selected_airline == 'SpiceJet' else 0,
        'Airline_Trujet': 1 if selected_airline == 'Trujet' else 0,
        'Airline_Vistara': 1 if selected_airline == 'Vistara' else 0,
        'Airline_Vistara Premium economy': 1 if selected_airline == 'Vistara Premium economy' else 0,
        'Source_Banglore': 1 if selected_source == 'Banglore' else 0,
        'Source_Chennai': 1 if selected_source == 'Chennai' else 0,
        'Source_Delhi': 1 if selected_source == 'Delhi' else 0,
        'Source_Kolkata': 1 if selected_source == 'Kolkata' else 0,
        'Source_Mumbai': 1 if selected_source == 'Mumbai' else 0,
        'Destination_Banglore': 1 if selected_destination == 'Banglore' else 0,
        'Destination_Cochin': 1 if selected_destination == 'Cochin' else 0,
        'Destination_Delhi': 1 if selected_destination == 'Delhi' else 0,
        'Destination_Hyderabad': 1 if selected_destination == 'Hyderabad' else 0,
        'Destination_Kolkata': 1 if selected_destination == 'Kolkata' else 0,
        'Destination_New Delhi': 1 if selected_destination == 'New Delhi' else 0,
        # Convert to numeric
        'Total_Stops': ['Non-stop', '1 stop', '2 stops', '3 stops', '4 stops'].index(selected_stops),
        'Duration_min': duration,
        # Placeholder feature, update as needed
        'Len_Route': len(selected_source + selected_destination),
        'Additional_Info_1 Long layover': 1 if long_layover else 0,
        'Additional_Info_1 Short layover': 1 if short_layover else 0,
        'Additional_Info_Business class': 1 if business_class else 0,
        'Additional_Info_Change airports': 1 if change_airports else 0,
        'Additional_Info_In-flight meal not included': 1 if meal_included else 0,
        'Additional_Info_No check-in baggage included': 1 if no_check_in_baggage else 0,
        'Additional_Info_Red-eye flight': 1 if red_eye_flight else 0,
        'month_3': 1 if month_of_journey == 3 else 0,
        'month_4': 1 if month_of_journey == 4 else 0,
        'month_5': 1 if month_of_journey == 5 else 0,
        'month_6': 1 if month_of_journey == 6 else 0,
        'day_1': 1 if day_of_journey == 1 else 0,
        'day_12': 1 if day_of_journey == 12 else 0,
        'day_15': 1 if day_of_journey == 15 else 0,
        'day_18': 1 if day_of_journey == 18 else 0,
        'day_21': 1 if day_of_journey == 21 else 0,
        'day_24': 1 if day_of_journey == 24 else 0,
        'day_27': 1 if day_of_journey == 27 else 0,
        'day_3': 1 if day_of_journey == 3 else 0,
        'day_6': 1 if day_of_journey == 6 else 0,
        'day_9': 1 if day_of_journey == 9 else 0
    }

    # Convert the features dictionary to a DataFrame
    input_df = pd.DataFrame([features])

    # Find the matching row in predictions_df that corresponds to the input features
    matching_row = predictions_df.loc[
        (predictions_df['Airline_Air Asia'] == input_df['Airline_Air Asia'][0]) &
        (predictions_df['Source_Banglore'] == input_df['Source_Banglore'][0]) &
        (predictions_df['Destination_Banglore'] == input_df['Destination_Banglore'][0]) &
        (predictions_df['Total_Stops'] == input_df['Total_Stops'][0]) &
        (predictions_df['Duration_min'] == input_df['Duration_min'][0])
    ]

    # Extract the predicted price from the matching row
    if not matching_row.empty:
        predicted_price = matching_row['Prdicted_Price'].values[0]
        st.write(f"Predicted Flight Price: ₹{predicted_price:.2f}")
    else:
        st.write("No matching flight details found.")
