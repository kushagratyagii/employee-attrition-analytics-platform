import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("models/attrition_streamlit.pkl")

# Page config
st.set_page_config(
    page_title="Employee Attrition Predictor",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Employee Attrition Analytics Platform")

st.markdown("""
Predict employee attrition risk using an XGBoost model trained on HR analytics data.
""")
st.markdown(
    "Predict whether an employee is likely to leave the organization."
)

st.divider()

# Inputs

age = st.sidebar.slider("Age", 18, 60, 30)

monthly_income = st.sidebar.number_input(
    "Monthly Income",
    min_value=1000,
    max_value=50000,
    value=10000,
    step=500
)

distance_from_home = st.sidebar.slider(
    "Distance From Home",
    1,
    30,
    5
)

overtime = st.sidebar.selectbox(
    "OverTime",
    ["Yes", "No"]
)

stock_option_level = st.sidebar.selectbox(
    "Stock Option Level",
    [0, 1, 2, 3]
)

job_satisfaction = st.sidebar.selectbox(
    "Job Satisfaction",
    [1, 2, 3, 4]
)

environment_satisfaction = st.sidebar.selectbox(
    "Environment Satisfaction",
    [1, 2, 3, 4]
)

relationship_satisfaction = st.sidebar.selectbox(
    "Relationship Satisfaction",
    [1, 2, 3, 4]
)

num_companies_worked = st.sidebar.slider(
    "Number of Companies Worked",
    0,
    10,
    2
)

years_with_curr_manager = st.sidebar.slider(
    "Years With Current Manager",
    0,
    20,
    3
)

st.divider()

if st.button("Predict Attrition Risk"):

    input_df = pd.DataFrame({
        "Age": [age],
        "MonthlyIncome": [monthly_income],
        "DistanceFromHome": [distance_from_home],
        "OverTime": [overtime],
        "StockOptionLevel": [stock_option_level],
        "JobSatisfaction": [job_satisfaction],
        "EnvironmentSatisfaction": [environment_satisfaction],
        "RelationshipSatisfaction": [relationship_satisfaction],
        "NumCompaniesWorked": [num_companies_worked],
        "YearsWithCurrManager": [years_with_curr_manager]
    })

    prediction = model.predict(input_df)[0]

    probability = model.predict_proba(input_df)[0][1]
    st.subheader("Top Attrition Drivers Identified by SHAP")
    

    st.info("""
    • Overtime

    • Monthly Income

    • Distance From Home

    • Stock Option Level

    • Age
    """)

    st.subheader("Prediction Result")

    if probability < 0.30:
        st.success(
            f"🟢 Low Attrition Risk ({probability:.1%})"
        )

    elif probability < 0.60:
        st.warning(
            f"🟡 Medium Attrition Risk ({probability:.1%})"
        )

    else:
        st.error(
            f"🔴 High Attrition Risk ({probability:.1%})"
        )

    st.progress(float(probability))

    st.write(
        f"Probability of Attrition: **{probability:.2%}**"
    
    )