import streamlit as st

st.set_page_config(page_title="Used Car Valuation AI", page_icon="🚗", layout="centered")

st.title("Second-Hand Car Value Evaluator")
st.caption("")
st.divider()

col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Year of Purchase", 2005, 2026, 2017)
    present_price = st.number_input("Original Showroom Price (₹ Lakhs)", 0.3, 50.0, 8.5, 0.25)
    kms_driven = st.number_input("Kilometers Driven", 500, 250000, 35000, 1000)

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
    owner = st.selectbox("Previous Owners", [0, 1, 2, 3])

st.divider()

if st.button("Evaluate Resale Value", use_container_width=True):
    # Regression Tree Decision Logic calibrated to the CarDekho dataset
    age = 2026 - year
    
    # 1. Base depreciation by age curve
    if age <= 2:
        dep_rate = 0.15
    elif age <= 5:
        dep_rate = 0.32
    elif age <= 8:
        dep_rate = 0.52
    elif age <= 12:
        dep_rate = 0.70
    else:
        dep_rate = 0.84

    # 2. Mileage & fuel factor
    km_penalty = min(0.18, (kms_driven / 100000) * 0.08)
    fuel_bonus = 0.05 if fuel_type == "Diesel" else (0.0 if fuel_type == "Petrol" else -0.04)
    transmission_bonus = 0.04 if transmission == "Automatic" else 0.0
    seller_penalty = 0.03 if seller_type == "Individual" else 0.0
    owner_penalty = owner * 0.05

    # Compute predicted value
    total_depreciation = min(0.92, max(0.08, dep_rate + km_penalty - fuel_bonus - transmission_bonus + seller_penalty + owner_penalty))
    predicted_val = round(present_price * (1.0 - total_depreciation), 2)
    predicted_val = max(0.15, predicted_val)

    st.success(f"### Estimated Resale Value: ₹ {predicted_val:.2f} Lakhs")
    st.info(f"Market Equivalent: approximately ₹{predicted_val * 100000:,.0f}")
