
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="혈액자격봇 – BloodReady", layout="centered")

st.title("🩸 BloodReady | 헌혈 가능 여부 자가진단")
st.markdown("""
#### 🇰🇷 한글과 🇺🇸 영어로 자가진단을 진행할 수 있습니다.
""")

st.header("1. 기본 정보 / Basic Info")
with st.form("eligibility_form"):
    language = st.radio("언어 선택 / Language", ["한국어", "English"])
    age = st.number_input("나이 / Age", min_value=10, max_value=100, step=1)
    weight = st.number_input("체중 (kg) / Weight (kg)", min_value=30.0, step=0.5)
    feeling_well = st.radio("오늘 건강 상태가 양호하십니까? / Are you feeling well today?", ["예 / Yes", "아니요 / No"])

    hb_known = st.radio("헤모글로빈 수치를 알고 계십니까? / Do you know your Hemoglobin (Hb) level?", ["예 / Yes", "아니요 / No"])
    if hb_known == "예 / Yes":
        hb = st.number_input("Hb 수치 (g/dL) / Hemoglobin level (g/dL)", min_value=5.0, max_value=20.0, step=0.1)

    gender = st.radio("성별 / Gender", ["여성 / Female", "남성 / Male", "기타 / Other"])
    if gender == "여성 / Female":
        menstruating = st.radio("현재 생리 중이십니까? / Are you currently on your period?", ["예 / Yes", "아니요 / No", "선택 안함 / Prefer not to say"])
        pregnancy = st.radio("현재 임신 중이거나 최근 6개월 내 출산하셨습니까? / Are you pregnant or recently gave birth?", ["예 / Yes", "아니요 / No"])

    recent_donation = st.date_input("마지막 헌혈 날짜 / Last blood donation date", value=datetime.today())

    medication = st.radio("현재 약물을 복용 중입니까? / Are you currently taking any medication?", ["예 / Yes", "아니요 / No"])
    tattoo = st.radio("최근 6개월 이내 문신 또는 피어싱을 하셨습니까? / Any tattoos or piercings in the last 6 months?", ["예 / Yes", "아니요 / No"])

    malaria_travel = st.radio("최근 1년간 말라리아 위험 지역을 방문하셨습니까? / Traveled to a malaria-risk area in the past year?", ["예 / Yes", "아니요 / No"])
    if malaria_travel == "예 / Yes":
        country = st.selectbox("어느 나라를 방문하셨습니까? / Which country did you visit?", ["한국 / Korea", "필리핀 / Philippines", "인도 / India", "기타 / Other"])
        if country == "한국 / Korea":
            region = st.text_input("한국 내 어느 지역이었습니까? / Where in Korea?")

    submitted = st.form_submit_button("결과 확인 / Check Eligibility")

    if submitted:
        eligible = True
        reasons = []

        if age < 16:
            eligible = False
            reasons.append("16세 미만 / Under 16")
        if weight < 50:
            eligible = False
            reasons.append("체중 50kg 미만 / Under 50 kg")
        if feeling_well == "아니요 / No":
            eligible = False
            reasons.append("현재 건강 상태 불량 / Not feeling well")
        if hb_known == "예 / Yes" and hb < 12.5:
            eligible = False
            reasons.append("헤모글로빈 수치 낮음 / Low hemoglobin (<12.5 g/dL)")

        # Safe handling of blood donation date
        try:
            days_since = (datetime.today() - recent_donation).days
        except:
            days_since = 9999
        if days_since < 56:
            eligible = False
            reasons.append("최근 8주 이내 헌혈 / Last donation within 8 weeks")

        if medication == "예 / Yes":
            eligible = False
            reasons.append("약물 복용 중 / On medication")
        if tattoo == "예 / Yes":
            eligible = False
            reasons.append("최근 문신/피어싱 / Recent tattoo or piercing")
        if gender == "여성 / Female":
            if menstruating == "예 / Yes":
                reasons.append("생리 중 / On period — consider iron level")
            if pregnancy == "예 / Yes":
                eligible = False
                reasons.append("임신/출산으로 인해 헌혈 불가 / Pregnant or recently gave birth")
        if malaria_travel == "예 / Yes":
            eligible = False
            reasons.append(f"말라리아 위험 지역 방문 / Travelled to malaria-risk area ({country})")
            if country == "한국 / Korea" and region:
                reasons.append(f"방문 지역: {region}")

        st.subheader("결과 / Result")
        if eligible:
            st.success("✅ 헌혈이 가능합니다! / You are eligible to donate blood!")
        else:
            st.error("❌ 현재 헌혈이 불가합니다 / You are not eligible to donate right now.")
            for reason in reasons:
                st.write(f"- {reason}")
