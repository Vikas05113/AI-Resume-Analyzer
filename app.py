import streamlit as st

# Page settings
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

# Title
st.title("📄 AI Resume Analyzer")
st.markdown("### Improve your resume based on the job role you are applying for")

st.write("---")

# Sidebar
st.sidebar.header("About")
st.sidebar.info(
    "This AI Resume Analyzer checks your resume and compares it with required skills for a job role."
)

# Job role selection
st.subheader("1️⃣ Select Job Role")

role = st.selectbox(
    "Choose the job role you are applying for",
    ["Data Scientist", "Machine Learning Engineer", "Web Developer", "Cyber Security Analyst"]
)

st.write("---")

# Resume upload
st.subheader("2️⃣ Upload Your Resume")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

st.write("---")

# Analyze button
if st.button("Analyze Resume 🚀"):

    if uploaded_file is None:
        st.warning("⚠️ Please upload your resume first.")
    else:
        st.success("✅ Resume uploaded successfully!")

        # Example result
        st.subheader("📊 Resume Analysis Result")

        st.progress(70)

        st.write("### Skills Found")
        st.success("✔ Python")
        st.success("✔ Machine Learning")
        st.success("✔ SQL")

        st.write("### Missing Skills")
        st.error("❌ Deep Learning")
        st.error("❌ Docker")
        st.error("❌ Kubernetes")

        st.info("💡 Tip: Add the missing skills to improve your resume score.")