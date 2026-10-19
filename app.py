import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import streamlit as st

st.set_page_config(page_title="Used Car Valuation AI", page_icon="🚗")

st.title("🚗 Second-Hand Car Value Evaluator")
st.caption(
    "CBSE Class 12 AI Capstone Project — UN SDG Goal 8: Decent Work & Economic Growth"
)


# Train Decision Tree model directly on startup using the dataset
@st.cache_resource
def get_trained_model():
  df = pd.read_csv("car_data.csv")
  df.columns = df.columns.str.strip()

  features = [
      "Year",
      "Present_Price",
      "Kms_Driven",
      "Fuel_Type",
      "Seller_Type",
      "Transmission",
      "Owner",
  ]
  X = df[features]
  y = df["Selling_Price"]

  # Encode categorical columns
  X = pd.get_dummies(
      X,
      columns=["Fuel_Type", "Seller_Type", "Transmission"],
      drop_first=False,
      dtype=int,
  )
  feature_cols = list(X.columns)

  # Using DecisionTreeRegressor (Matches your Orange Tree widget)
  model = DecisionTreeRegressor(random_state=42)
  model.fit(X, y)
  return model, feature_cols


try:
  model, feature_cols = get_trained_model()
except Exception as e:
  st.error(
      f"Error loading 'car_data.csv'. Ensure car_data.csv is uploaded in your GitHub repo! Details: {e}"
  )
  st.stop()

# Inputs
col1, col2 = st.columns(2)

with col1:
  year = st.number_input("Year of Purchase", 2005, 2026, 2017)
  present_price = st.number_input(
      "Original Showroom Price (₹ Lakhs)", 0.5, 50.0, 8.5, 0.25
  )
  kms_driven = st.number_input("Kilometers Driven", 500, 250000, 35000, 1000)

with col2:
  fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
  seller_type = st.selectbox("Seller Type", ["Dealer", "Individual"])
  transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
  owner = st.selectbox("Previous Owners", [0, 1, 2, 3])

if st.button("Evaluate Resale Value", use_container_width=True):
  row = {
      "Year": year,
      "Present_Price": present_price,
      "Kms_Driven": kms_driven,
      "Owner": owner,
      f"Fuel_Type_{fuel_type}": 1,
      f"Seller_Type_{seller_type}": 1,
      f"Transmission_{transmission}": 1,
  }

  input_df = pd.DataFrame([row])
  for col in feature_cols:
    if col not in input_df.columns:
      input_df[col] = 0
  input_df = input_df[feature_cols]

  prediction = max(0.15, float(model.predict(input_df)[0]))

  st.success(f"### Estimated Resale Value: ₹ {prediction:.2f} Lakhs")
  st.info(f"Equivalent Value: approximately ₹{prediction * 100000:,.0f}")
