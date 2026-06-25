import streamlit as st
from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
import io
import os


# -----------------------------
# CONFIG
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="AI Requirements Assistant", layout="wide")

st.title("AI Requirements Engineering Assistant")
st.caption("Consulting-grade AI tool for generating and evaluating software requirements")

# -----------------------------
# INPUTS
# -----------------------------
industry = st.selectbox(
    "Select Industry",
    ["General", "Banking", "Healthcare", "Retail", "Government"]
)

requirement = st.text_area("Enter Business Requirement")

generate = st.button("Generate Analysis")

# -----------------------------
# AI FUNCTION
# -----------------------------
def generate_requirements(text, industry):

    system_prompt = f"""
You are a Senior Business Analyst working in a top consulting firm.

Industry: {industry}

Convert business requirements into structured consulting-grade documentation.

Generate:

1. User Story (Agile format)
2. Acceptance Criteria (detailed)
3. Functional Requirements
4. Test Cases (positive + negative)
5. Edge Cases
6. Risks & Assumptions
7. Dependencies
8. AI / Automation Opportunities
9. Requirement Quality Score Section:
   - Clarity Score (1-10)
   - Risk Score (1-10)
   - Completeness Score (1-10)
   - Key Issues
   - Recommendations

Rules:
- Be structured and professional
- Tailor to industry context
- Think like a consultant
- Be concise but complete
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]
    )

    return response.choices[0].message.content

# -----------------------------
# PDF GENERATOR
# -----------------------------
def create_pdf(text, industry, requirement):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Requirements Engineering Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(f"<b>Industry:</b> {industry}", styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>Business Requirement:</b>", styles["Heading2"]))
    content.append(Paragraph(requirement, styles["Normal"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("<b>AI Analysis:</b>", styles["Heading2"]))
    content.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))

    doc.build(content)

    buffer.seek(0)
    return buffer

# -----------------------------
# OUTPUT UI
# -----------------------------
if generate:
    if requirement.strip() == "":
        st.warning("Please enter a business requirement first")
    else:
        with st.spinner("Generating consulting-grade analysis..."):
            output = generate_requirements(requirement, industry)

        st.success("Analysis Complete")

        st.markdown(output)

        st.divider()

        st.subheader("📊 Requirement Quality Dashboard")
        st.info("AI evaluates clarity, risk, and completeness of the requirement.")

        # -----------------------------
        # PDF DOWNLOAD
        # -----------------------------
        pdf_buffer = create_pdf(output, industry, requirement)

        st.download_button(
            label="📄 Download Consulting Report (PDF)",
            data=pdf_buffer,
            file_name="AI_Requirements_Report.pdf",
            mime="application/pdf"
        )
