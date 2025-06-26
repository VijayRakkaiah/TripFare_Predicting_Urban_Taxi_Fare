import pandas as pd
import numpy as np
import pickle
import streamlit as st
from datetime import datetime
from datetime import time

st.set_page_config(
    page_title="Taxi Fare Prediction",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the trained model
with open('best_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Title
st.title("Taxi Fare Prediction (XGBoost)")

# Create three columns evenly spaced
col1, col2, col3 = st.columns(3)

# Column 1
with col1:
    st.markdown("#### Trip Date & Time")
    now = datetime.now()
    selected_date = st.date_input("Select Date", value=now.date(), min_value=now.date())
    selected_time = st.time_input("Select Time", value=time(now.hour, now.minute))

    user_datetime = datetime.combine(selected_date, selected_time)
    day_of_week = user_datetime.weekday()
    hour = user_datetime.hour
    am_pm = 0 if hour < 12 else 1
    is_night = 1 if hour >= 22 or hour <= 5 else 0

    with st.expander("Show Extracted Date/Time Features"):
        st.json({
            "day_of_week": day_of_week,
            "hour": hour,
            "am_pm": am_pm,
            "is_night": is_night
        })

# Column 2
with col2:
    st.markdown("#### Ride Information")
    passenger_count = st.slider("Passenger Count", 1, 7, 1)
    distance_km = st.number_input("Distance (km)", min_value=0.0, format="%.2f")
    payment_type = st.selectbox("Payment Type", [
        "1 = UPI", "2 = Cash", "3 = Credit card", "4 = Debit card"
    ])
    payment_type = int(payment_type.split(" = ")[0])  # Extract number

# Column 3
with col3:
    st.markdown("#### Charges")
    extra = st.number_input("Extra charges due to peak time", min_value=0.0, format="%.2f")
    tip_amount = st.number_input("Tip Amount", min_value=0.0, format="%.2f")
    tolls_amount = st.number_input("Tolls Amount", min_value=0.0, format="%.2f")

# Prediction Section
st.markdown("---")
if st.button("Predict Fare"):
    input_data = pd.DataFrame([{
        "passenger_count": passenger_count,
        "payment_type": payment_type,
        "extra": extra,
        "tip_amount": tip_amount,
        "tolls_amount": tolls_amount,
        "distance_km": distance_km,
        "day_of_week": day_of_week,
        "am_pm": am_pm,
        "hour": hour,
        "is_night": is_night
    }])

    # Apply log transformation to distance
    input_data['distance_km'] = np.log1p(input_data['distance_km'])

    # Predict using the loaded model
    prediction = model.predict(input_data)[0]
    st.success(f"Predicted Fare: ${prediction:.2f}")
