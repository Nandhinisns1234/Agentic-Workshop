import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import os
from io import BytesIO

# === Configure Gemini API ===
# Set your Gemini API Key (replace with your actual API key)
GEMINI_API_KEY = "AIzaSyBRsrgvnw7ASL-Y_yb0GaOeBMlZ3u1q1FI"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel("gemini-2.0-flash")

# === Streamlit App ===
st.set_page_config(page_title="AI Email Generator", layout="centered")
st.title("📧 AI Email Generator with Gemini")
st.markdown("Generate professional emails using AI. Enter your message, select format and tone, then download it as a PDF.")

# === User Inputs ===
user_input = st.text_area("✏️ Input the content or purpose of your email:", height=150)

format_option = st.selectbox("📂 Choose the email format:", ["Formal", "Informal", "Business", "Apology", "Follow-up"])

tone_option = st.selectbox("🎯 Choose the tone:", ["Polite", "Friendly", "Direct", "Persuasive", "Grateful"])

# Session state to hold the response
if "generated_email" not in st.session_state:
    st.session_state["generated_email"] = ""

# === Function to generate email ===
def generate_email(text, email_format, tone):
    prompt = (
        f"Generate an {email_format.lower()} email with a {tone.lower()} tone based on the following input:\n"
        f"\"{text}\"\n"
        "Ensure it is well-structured and grammatically correct."
    )
    response = model.generate_content(prompt)
    return response.text

# === Generate Email Button ===
if st.button("🚀 Generate Email"):
    if user_input.strip() == "":
        st.warning("Please enter some input to generate an email.")
    else:
        st.session_state["generated_email"] = generate_email(user_input, format_option, tone_option)

# === Regenerate Button ===
if st.button("🔁 Regenerate with New Format/Tone"):
    if user_input.strip() == "":
        st.warning("Please enter some input before regenerating.")
    else:
        st.session_state["generated_email"] = generate_email(user_input, format_option, tone_option)

# === Display Generated Email ===
if st.session_state["generated_email"]:
    st.subheader("📬 Generated Email")
    st.text_area("Here is your email:", st.session_state["generated_email"], height=300)

    # === PDF Download ===
    def create_pdf(text):
     pdf = FPDF()
     pdf.add_page()
     pdf.set_font("Arial", size=12)
     for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
     pdf_output = pdf.output(dest='S').encode('latin1')  # Get PDF as string and encode it
     return BytesIO(pdf_output)

    pdf_buffer = create_pdf(st.session_state["generated_email"])
    st.download_button(
        label="📥 Download Email as PDF",
        data=pdf_buffer,
        file_name="generated_email.pdf",
        mime="application/pdf"
    )
