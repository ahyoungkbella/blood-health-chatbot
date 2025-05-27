
# BloodReady | Final Streamlit App with Full Functionality, Language Toggle, PDF, Email, Dashboard

import streamlit as st
from datetime import datetime
import base64
from io import BytesIO
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="BloodReady | Blood Donation Eligibility",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PDF Export Function ---
def create_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)
    for line in summary_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)
    return pdf

def get_pdf_download_link(pdf):
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="blood_eligibility_summary.pdf">📄 Download PDF Result</a>'
    return href

# --- Email Sending ---
def send_email(to_email, subject, body, pdf_buffer):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = to_email
    msg.set_content(body)
    msg.add_attachment(pdf_buffer.getvalue(), maintype='application', subtype='pdf', filename='blood_eligibility_summary.pdf')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@example.com', 'your_password')
        smtp.send_message(msg)

# --- Language Pref ---
language = st.sidebar.radio("🌐 Language / 언어", ["English", "한국어"])
is_kr = language == "한국어"

# --- Sidebar Info ---
with st.sidebar:
    st.markdown("## 🧾 Info")
    if is_kr:
        st.markdown("이 도구는 헌혈 자격 조건을 사전에 확인할 수 있도록 제작되었습니다.")
        st.markdown("헌혈 기준은 대한적십자사의 공식 가이드를 따릅니다.")
    else:
        st.markdown("This tool helps you check if you're eligible to donate blood before visiting a donation center.")
        st.markdown("Eligibility follows guidelines from the Korean Red Cross.")
    st.markdown("**Made by Ahyoung Bella Kim, Co-Chair of ABO Supporters**")

# --- Styling ---
st.markdown("""<style>
html, body, [class*='css'] {
    font-family: 'Helvetica Neue', sans-serif;
    background: linear-gradient(135deg, #fff5f7, #fefefe);
    color: #111827;
}
.section {
    background-color: white;
    padding: 2rem;
    margin: 2rem auto;
    border-radius: 20px;
    border: 2px solid #f3c5c5;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}
.photo-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.2rem;
    margin-top: 3rem;
}
.photo-grid img {
    width: 100%;
    border-radius: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
    border: 1px solid #eee;
}
</style>""", unsafe_allow_html=True)

# --- Title ---
st.markdown("""<div class='section'>
<h1 style='text-align:center; color:#d62828;'>BloodReady | 헌혈 자격 셀프 체크</h1>
<p style='text-align:center; color:#e63946;'>당신의 따뜻함이 생명이 됩니다.<br>Your Warmth Can Save a Life.</p>
</div>""", unsafe_allow_html=True)

# --- Form ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🩸 " + ("정보 입력" if is_kr else "Fill in your details"))

gender = st.radio("성별 / Gender", ["여성 / Female", "남성 / Male", "기타 / Other"] if is_kr else ["Female", "Male", "Other"])
if "여성" in gender or gender == "Female":
    menstruating = st.radio("현재 생리 중입니까?" if is_kr else "Are you currently on your period?", ["예 / Yes", "아니요 / No", "모름" if is_kr else "Prefer not to say"])
    pregnancy = st.radio("현재 임신 중이거나 출산 직후입니까?" if is_kr else "Are you pregnant or recently gave birth?", ["예 / Yes", "아니요 / No"])

donation_date = st.date_input("마지막 헌혈 날짜" if is_kr else "Last blood donation date", value=datetime.today())
tattoo = st.radio("최근 문신/피어싱 여부" if is_kr else "Recent tattoo/piercing?", ["예 / Yes", "아니요 / No"])
age = st.slider("나이" if is_kr else "Age", 10, 100, 20)
weight = st.slider("체중 (kg)" if is_kr else "Weight (kg)", 30, 150, 60)
feeling_well = st.radio("오늘 건강하십니까?" if is_kr else "Feeling well today?", ["예 / Yes", "아니요 / No"])
hb = st.slider("헤모글로빈 수치 (g/dL)" if is_kr else "Hemoglobin (Hb) Level (g/dL)", 5.0, 20.0, 13.0, step=0.1)
meds = st.radio("약 복용 여부" if is_kr else "Currently on medication?", ["예 / Yes", "아니요 / No"])
travel = st.radio("최근 1년간 해외여행 여부" if is_kr else "Have you traveled abroad recently?", ["예 / Yes", "아니요 / No"])
email = st.text_input("이메일 입력 (선택)" if is_kr else "Enter email (optional for PDF)")
country, region = "", ""
malaria_risk = False

if "예" in travel or travel == "Yes":
    country = st.text_input("방문 국가" if is_kr else "Country visited")
    region = st.text_input("방문 지역" if is_kr else "Region visited")
    malaria_data = {"India": ["Odisha", "Assam"], "Philippines": ["Palawan", "Mindanao"], "Indonesia": ["Papua", "Kalimantan"]}
    if country in malaria_data:
        if any(r.lower() in region.lower() for r in malaria_data[country]):
            malaria_risk = True

if st.button("결과 확인" if is_kr else "Check Eligibility"):
    try:
        days_since = (datetime.today() - donation_date).days
    except:
        days_since = 9999
    eligible = True
    reasons = []
    if age < 16: eligible, reasons = False, reasons + ["16세 미만" if is_kr else "Under 16"]
    if weight < 50: eligible, reasons = False, reasons + ["50kg 미만" if is_kr else "Under 50 kg"]
    if "아니요" in feeling_well or feeling_well == "No": eligible, reasons = False, reasons + ["컨디션 불량" if is_kr else "Not feeling well"]
    if hb < 12.5: eligible, reasons = False, reasons + ["Hb 수치 낮음" if is_kr else "Low hemoglobin"]
    if "예" in meds or meds == "Yes": eligible, reasons = False, reasons + ["약 복용 중" if is_kr else "Currently on medication"]
    if malaria_risk: eligible, reasons = False, reasons + ["말라리아 위험 지역 방문" if is_kr else "Visited malaria-risk region"]
    if ("여성" in gender or gender == "Female"):
        if "예" in menstruating or menstruating == "Yes":
            reasons.append("생리 중" if is_kr else "Currently menstruating")
        if "예" in pregnancy or pregnancy == "Yes":
            eligible, reasons = False, reasons + ["임신 또는 출산 직후" if is_kr else "Pregnant or recently gave birth"]
    if days_since < 56: eligible, reasons = False, reasons + ["8주 이내 헌혈" if is_kr else "Donated within 8 weeks"]
    if "예" in tattoo or tattoo == "Yes": eligible, reasons = False, reasons + ["문신/피어싱 있음" if is_kr else "Recent tattoo/piercing"]

    result_msg = "적합함" if eligible and is_kr else "부적합함" if not eligible and is_kr else "Eligible" if eligible else "Not Eligible"
    summary = f"Age: {age}\nWeight: {weight}kg\nHb: {hb}\nEligible: {result_msg}\nReasons:\n" + "\n".join(reasons)

    st.subheader("결과 / Result")
    if eligible:
        st.success("✅ 헌혈이 가능합니다!" if is_kr else "✅ You are eligible to donate blood!")
    else:
        st.error("❌ 현재 헌혈이 불가능합니다." if is_kr else "❌ You are not eligible to donate blood at this time.")
        for r in reasons:
            st.markdown(f"- {r}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Save to CSV
    record = {
        "age": age, "weight": weight, "gender": gender,
        "hb": hb, "well": feeling_well, "meds": meds,
        "travel": travel, "country": country, "region": region,
        "donation_date": str(donation_date), "tattoo": tattoo,
        "eligible": result_msg, "timestamp": str(datetime.now())
    }
    df = pd.DataFrame([record])
    df.to_csv("eligibility_records.csv", mode='a', header=not os.path.exists("eligibility_records.csv"), index=False)

    # PDF
    pdf = create_pdf(summary)
    st.markdown(get_pdf_download_link(pdf), unsafe_allow_html=True)
    if email:
        try:
            buffer = BytesIO(pdf.output(dest='S').encode('latin1'))
            send_email(email, "Your Blood Donation Eligibility Result", "Please find attached your PDF summary.", buffer)
            st.success("📧 PDF sent to your email!")
        except Exception as e:
            st.warning(f"Email failed: {e}")

# --- Dashboard ---
if os.path.exists("eligibility_records.csv"):
    st.subheader("📊 Dashboard")
    dashboard_df = pd.read_csv("eligibility_records.csv")
    col1, col2 = st.columns(2)
    col1.metric("Total Submissions", len(dashboard_df))
    col1.metric("Eligible", (dashboard_df["eligible"] == "Eligible").sum())
    col1.metric("Not Eligible", (dashboard_df["eligible"] == "Not Eligible").sum())
    with col2:
        fig = plt.figure()
        sns.histplot(dashboard_df["age"], bins=20, kde=True, color="salmon")
        plt.title("Age Distribution")
        st.pyplot(fig)
    st.dataframe(dashboard_df)
    st.markdown("</div>", unsafe_allow_html=True)
