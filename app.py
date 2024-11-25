import streamlit as st
import joblib
import pandas as pd
st.title("Medical Insurance Finder")
model = joblib.load('model2.pkl')

st.markdown("""
    <style>
    /* Styling for app title, inputs, buttons, etc. */
    /* (Same as before, omitted for brevity) */
    </style>
""", unsafe_allow_html=True)

st.header("Enter Patient Details")
age = st.number_input("Age",min_value=0)
sex = st.selectbox("Gender",options = ['Male','Female'])
bmi = st.number_input("Bmi",min_value=0.0)
smoker = st.selectbox("Smoker",options=['Yes','No'])

# Sidebar calculations
st.sidebar.header("Useful Calculations")

# BMI Calculation
st.sidebar.subheader("BMI Calculation")
weight = st.sidebar.number_input("Weight (in kg)", min_value=10, max_value=200, value=70, step=1)
height = st.sidebar.number_input("Height (in cm)", min_value=50, max_value=250, value=170, step=1)
height_m = height / 100
bmi = weight / (height_m ** 2)
st.sidebar.write(f"Calculated BMI: {bmi:.2f}")

# BMR Calculation (Basal Metabolic Rate)
st.sidebar.subheader("BMR Calculation")
if sex == 'Male':
    bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
else:
    bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
st.sidebar.write(f"Your BMR: {bmr:.2f} calories/day")

# TDEE Calculation (Total Daily Energy Expenditure based on activity)
activity_level = st.sidebar.selectbox("Activity Level", options=['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'])
activity_multiplier = {
    'Sedentary': 1.2,
    'Light': 1.375,
    'Moderate': 1.55,
    'Active': 1.725,
    'Very Active': 1.9
}
tdee = bmr * activity_multiplier[activity_level]
st.sidebar.write(f"Estimated TDEE: {tdee:.2f} calories/day")

# BMI Category
st.sidebar.subheader("BMI Category")
if bmi < 18.5:
    bmi_category = "Underweight"
elif 18.5 <= bmi < 24.9:
    bmi_category = "Normal weight"
elif 25 <= bmi < 29.9:
    bmi_category = "Overweight"
else:
    bmi_category = "Obese"
st.sidebar.write(f"BMI Category: {bmi_category}")

# Body Fat Percentage Estimate (based on BMI)
st.sidebar.subheader("Estimated Body Fat Percentage")
if sex == 'Male':
    body_fat = 1.20 * bmi + 0.23 * age - 16.2
else:
    body_fat = 1.20 * bmi + 0.23 * age - 5.4
st.sidebar.write(f"Estimated Body Fat Percentage: {body_fat:.2f}%")

# Ideal Body Weight (IBW)
st.sidebar.subheader("Ideal Body Weight (IBW)")
if sex == 'Male':
    ibw = 50 + 0.91 * (height - 152.4)
else:
    ibw = 45.5 + 0.91 * (height - 152.4)
st.sidebar.write(f"Ideal Body Weight: {ibw:.2f} kg")


if st.button("Predict Insurance Cost"):
    if age == 0:
        st.error('Age cannot be zero')
    elif bmi == 0.00:
        st.error('BMI cannnot be zero')
    else:
        sex = 1 if sex == "Male" else 0
        smoker = 1 if smoker == 'Yes' else 0

        features = [[age, sex, bmi, smoker]]
        
        predict = model.predict(features)
        st.success(f"Predicted Insurance Cost: {predict[0]:,.2f} Rupees")
