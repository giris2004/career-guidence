import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
import PyPDF2
import io
import base64

# --------------------------
# CONFIGURATION
# --------------------------
GOOGLE_API_KEY = "AIzaSyBtZCzwHfujo3yevV5yc7GO8bLM1-Q7MFA"
genai.configure(api_key=GOOGLE_API_KEY)
model_name = "models/gemini-1.5-flash-latest"

recognizer = sr.Recognizer()


# --------------------------
# FUNCTION DEFINITIONS
# --------------------------

def get_ai_response(prompt):
    model = genai.GenerativeModel(model_name)
    contents = [{"role": "user", "parts": [{"text": prompt}]}]
    response = model.generate_content(contents=contents)
    return response.text


def analyze_resume(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def get_resume_feedback(resume_text, target_job):
    prompt = (
        f"You are a professional career coach and resume expert.\n"
        f"Review the following resume:\n\n"
        f"{resume_text}\n\n"
        f"Provide detailed feedback on its structure, grammar, ATS compatibility, and how it fits for the job role: {target_job}.\n"
        f"Suggest improvements and missing skills."
    )
    return get_ai_response(prompt)


def recommend_learning_path(skills_gap):
    prompt = (
        f"You are an AI career advisor.\n"
        f"Based on the following missing skills: {skills_gap}, recommend a personalized learning path.\n"
        f"Include courses, certifications, and project ideas."
    )
    return get_ai_response(prompt)


def get_voice_input():
    with sr.Microphone() as source:
        st.info("🎤 Listening... Speak now!")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("❗ Could not understand your speech.")
            return None
        except sr.RequestError:
            st.error("❗ Could not access the recognition service.")
            return None


# --------------------------
# STREAMLIT UI
# --------------------------

st.set_page_config(page_title="AI Career Counselor & Resume Analyzer", layout="centered")

st.title("💼 AI-Powered Career Counselor & Resume Analyzer")

# TABS for Each Feature
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Career Guidance Chatbot",
    "Resume Analyzer",
    "Learning Path Recommendations",
    "Mock Interview (Q&A)",
    "Job Market Insights"
])

# ----------------------------------------
# TAB 1: Career Guidance Chatbot
# ----------------------------------------
with tab1:
    st.header("🔮 Personalized Career Guidance")

    user_name = st.text_input("Enter your name:")
    user_background = st.text_area("Describe your background, skills, and interests:")

    if st.button("Suggest Career Paths"):
        if user_background:
            prompt = (
                f"You are an AI Career Counselor for {user_name}.\n"
                f"Based on their background and interests:\n"
                f"{user_background}\n\n"
                f"Suggest 3-5 suitable career paths with explanations. Include industry demand, salaries, and growth potential."
            )
            response = get_ai_response(prompt)
            st.subheader("🔑 Recommended Career Paths:")
            st.write(response)
        else:
            st.warning("Please enter your background information.")

# ----------------------------------------
# TAB 2: Resume Analyzer
# ----------------------------------------
with tab2:
    st.header("📄 Resume Analyzer & Suggestions")

    uploaded_resume = st.file_uploader("Upload your resume (PDF only):", type=["pdf"])
    target_job = st.text_input("Target Job Role (e.g., Data Scientist, Software Engineer)")

    if uploaded_resume and st.button("Analyze Resume"):
        resume_text = analyze_resume(uploaded_resume)
        if resume_text:
            feedback = get_resume_feedback(resume_text, target_job)
            st.subheader("✅ Resume Feedback:")
            st.write(feedback)
        else:
            st.error("❗ Could not extract text from the uploaded PDF.")

# ----------------------------------------
# TAB 3: Personalized Learning Path
# ----------------------------------------
with tab3:
    st.header("📚 Personalized Learning Path & Skill Recommendations")

    skills_gap = st.text_area("List your missing skills or areas you'd like to improve:")

    if st.button("Get Learning Path"):
        if skills_gap:
            learning_plan = recommend_learning_path(skills_gap)
            st.subheader("🚀 Recommended Learning Path:")
            st.write(learning_plan)
        else:
            st.warning("Please enter your missing skills.")

# ----------------------------------------
# TAB 4: Mock Interview (Q&A)
# ----------------------------------------
with tab4:
    st.header("🗣 AI-Powered Mock Interview")

    role = st.selectbox("Select Interview Role:",
                        ["Software Engineer", "Data Scientist", "Product Manager", "Marketing Specialist"])

    if st.button("🎤 Start Mock Interview (Speak Your Answer)"):
        question_prompt = (
            f"You are an interviewer for the role of {role}.\n"
            f"Ask one technical and one behavioral question to the candidate."
        )
        question = get_ai_response(question_prompt)
        st.info(f"❓ {question}")

        answer = get_voice_input()
        if answer:
            feedback_prompt = (
                f"As an interviewer for {role}, evaluate the following answer:\n\n"
                f"{answer}\n\n"
                f"Provide feedback on communication, technical knowledge, and confidence."
            )
            feedback = get_ai_response(feedback_prompt)
            st.subheader("✅ Interview Feedback:")
            st.write(feedback)

# ----------------------------------------
# TAB 5: Job Market Insights (Static Demo)
# ----------------------------------------
with tab5:
    st.header("📈 Real-Time Job Market Insights (Demo Data)")

    trending_roles = [
        "AI/ML Engineer",
        "Cybersecurity Specialist",
        "Data Analyst",
        "Product Manager",
        "Full-Stack Developer"
    ]
    st.subheader("🔥 Trending Job Roles:")
    st.write("\n".join([f"✅ {role}" for role in trending_roles]))

    st.subheader("📊 Salary Insights (INR):")
    salary_data = {
        "AI/ML Engineer": "₹10-30 LPA",
        "Cybersecurity Specialist": "₹8-20 LPA",
        "Data Analyst": "₹6-15 LPA",
        "Product Manager": "₹15-35 LPA",
        "Full-Stack Developer": "₹8-18 LPA"
    }

    for role, salary in salary_data.items():
        st.write(f"{role}:** {salary}")

# --------------------------
# END OF APP
# --------------------------
