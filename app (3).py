import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="혈액 자격 확인 앱: BloodReady",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
        background-color: #FAFAFA;
    }
    .stButton > button {
        background-color: #D62828;
        color: white;
        font-weight: 600;
        border-radius: 0.5rem;
        padding: 0.6em 1.2em;
        font-size: 1rem;
    }
    .stRadio > div {
        padding: 0.2rem 0;
    }
    .stTitle > h1 {
        font-weight: 700;
        color: #222222;
        border-left: 5px solid #D62828;
        padding-left: 12px;
        margin-bottom: 1rem;
    }
    .stHeader > h2 {
        color: #444444;
    }
</style>
""", unsafe_allow_html=True)

st.title("BloodReady | 헌혈 가능 여부 자가진단")

# Real-time language toggle
language = st.radio("Select Language / 언어 선택", ["English", "한국어"])

text = {
    "age": {"English": "Age", "한국어": "나이"},
    "weight": {"English": "Weight (kg)", "한국어": "체중 (kg)"},
    "well": {"English": "Are you feeling well today?", "한국어": "오늘 건강 상태가 양호하십니까?"},
    "hb_known": {"English": "Do you know your Hemoglobin (Hb) level?", "한국어": "헤모글로빈 수치를 알고 계십니까?"},
    "hb_level": {"English": "Hemoglobin level (g/dL)", "한국어": "Hb 수치 (g/dL)"},
    "gender": {"English": "Gender", "한국어": "성별"},
    "period": {"English": "Are you currently on your period?", "한국어": "현재 생리 중이십니까?"},
    "pregnant": {"English": "Are you pregnant or recently gave birth?", "한국어": "현재 임신 중이거나 최근 6개월 내 출산하셨습니까?"},
    "donation": {"English": "Last blood donation date", "한국어": "마지막 헌혈 날짜"},
    "meds": {"English": "Are you currently taking any medication?", "한국어": "현재 약물을 복용 중입니까?"},
    "tattoo": {"English": "Any tattoos or piercings in the last year?", "한국어": "최근 1년 이내 문신 또는 피어싱을 하셨습니까?"},
    "travel": {"English": "Have you traveled abroad in the last year?", "한국어": "최근 1년간 해외여행을 하셨습니까?"},
    "country": {"English": "Which country did you visit?", "한국어": "방문한 국가를 선택해 주세요"},
    "region": {"English": "Which region(s) did you visit in that country?", "한국어": "그 나라 내 방문 지역을 입력해 주세요"},
    "submit": {"English": "Check Eligibility", "한국어": "결과 확인"},
    "result": {"English": "Result", "한국어": "결과"},
    "yes": {"English": "Yes", "한국어": "예"},
    "no": {"English": "No", "한국어": "아니요"},
    "lookup": {"English": "Looking up malaria risk...", "한국어": "말라리아 위험 여부 확인 중..."}
}

st.header(f"{text['age'][language]}")

st.header(f"1. {text['age'][language]} / {text['age']['한국어'] if language == 'English' else text['age']['English']}")

age = st.number_input(text['age'][language], min_value=10, max_value=100, step=1)
weight = st.number_input(text['weight'][language], min_value=30.0, step=0.5)
feeling_well = st.radio(text['well'][language], [text['yes'][language], text['no'][language]])

hb_known = st.radio(text['hb_known'][language], [text['yes'][language], text['no'][language]])
if hb_known == text['yes'][language]:
    hb = st.number_input(text['hb_level'][language], min_value=5.0, max_value=20.0, step=0.1)

gender = st.radio(text['gender'][language], ["Female", "Male", "Other"])
if gender == "Female":
    menstruating = st.radio(text['period'][language], [text['yes'][language], text['no'][language], "Prefer not to say"])
    pregnancy = st.radio(text['pregnant'][language], [text['yes'][language], text['no'][language]])

recent_donation = st.date_input(text['donation'][language], value=datetime.today())

medication = st.radio(text['meds'][language], [text['yes'][language], text['no'][language]])
tattoo = st.radio(text['tattoo'][language], [text['yes'][language], text['no'][language]])

travel = st.radio(text['travel'][language], [text['yes'][language], text['no'][language]])
region_detail = ""
malaria_risk = False
if travel == text['yes'][language]:
    country = st.text_input(text['country'][language])
    region_detail = st.text_input(text['region'][language])

    if country and region_detail:
        st.info(text['lookup'][language])
        try:
            malaria_dataset = {
                "Philippines": ["Palawan", "Mindanao", "Sulu"],
                "India": ["Assam", "Odisha", "Jharkhand", "Chhattisgarh"],
                "Indonesia": ["Papua", "Kalimantan", "NTT", "Sulawesi"],
                "Malaysia": ["Sabah", "Sarawak"],
                "Papua New Guinea": ["Western", "Madang", "East Sepik"],
                "Thailand": ["Tak", "Ubon Ratchathani", "Yala"],
                "Myanmar": ["Kayin", "Rakhine", "Chin"],
                "Vietnam": ["Gia Lai", "Quang Tri"],
                "Cambodia": ["Pursat", "Ratanakiri"]
            }
            risk_regions = malaria_dataset.get(country.title(), [])
            if any(risk.lower() in region_detail.lower() for risk in risk_regions):
                malaria_risk = True
        except:
            malaria_risk = False

if st.button(text['submit'][language]):
    eligible = True
    reasons = []

    if age < 16:
        eligible = False
        reasons.append("Under 16")
    if weight < 50:
        eligible = False
        reasons.append("Under 50 kg")
    if feeling_well == text['no'][language]:
        eligible = False
        reasons.append("Not feeling well")
    if hb_known == text['yes'][language] and hb < 12.5:
        eligible = False
        reasons.append("Low hemoglobin (<12.5 g/dL)")

    try:
        days_since = (datetime.today() - recent_donation).days
    except:
        days_since = 9999
    if days_since < 56:
        eligible = False
        reasons.append("Donated within last 8 weeks")

    if medication == text['yes'][language]:
        eligible = False
        reasons.append("On medication")
    if tattoo == text['yes'][language]:
        eligible = False
        reasons.append("Recent tattoo or piercing")
    if gender == "Female":
        if menstruating == text['yes'][language]:
            reasons.append("On period — consider iron level")
        if pregnancy == text['yes'][language]:
            eligible = False
            reasons.append("Pregnant or recently gave birth")

    if travel == text['yes'][language]:
        reasons.append(f"Recent travel to {country} - {region_detail}")
        if malaria_risk:
            eligible = False
            reasons.append("Visited malaria-risk area")

    st.subheader(text['result'][language])
    if eligible:
        st.success("✅ You are eligible to donate blood!")
    else:
        st.error("❌ You are not eligible to donate blood at this time.")
        for reason in reasons:
            st.write(f"- {reason}")
