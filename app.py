
import streamlit as st
from datetime import datetime, timedelta

# -------------------------------
# 1. Blood Donation Eligibility Chatbot
# -------------------------------
st.title("🩸 Blood Donation Eligibility & Iron Tracker App")
st.header("1. Blood Donation Eligibility Checker")

with st.form("eligibility_form"):
    age = st.number_input("How old are you?", min_value=10, max_value=100, step=1)
    weight = st.number_input("What is your weight (kg)?", min_value=30.0, step=0.5)
    hb_known = st.radio("Do you know your Hemoglobin (Hb) level?", ["Yes", "No"])
    if hb_known == "Yes":
        hb = st.number_input("Enter your Hemoglobin level (g/dL):", min_value=5.0, max_value=20.0, step=0.1)
    symptoms = st.radio("Are you feeling healthy today (no fever, fatigue, etc.)?", ["Yes", "No"])
    period = st.radio("Are you currently on your menstrual period?", ["Yes", "No", "Prefer not to say"])
    last_donation = st.date_input("When was your last blood donation? (or skip if never)", value=datetime.today())
    meds = st.radio("Are you on antibiotics or being treated for an illness?", ["Yes", "No"])
    malaria_zone = st.radio("Have you visited a malaria zone in the past year?", ["Yes", "No"])

    submitted = st.form_submit_button("Check Eligibility")

    if submitted:
        eligibility = True
        reasons = []

        if age < 16:
            eligibility = False
            reasons.append("Underage (<16).")
        if weight < 50:
            eligibility = False
            reasons.append("Underweight (<50 kg).")
        if hb_known == "Yes" and hb < 12.5:
            eligibility = False
            reasons.append("Low hemoglobin (<12.5 g/dL).")
        if symptoms == "No":
            eligibility = False
            reasons.append("Not feeling healthy today.")
        if (datetime.today() - last_donation).days < 56:
            eligibility = False
            reasons.append("Donated blood less than 8 weeks ago.")
        if meds == "Yes":
            eligibility = False
            reasons.append("Currently on medication.")
        if malaria_zone == "Yes":
            eligibility = False
            reasons.append("Recent travel to malaria-prone area.")

        st.subheader("Eligibility Result")
        if eligibility:
            st.success("✅ You are eligible to donate blood today!")
        else:
            st.error("❌ You are not eligible right now.")
            for reason in reasons:
                st.write(f"- {reason}")


# -------------------------------
# 2. Iron Tracker via Diet
# -------------------------------
st.header("2. Daily Iron Intake Tracker")
st.write("Select the iron-rich foods you ate today:")

iron_sources = {
    "Spinach (1 cup)": 6.4,
    "Beef (100g)": 2.6,
    "Chicken liver (100g)": 9.0,
    "Tofu (1/2 block)": 3.4,
    "Lentils (1 cup)": 6.6,
    "Dark chocolate (30g)": 3.3,
    "Pumpkin seeds (30g)": 2.5,
    "Broccoli (1 cup)": 1.0,
    "Fortified cereal (1 bowl)": 8.0,
    "Egg (1)": 0.9
}

selected_foods = st.multiselect("Iron-rich foods consumed:", options=list(iron_sources.keys()))

if st.button("Calculate Iron Intake"):
    total_iron = sum([iron_sources[food] for food in selected_foods])
    st.subheader("🧪 Iron Intake Result")
    st.write(f"You consumed approximately **{total_iron:.1f} mg** of iron today.")
    if total_iron < 8:
        st.warning("Your intake is lower than the recommended minimum (8–18 mg/day). Consider adding more iron-rich foods.")
    else:
        st.success("Great job! Your iron intake is within a healthy range.")
