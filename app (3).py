# BloodReady | Final App with Full Functionality + PDF + Email + Logging
import streamlit as st
from datetime import datetime
import base64
from io import BytesIO
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import pandas as pd

st.set_page_config(
    page_title="BloodReady | Blood Donation Eligibility",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PDF Export Function ---
def create_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', '', '/usr/share/fonts/truetype/noto/NotoSansKR-Regular.otf', uni=True)
    pdf.set_font('ArialUnicode', '', 12)
    for line in summary_text.split('\n'):
        pdf.cell(200, 10, txt=line, ln=True)
    return pdf

def get_pdf_download_link(pdf):
    buffer = BytesIO()
    pdf.output(buffer)
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="blood_eligibility_summary.pdf">📄 Download PDF Result</a>'
    return href

# --- Email Sending ---
def send_email(to_email, subject, body, pdf_bytes):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = to_email
    msg.set_content(body)
    msg.add_attachment(pdf_bytes.getvalue(), maintype='application', subtype='pdf', filename='blood_eligibility_summary.pdf')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@example.com', 'your_password')
        smtp.send_message(msg)

# --- Sidebar ---
with st.sidebar:
    st.image("https://blood-health-chatbot.streamlit.app/files/file-SnFRkJPAD4wgV45VizmH6z", use_column_width=True)
    st.markdown("## 🧾 Blood Donation Summary")
    st.write("Fill out the form to determine your blood donation eligibility according to the Korean Red Cross.")
    st.markdown("---")
    st.markdown("This tool is designed to help you pre-check your eligibility before visiting a donation center.")
    st.markdown("이 도구는 헌혈의 집을 방문하기 전, 본인이 자격 조건을 충족하는지 사전에 확인할 수 있도록 돕기 위해 제작되었습니다.")
    st.markdown("**Made by Ahyoung Bella Kim, Co-Chair of ABO Supporters**")

# --- Styling ---
st.markdown("""<style>
html, body, [class*='css'] {
    font-family: 'Helvetica Neue', sans-serif;
    background: linear-gradient(135deg, #fff5f7, #fefefe);
    color: #111827;
}
.title-area {
    text-align: center;
    padding-top: 1rem;
    margin-bottom: 2rem;
}
.title-area img {
    width: 130px;
    animation: fadeIn 1s ease-in-out;
}
.title-area h1 {
    font-size: 2.8em;
    margin-bottom: 0.2em;
    font-weight: 800;
    color: #d62828;
}
.title-area p {
    color: #e63946;
    font-weight: 500;
    font-size: 1.2em;
    margin-top: 0.2em;
}
.section {
    background-color: white;
    padding: 2.5rem;
    margin: 2.5rem auto;
    border-radius: 20px;
    border: 2px solid #f3c5c5;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    transition: transform 0.2s;
}
.section:hover {
    transform: translateY(-2px);
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
    transition: 0.3s ease;
}
.photo-grid img:hover {
    transform: scale(1.02);
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Remove floating animation if any */
[class*='floating'] {
    animation: none !important;
    transform: none !important;
}
    to { opacity: 1; transform: translateY(0); }
}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class='title-area'>
<img src='https://blood-health-chatbot.streamlit.app/files/file-SnFRkJPAD4wgV45VizmH6z' alt='mascot'>
<h1>BloodReady | 헌혈 자격 셀프 체크</h1>
<p>당신의 따뜻함이 생명이 됩니다. <br> Your Warmth Can Save a Life.</p>
</div>""", unsafe_allow_html=True)

# --- Form ---
# Based on additional Korean Red Cross questions
st.markdown("<div class='section'>", unsafe_allow_html=True)
language = st.radio("🌐 Select Language / 언어 선택", ["English", "한국어"])
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🩸 Fill in your details")
gender = st.radio("Gender", ["Female", "Male", "Other"])
if gender == "Female":
    menstruating = st.radio("Are you currently on your period?", ["Yes", "No", "Prefer not to say"])
    pregnancy = st.radio("Are you pregnant or recently gave birth?", ["Yes", "No"])
donation_date = st.date_input("Last blood donation date", value=datetime.today())
tattoo = st.radio("Any tattoos or piercings in the last year?", ["Yes", "No"])
age = st.slider("Age", 10, 100, 20)
weight = st.slider("Weight (kg)", 30, 150, 60)
feeling_well = st.radio("Are you feeling well today?", ["Yes", "No"])
hb = st.slider("Hemoglobin (Hb) Level (g/dL)", 5.0, 20.0, 13.0, step=0.1)
meds = st.radio("Currently taking any medication?", ["Yes", "No"])
travel = st.radio("Have you traveled abroad recently?", ["Yes", "No"])
email = st.text_input("Enter your email (optional, for PDF)")
malaria_risk = False
country, region = "", ""
if travel == "Yes":
    country = st.text_input("Which country did you visit?")
    region = st.text_input("Which region in that country?")
    malaria_data = {"India": ["Odisha", "Assam", "Jharkhand"], "Philippines": ["Palawan", "Mindanao"], "Indonesia": ["Papua", "Kalimantan"]}
    if country in malaria_data:
        if any(r.lower() in region.lower() for r in malaria_data[country]):
            malaria_risk = True

if st.button("Check Eligibility"):
    try:
        days_since = (datetime.today() - donation_date).days
    except:
        days_since = 9999
    eligible = True
    reasons = []
    if age < 16: eligible, reasons = False, reasons + ["Must be 16 or older"]
    if weight < 50: eligible, reasons = False, reasons + ["Must weigh at least 50kg"]
    if feeling_well == "No": eligible, reasons = False, reasons + ["Not feeling well today"]
    if hb < 12.5: eligible, reasons = False, reasons + ["Hemoglobin too low"]
    if meds == "Yes": eligible, reasons = False, reasons + ["Currently taking medication"]
    if malaria_risk: eligible, reasons = False, reasons + ["Visited malaria-risk region"]
    if gender == "Female":
        if menstruating == "Yes": reasons = reasons + ["Currently menstruating"]
        if pregnancy == "Yes": eligible, reasons = False, reasons + ["Pregnant or recently gave birth"]
    if days_since < 56: eligible, reasons = False, reasons + ["Donated within the last 8 weeks"]
    if tattoo == "Yes": eligible, reasons = False, reasons + ["Recent tattoo or piercing"]

    summary = f"Age: {age}\nWeight: {weight}kg\nFeeling Well: {feeling_well}\nHb Level: {hb}\nMedication: {meds}\nTravel: {travel}\nCountry: {country}\nRegion: {region}\n"
    result_msg = "Eligible" if eligible else "Not Eligible"
    summary += f"Result: {result_msg}\n"
    if not eligible:
        summary += "Reasons:\n" + "\n".join(f"- {r}" for r in reasons)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("Eligibility Result")
    if eligible:
        st.success("✅ You are eligible to donate blood!")
    else:
        st.error("❌ You are not eligible to donate blood at this time.")
        for r in reasons:
            st.markdown(f"- {r}")
    st.markdown("</div>", unsafe_allow_html=True)

    # Save to CSV
    record = {"age": age, "weight": weight, "gender": gender, "hb": hb, "well": feeling_well, "meds": meds, "travel": travel, "country": country, "region": region, "donation_date": str(donation_date), "tattoo": tattoo, "eligible": result_msg, "timestamp": str(datetime.now())}
    df = pd.DataFrame([record])
    try:
        df.to_csv("eligibility_records.csv", mode='a', header=False, index=False)
    except:
        df.to_csv("eligibility_records.csv", mode='w', header=True, index=False)

    # PDF + Email
    pdf = create_pdf(summary)
    st.markdown(get_pdf_download_link(pdf), unsafe_allow_html=True)
    if email:
        try:
            buffer = BytesIO()
            pdf.output(buffer)
            send_email(email, "Your Blood Donation Eligibility Result", "Please find attached your PDF summary.", buffer)
            st.success("📧 Result sent to your email!")
        except Exception as e:
            st.warning(f"Email failed: {e}")

# --- Gallery ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📸 헌혈 행사 스냅 | Snapshots from Blood Donation Event")
st.markdown("""<div class='photo-grid'>
<img src='https://blood-health-chatbot.streamlit.app/files/file-FzUtSQno4mRzY3VTvPSah6' alt='헌혈 캠페인 1'>
<img src='https://blood-health-chatbot.streamlit.app/files/file-DwgfFk9VY7Azh1Aqcdahev' alt='헌혈 캠페인 2'>
<img src='https://blood-health-chatbot.streamlit.app/files/file-Y2SssVJR6RnF1bPMRv6BMZ' alt='헌혈 캠페인 3'>
</div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# --- Dashboard Section ---
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📊 Blood Donation Eligibility Dashboard")

import os
if os.path.exists("eligibility_records.csv"):
    df = pd.read_csv("eligibility_records.csv")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Records", len(df))
        st.metric("Eligible", (df["eligible"] == "Eligible").sum())
        st.metric("Not Eligible", (df["eligible"] == "Not Eligible").sum())
    with col2:
        fig1 = plt.figure()
        sns.histplot(df["age"], bins=20, kde=True, color="salmon")
        plt.title("Age Distribution")
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        fig2 = plt.figure()
        sns.countplot(data=df, x="gender", palette="pastel")
        plt.title("Gender Distribution")
        st.pyplot(fig2)

    with col4:
        fig3 = plt.figure()
        sns.countplot(data=df, x="eligible", palette="coolwarm")
        plt.title("Eligibility Status")
        st.pyplot(fig3)

    st.subheader("📋 Raw Submission Records")
    st.dataframe(df)
else:
    st.info("No records yet. Please complete the form to generate data.")
st.markdown("</div>", unsafe_allow_html=True)

