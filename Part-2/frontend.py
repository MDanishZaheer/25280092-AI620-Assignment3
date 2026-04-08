# Name : M Danish Zaheer
# Roll No : 25280092

# Taken help from: https://docs.streamlit.io/get-started/tutorials/create-an-app
# Also taken help from gpt multiple times to debug and understnad the need and code syntax

# importing necessary libraries
import streamlit as st
import requests

st.title("PakWheels Price Category Predictor for Assignment-3-Part-2 [25280092]")

# creating input fields for the user to enter car details 
year = st.number_input("Year", min_value=0, max_value=2026)
engine = st.number_input("Engine", min_value=0, value=1300)
mileage = st.number_input("Mileage", min_value=0, value=45000)
city = st.text_input("City (e.g. Lahore, Karachi)", value="")
body = st.text_input("Body (e.g. Sedan, Hatchback, SUV)", value="")
make = st.text_input("Make (e.g. Honda, Suzuki, Toyota)", value="")
model = st.text_input("Model (e.g. City, Mehran, Corolla)", value="")
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "Hybrid", "CNG"])
color = st.text_input("Color (e.g. White, Black, Silver)", value="")
registered = st.text_input("Registered (e.g. Punjab, Sindh)", value="")


# when the user clicks the Predict button, we send a POST request to the FastAPI backend with the input data and display the prediction result
if st.button("Predict"):
    data = {"year": year, "engine": engine, "mileage": mileage, "city": city, "body": body, "make": make, "model": model,
        "transmission": transmission, "fuel": fuel, "color": color, "registered": registered}

    # sending a post request to the FastAPI backend with the input data
    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    # safety check
    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['label']}")
        st.write(result)
    else:
        st.error("Error in prediction")
        st.write(response.text)
