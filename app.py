import Orange
import pandas as pd
import streamlit as st

st.title("🚗 Second-Hand Car Value Evaluator")

# 1. Load the model exported from your Orange canvas
model = Orange.classification.load_learner("car_value_estimator.pkcls")

# 2. Collect inputs matching your exact Orange columns
year = st.number_input("Year of Purchase", 2005, 2026, 2017)[cite: 11]
present_price = st.number_input("Original Showroom Price (₹ Lakhs)", 0.5, 50.0, 8.5)[cite: 11]
kms_driven = st.number_input("Kilometers Driven", 500, 250000, 35000)[cite: 11]
fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])[cite: 11]
seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])[cite: 11]
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])[cite: 11]
owner = st.selectbox("Previous Owners", [0, 1, 2, 3])[cite: 11]

# 3. Predict when button is clicked
if st.button("Evaluate Resale Value"):
    data = pd.DataFrame([{
        "Year": year,
        "Present_Price": present_price,
        "Kms_Driven": kms_driven,
        "Fuel_Type": fuel_type,
        "Seller_Type": seller_type,
        "Transmission": transmission,
        "Owner": owner,
        "Selling_Price": 0.0  # Placeholder target required by Orange
    }])[cite: 11]
    
    # Send row into the Orange model
    table = Orange.data.Table.from_pandas(data)
    predicted_val = float(model(table[0]))
    
    st.success(f"Estimated Resale Value: ₹ {predicted_val:.2f} Lakhs")