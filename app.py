import streamlit as st
import pickle
import datetime
from datetime import datetime as dt
import pandas as pd

model = pickle.load(open('best_xgb_model.pkl', 'rb'))
    

# Title
st.title("🔍 Preventing Digital Fraud in UPI with Predictive Analytics")

# Date input
tran_date = st.date_input("Transaction Date", datetime.date.today())
selected_date = dt.combine(tran_date, dt.min.time())
month = selected_date.month
day = selected_date.day
day_of_week = selected_date.strftime('%A')

# User inputs
transaction_type = st.selectbox("Transaction Type", ['Send', 'Receive', 'Merchant Payment'])
location = st.selectbox("Location", ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata',
                                     'Hyderabad', 'Ahmedabad', 'Pune', 'Surat', 'Jaipur'])
device_type = st.selectbox("Device Type", ['Mobile', 'Tablet'])
is_rooted_device = st.selectbox("Is Rooted Device?", ['Yes', 'No'])
network_type = st.selectbox("Network Type", ['Wi-Fi', '4G', '5G'])
time_of_day = st.selectbox("Time of Day", ['Morning', 'Afternoon', 'Evening', 'Night'])
amount = st.number_input("Transaction Amount", min_value=0.0, step=0.1)

# Label Encoding Manually
label_encodings = {
    'transaction_type': {'Send': 0, 'Receive': 1, 'Merchant Payment': 2},
    'location': {'Mumbai': 0, 'Delhi': 1, 'Bangalore': 2, 'Chennai': 3, 'Kolkata': 4,
                 'Hyderabad': 5, 'Ahmedabad': 6, 'Pune': 7, 'Surat': 8, 'Jaipur': 9},
    'device_type': {'Mobile': 0, 'Tablet': 1},
    'is_rooted_device': {'No': 0, 'Yes': 1},
    'network_type': {'Wi-Fi': 0, '4G': 1, '5G': 2},
    'time_of_day': {'Morning': 0, 'Afternoon': 1, 'Evening': 2, 'Night': 3},
    'day_of_week': {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                    'Friday': 4, 'Saturday': 5, 'Sunday': 6}
}

# Prepare input in correct format (removed 'hour')
input_df = pd.DataFrame({
    'amount': [amount],
    'transaction_type': [label_encodings['transaction_type'][transaction_type]],
    'location': [label_encodings['location'][location]],
    'device_type': [label_encodings['device_type'][device_type]],
    'is_rooted_device': [label_encodings['is_rooted_device'][is_rooted_device]],
    'network_type': [label_encodings['network_type'][network_type]],
    'time_of_day': [label_encodings['time_of_day'][time_of_day]],
    'month': [month],
    'day': [day],
    'day_of_week': [label_encodings['day_of_week'][day_of_week]]
})

# Predict
import time

if st.button("Check Transaction"):
    with st.spinner('Analyzing transaction...'):
        time.sleep(1)  # Show spinner for 1 seconds
        try:
            prediction = model.predict(input_df)[0]
            if prediction == 0:
                st.success("✅ Legitimate Transaction.")
                st.markdown(
                    """
                    <style>
                    .stApp {
                        background-color: #d4edda;  /* light green */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("🚨 Fraudulent Transaction Detected!")
                st.markdown(
                    """
                    <style>
                    .stApp {
                        background-color: #f8d7da;  /* light red */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"❌ Prediction Error: {str(e)}")



