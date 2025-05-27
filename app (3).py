import streamlit as st
from datetime import datetime
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(
    page_title="BloodReady | Blood Donation Eligibility",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar summary panel
with st.sidebar:
    st.markdown("## 🧾 Form Summary")
    st.write("Fill out the form on the right to determine blood donation eligibility based on Korean Red Cross criteria.")
    st.markdown("---")
    st.markdown("This tool is designed to help individuals understand if they meet the criteria before visiting a donation center.")
    st.markdown("Made by Ahyoung Bella Kim Co-Chair of ABO Supporters")

# --- Global Styling ---
st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Helvetica Neue', sans-serif;
        background-color: #f9fafb;
        color: #111827;
    }
    .stApp {
        padding: 1rem 2rem;
    }
    .stTitle > h1 {
        font-weight: 800;
        color: #1f2937;
        font-size: 2.4em;
        margin-bottom: 0.5em;
    }
    .stButton > button {
        background-color: #ef4444;
        color: white;
        font-weight: bold;
        border-radius: 0.6rem;
        padding: 0.7em 1.4em;
        font-size: 1rem;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #dc2626;
    }
    .section-box {
        background-color: white;
        padding: 2rem;
        margin: 1.5rem auto;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }
    .stRadio > div {
        padding: 0.2rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("BloodReady | Blood Donation Eligibility Checker")

# Use columns to eliminate center box look
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    with st.container():
        language = st.radio("🌐 Select Language / 언어 선택", ["English", "한국어"])

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

        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader(text['age'][language])
        age = st.slider(text['age'][language], min_value=10, max_value=100, step=1)
        st.subheader(text['weight'][language])
        weight = st.slider(text['weight'][language], min_value=30, max_value=150, step=1)
        st.subheader(text['well'][language])
        feeling_well = st.radio(text['well'][language], [text['yes'][language], text['no'][language]])
        st.subheader(text['hb_known'][language])
        hb_known = st.radio(text['hb_known'][language], [text['yes'][language], text['no'][language]])
        hb = 13.0
        if hb_known == text['yes'][language]:
            hb = st.slider(text['hb_level'][language], min_value=5.0, max_value=20.0, step=0.1)
        st.subheader(text['gender'][language])
        gender = st.radio(text['gender'][language], ["Female", "Male", "Other"])
        if gender == "Female":
            st.subheader(text['period'][language])
            menstruating = st.radio(text['period'][language], [text['yes'][language], text['no'][language], "Prefer not to say"])
            st.subheader(text['pregnant'][language])
            pregnancy = st.radio(text['pregnant'][language], [text['yes'][language], text['no'][language]])
        st.subheader(text['donation'][language])
        recent_donation = st.date_input(text['donation'][language], value=datetime.today())
        st.subheader(text['meds'][language])
        medication = st.radio(text['meds'][language], [text['yes'][language], text['no'][language]])
        st.subheader(text['tattoo'][language])
        tattoo = st.radio(text['tattoo'][language], [text['yes'][language], text['no'][language]])
        st.subheader(text['travel'][language])
        travel = st.radio(text['travel'][language], [text['yes'][language], text['no'][language]])

        malaria_risk = False
        country = ""
        region_detail = ""
        if travel == text['yes'][language]:
            country = st.text_input(text['country'][language])
            region_detail = st.text_input(text['region'][language])
            if country and region_detail:
                st.info(text['lookup'][language])
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
                regions = malaria_dataset.get(country.title(), [])
                if any(risk.lower() in region_detail.lower() for risk in regions):
                    malaria_risk = True

        # --- Results ---
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
                if (datetime.today() - recent_donation).days < 56:
                    eligible = False
                    reasons.append("Donated within the last 8 weeks")
            except:
                pass
            if medication == text['yes'][language]:
                eligible = False
                reasons.append("Currently on medication")
            if tattoo == text['yes'][language]:
                eligible = False
                reasons.append("Recent tattoo or piercing")
            if gender == "Female":
                if menstruating == text['yes'][language]:
                    reasons.append("Currently menstruating")
                if pregnancy == text['yes'][language]:
                    eligible = False
                    reasons.append("Pregnant or recently gave birth")
            if travel == text['yes'][language] and malaria_risk:
                eligible = False
                reasons.append("Visited malaria-risk area")

            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.subheader(text['result'][language])
            if eligible:
                st.success("✅ You are eligible to donate blood!")
            else:
                st.error("❌ You are not eligible to donate blood at this time.")
                for reason in reasons:
                    st.markdown(f"- {reason}")
            st.markdown('</div>', unsafe_allow_html=True)
