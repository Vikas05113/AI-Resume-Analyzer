import streamlit as st
import matplotlib.pyplot as plt
import time
import random
from wordcloud import WordCloud
from job_roles import job_roles
from resume_parser import extract_text
from skill_matcher import match_skills


# ---------- UI STYLE ----------
st.markdown("""
<style>

[data-testid="stSidebar"] {
background: linear-gradient(180deg,#1f4037,#99f2c8);
color:white;
}

.stApp {
background: linear-gradient(-45deg,#0f2027,#203a43,#2c5364,#00c6ff);
background-size: 400% 400%;
animation: gradient 12s ease infinite;
}

@keyframes gradient {
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

</style>
""", unsafe_allow_html=True)


# ---------- SESSION ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "otp" not in st.session_state:
    st.session_state.otp = None

if "otp_time" not in st.session_state:
    st.session_state.otp_time = None


# ---------- LOGIN ----------
def login():

    st.title("🔐 AI Career Platform Login")

    email = st.text_input("Enter Email")

    if st.button("Send OTP"):

        if email == "":
            st.warning("Please enter email")

        else:

            otp = random.randint(1000,9999)

            st.session_state.otp = otp
            st.session_state.otp_time = time.time()

            st.success(f"Demo OTP: {otp}")

    entered = st.text_input("Enter OTP")

    if st.button("Verify OTP"):

        if st.session_state.otp is None:
            st.warning("Generate OTP first")

        elif time.time() - st.session_state.otp_time > 120:
            st.error("OTP expired. Generate again")

        elif entered == str(st.session_state.otp):

            st.session_state.logged_in = True
            st.success("Login Successful")

        else:
            st.error("Invalid OTP")


# ---------- HOME ----------
def home_page():

    st.title("🚀 AI Career Platform")

    st.markdown("""
### Welcome 👋

This platform helps students and professionals:

- 📄 Analyze resumes  
- 📊 Check job match percentage  
- 🎓 Get career guidance  
- 💼 Discover job platforms  

Upload your resume and discover how well it matches your dream job.
""")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("AI Job Roles", "15+")

    with col2:
        st.metric("Resume Analysis", "Instant")

    with col3:
        st.metric("Career Domains", "4+")

    st.markdown("---")

    st.subheader("🔥 Popular Tech Career Domains")

    st.write("""
• Artificial Intelligence / Machine Learning  
• Web Development  
• Data Science  
• Cyber Security  
• Cloud Computing  
""")


# ---------- RESUME ANALYZER ----------
def resume_analyzer():

    # ---------- UI STYLE ----------
    st.markdown("""
    <style>

    .result-card{
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(10px);
        padding:20px;
        border-radius:12px;
        margin-bottom:20px;
        box-shadow:0 8px 20px rgba(0,0,0,0.3);
    }

    .skill-badge{
        background:linear-gradient(135deg,#00c6ff,#0072ff);
        color:white;
        padding:6px 12px;
        border-radius:8px;
        display:inline-block;
        margin:4px;
    }

    .missing-badge{
        background:linear-gradient(135deg,#ff5e62,#ff9966);
        color:white;
        padding:6px 12px;
        border-radius:8px;
        display:inline-block;
        margin:4px;
    }

    </style>
    """, unsafe_allow_html=True)


    st.title("📄 AI Resume Analyzer")
    st.markdown("Upload your resume and check how well it matches a job role.")


    role = st.selectbox("🎯 Select Job Role", list(job_roles.keys()))

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


    if uploaded_file:

        with st.spinner("🤖 AI analyzing resume..."):
            time.sleep(2)

        text = extract_text(uploaded_file)

        required_skills = job_roles[role]

        found, missing, score = match_skills(text, required_skills)


        # ---------- ATS SCORE ----------
        ats_score = min(100, score + 10)

        st.markdown("## 📊 Resume Analysis Result")

        col1,col2,col3 = st.columns(3)

        with col1:
            st.metric("Job Match %", f"{score:.1f}%")

        with col2:
            st.metric("ATS Score", f"{ats_score:.0f}%")

        with col3:
            st.metric("Skills Found", len(found))


        st.progress(int(score))


        st.markdown("---")


        col1,col2 = st.columns(2)


        # ---------- FOUND SKILLS ----------
        with col1:

            st.subheader("✅ Skills Found")

            for s in found:
                st.markdown(f'<span class="skill-badge">{s}</span>', unsafe_allow_html=True)


        # ---------- MISSING SKILLS ----------
        with col2:

            st.subheader("❌ Missing Skills")

            for m in missing:
                st.markdown(f'<span class="missing-badge">{m}</span>', unsafe_allow_html=True)


        # ---------- SUGGESTIONS ----------
        st.markdown("### 💡 Resume Improvement Suggestions")

        for m in missing:
            st.warning(f"Add **{m}** to improve ATS ranking")


        # ---------- WORD CLOUD ----------
        st.markdown("### ☁ Resume Keywords Visualization")

        wc = WordCloud(width=800,height=400,background_color="white").generate(text)

        fig,ax = plt.subplots()

        ax.imshow(wc)

        ax.axis("off")

        st.pyplot(fig)


        st.markdown("---")


        # ---------- ATS FRIENDLY CHECK ----------
        st.subheader("🤖 ATS Compatibility")

        if ats_score > 80:

            st.success("Your resume is ATS Friendly ✔")

        else:

            st.error("Your resume is NOT ATS optimized")


            st.info("""
Improve ATS score by:

• Adding more relevant skills  
• Using simple formatting  
• Including job keywords  
• Avoiding images/tables  
""")


        st.markdown("---")


   

# ---------- CAREER GUIDANCE ----------
def career_page():

    # ---------- Advanced UI ----------
    st.markdown("""
    <style>

    .career-card{
        background:rgba(255,255,255,0.08);
        backdrop-filter:blur(12px);
        padding:25px;
        border-radius:15px;
        box-shadow:0 10px 25px rgba(0,0,0,0.3);
        margin-bottom:20px;
    }

    .skill-badge{
        background:linear-gradient(135deg,#00c6ff,#0072ff);
        color:white;
        padding:6px 12px;
        border-radius:8px;
        display:inline-block;
        margin:4px;
        font-size:14px;
    }

    .role-badge{
        background:linear-gradient(135deg,#ff9966,#ff5e62);
        color:white;
        padding:6px 12px;
        border-radius:8px;
        display:inline-block;
        margin:4px;
        font-size:14px;
    }

    .salary-box{
        background:linear-gradient(135deg,#1f4037,#99f2c8);
        padding:25px;
        border-radius:12px;
        text-align:center;
        font-size:24px;
        color:white;
        margin-top:15px;
    }

    .learn-card{
        background:linear-gradient(135deg,#141E30,#243B55);
        padding:20px;
        border-radius:12px;
        color:white;
        margin-bottom:15px;
    }

    </style>
    """, unsafe_allow_html=True)


    st.title("🎓 Career Guidance Center")
    st.markdown("### 🚀 Explore Tech Career Paths")


    # ---------- Currency ----------
    currency = st.selectbox(
        "💱 View Salary In",
        ["USD ($)", "INR (₹)", "EUR (€)", "GBP (£)"]
    )

    conversion = {
        "USD ($)":1,
        "INR (₹)":83,
        "EUR (€)":0.92,
        "GBP (£)":0.78
    }

    symbol = currency.split(" ")[1].replace("(","").replace(")","")


    # ---------- Domain ----------
    domain = st.selectbox(
        "Choose Your Career Domain",
        [
        "AI / Machine Learning",
        "Data Science",
        "Web Development",
        "Cyber Security",
        "Cloud Computing",
        "DevOps Engineering",
        "Mobile App Development",
        "Blockchain Development",
        "Game Development",
        "UI/UX Design",
        "Software Engineering",
        "Database Engineering",
        "IoT Engineering",
        "AR/VR Development",
        "Robotics Engineering"
        ]
    )


    st.markdown("---")


    # ---------- Description ----------
    descriptions = {
    "AI / Machine Learning":"AI builds intelligent systems that learn from data and make predictions.",
    "Data Science":"Data science analyzes large datasets to discover patterns and insights.",
    "Web Development":"Web developers build modern websites and web applications.",
    "Cyber Security":"Cyber security protects systems and networks from cyber threats.",
    "Cloud Computing":"Cloud computing allows scalable infrastructure using AWS, Azure and GCP.",
    "DevOps Engineering":"DevOps automates development pipelines and improves deployment speed.",
    "Mobile App Development":"Mobile developers create Android and iOS applications.",
    "Blockchain Development":"Blockchain enables decentralized applications and smart contracts.",
    "Game Development":"Game developers create interactive digital games.",
    "UI/UX Design":"UI/UX designers focus on user-friendly digital experiences.",
    "Software Engineering":"Software engineers design and build large-scale applications.",
    "Database Engineering":"Database engineers design and manage data storage systems.",
    "IoT Engineering":"IoT connects smart devices and sensors.",
    "AR/VR Development":"AR/VR creates immersive digital environments.",
    "Robotics Engineering":"Robotics engineers build automated machines and robots."
    }


    skills = {
    "AI / Machine Learning":["Python","Machine Learning","Deep Learning","TensorFlow","PyTorch"],
    "Data Science":["Python","Pandas","SQL","Statistics","Data Visualization"],
    "Web Development":["HTML","CSS","JavaScript","React","Node.js"],
    "Cyber Security":["Network Security","Ethical Hacking","Linux","Cryptography"],
    "Cloud Computing":["AWS","Azure","Docker","Kubernetes"],
    "DevOps Engineering":["CI/CD","Docker","Kubernetes","Linux"],
    "Mobile App Development":["Flutter","Kotlin","Swift","React Native"],
    "Blockchain Development":["Solidity","Ethereum","Smart Contracts"],
    "Game Development":["Unity","C#","3D Graphics"],
    "UI/UX Design":["Figma","Adobe XD","User Research"],
    "Software Engineering":["Algorithms","Data Structures","System Design"],
    "Database Engineering":["SQL","Data Modeling","Database Optimization"],
    "IoT Engineering":["Arduino","Embedded Systems","Sensors"],
    "AR/VR Development":["Unity","3D Modeling","XR Interaction"],
    "Robotics Engineering":["ROS","Computer Vision","Control Systems"]
    }


    roles = {
    "AI / Machine Learning":["AI Engineer","ML Engineer","NLP Engineer"],
    "Data Science":["Data Scientist","Data Analyst"],
    "Web Development":["Frontend Developer","Backend Developer","Full Stack Developer"],
    "Cyber Security":["Security Analyst","Penetration Tester"],
    "Cloud Computing":["Cloud Engineer","Cloud Architect"],
    "DevOps Engineering":["DevOps Engineer","Automation Engineer"],
    "Mobile App Development":["Android Developer","Flutter Developer"],
    "Blockchain Development":["Blockchain Developer","Smart Contract Engineer"],
    "Game Development":["Game Developer","3D Artist"],
    "UI/UX Design":["UI Designer","UX Designer"],
    "Software Engineering":["Software Engineer","Systems Engineer"],
    "Database Engineering":["Database Engineer","DBA"],
    "IoT Engineering":["IoT Engineer","Embedded Engineer"],
    "AR/VR Development":["XR Developer","3D Designer"],
    "Robotics Engineering":["Robotics Engineer","Automation Engineer"]
    }


    salary = {
    "AI / Machine Learning":100000,
    "Data Science":95000,
    "Web Development":85000,
    "Cyber Security":105000,
    "Cloud Computing":110000,
    "DevOps Engineering":108000,
    "Mobile App Development":90000,
    "Blockchain Development":120000,
    "Game Development":80000,
    "UI/UX Design":75000,
    "Software Engineering":95000,
    "Database Engineering":88000,
    "IoT Engineering":92000,
    "AR/VR Development":98000,
    "Robotics Engineering":102000
    }


    converted_salary = salary[domain] * conversion[currency]


    col1,col2 = st.columns(2)


    # ---------- Description ----------
    with col1:

        st.markdown(f"""
        <div class="career-card">
        <h3>{domain}</h3>
        <p>{descriptions[domain]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🧠 Skills Required")

        for s in skills[domain]:
            st.markdown(f'<span class="skill-badge">{s}</span>', unsafe_allow_html=True)


    # ---------- Roles ----------
    with col2:

        st.subheader("💼 Career Roles")

        for r in roles[domain]:
            st.markdown(f'<span class="role-badge">{r}</span>', unsafe_allow_html=True)

        st.markdown("### 💰 Average Salary")

        st.markdown(
        f"""
        <div class="salary-box">
        {symbol}{int(converted_salary):,}
        </div>
        """,
        unsafe_allow_html=True
        )


    st.markdown("---")
    
    # ---------- Learning Resources ----------
    st.subheader("📚 If You Don't Know These Skills Yet")

    col1,col2,col3 = st.columns(3)

    with col1:

        st.markdown("""
        <div class="learn-card">
        <h4>🎥 YouTube</h4>
        Free tutorials for all technologies.
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Start Learning","https://youtube.com")


        st.markdown("""
        <div class="learn-card">
        <h4>📚 Coursera</h4>
        University level courses from top institutes.
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Explore Courses","https://coursera.org")


    with col2:

        st.markdown("""
        <div class="learn-card">
        <h4>💻 freeCodeCamp</h4>
        Best free coding courses.
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Learn Coding","https://freecodecamp.org")


        st.markdown("""
        <div class="learn-card">
        <h4>📊 Kaggle</h4>
        Practice ML and Data Science.
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Practice on Kaggle","https://kaggle.com")


    with col3:

        st.markdown("""
        <div class="learn-card">
        <h4>📘 W3Schools</h4>
        Beginner friendly tutorials.
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Start Tutorials","https://w3schools.com")


        st.markdown("""
        <div class="learn-card">
        <h4>🧠 GeeksforGeeks</h4>
        Best coding interview preparation platform.
        </div>
        """, unsafe_allow_html=True)

        st.link_button("Visit GFG","https://geeksforgeeks.org")


    st.markdown("---")


    st.subheader("📈 Career Roadmap")

    st.write("""
1️⃣ Learn programming fundamentals  
2️⃣ Master domain technologies  
3️⃣ Build real-world projects  
4️⃣ Contribute to open-source  
5️⃣ Apply for internships/jobs  
""")

    st.success("💡 Tip: Focus on building real projects and continuously improving your skills.")

    # ---------- Description ----------
    with col1:

        st.markdown(f"""
        <div class="career-card">
        <h3>📘 {domain}</h3>
        <p>{descriptions[domain]}</p>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🧠 Skills Required")

        for s in skills[domain]:
            st.markdown(f'<span class="skill-badge">{s}</span>', unsafe_allow_html=True)


    # ---------- Roles ----------
    with col2:

        st.subheader("💼 Career Roles")

        for r in roles[domain]:
            st.markdown(f'<span class="role-badge">{r}</span>', unsafe_allow_html=True)

        st.markdown("### 💰 Average Salary")

        st.markdown(
        f"""
        <div class="salary-box">
        {symbol}{int(converted_salary):,}
        </div>
        """,
        unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("📈 Career Roadmap")

    st.write("""
1️⃣ Learn programming fundamentals  
2️⃣ Master the key technologies in the domain  
3️⃣ Build real-world projects  
4️⃣ Contribute to open-source projects  
5️⃣ Apply for internships and entry-level jobs  
""")

    st.success("💡 Tip: Building real projects and gaining practical experience is the fastest way to grow in tech careers.")


# ---------- JOB PLATFORMS ----------
def jobs_page():

    st.title("💼 Where to Apply for Jobs")

    st.markdown("### 🚀 Top Job Platforms for Tech Careers")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        #### 🔵 LinkedIn Jobs
        The most popular professional network where companies post millions of jobs.
        Perfect for networking and applying directly to recruiters.
        """)
        st.link_button("Apply on LinkedIn", "https://www.linkedin.com/jobs")

        st.markdown("---")

        st.markdown("""
        #### 🟢 Indeed
        A global job search engine that aggregates jobs from thousands of websites.
        Great for entry-level and experienced roles.
        """)
        st.link_button("Search Jobs on Indeed", "https://www.indeed.com")

        st.markdown("---")

        st.markdown("""
        #### 🟣 Glassdoor
        Find jobs along with company reviews, salaries, and interview experiences.
        """)
        st.link_button("Explore Glassdoor Jobs", "https://www.glassdoor.com")

    with col2:

        st.markdown("""
        #### 🟡 Naukri
        One of India's largest job portals with thousands of IT and tech job listings.
        """)
        st.link_button("Find Jobs on Naukri", "https://www.naukri.com")

        st.markdown("---")

        st.markdown("""
        #### 🚀 AngelList (Wellfound)
        Best platform for startup jobs and remote tech opportunities.
        """)
        st.link_button("Startup Jobs on AngelList", "https://angel.co/jobs")

        st.markdown("---")

        st.info("💡 Tip: Always keep your resume updated and apply to multiple platforms.")

    st.markdown("---")

    st.success("🎯 Pro Tip: Apply to at least **5–10 jobs daily** to increase your chances of getting interviews.")

# ---------- APP ----------
if not st.session_state.logged_in:

    login()

else:

    # ---------- Sidebar Style ----------
    st.markdown("""
    <style>

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg,#141E30,#243B55);
        color:white;
    }

    .nav-button{
        width:100%;
        padding:10px;
        border-radius:8px;
        background:linear-gradient(135deg,#00c6ff,#0072ff);
        color:white;
        text-align:center;
        font-weight:bold;
        margin-bottom:10px;
    }

    </style>
    """, unsafe_allow_html=True)


    st.sidebar.title("🚀 AI Career Platform")

    st.sidebar.markdown("### Navigation")

    # ---------- Navigation Buttons ----------
    if st.sidebar.button("🏠 Home           "):
        st.session_state.page = "Home"

    if st.sidebar.button("📄 Resume Analyze "):
        st.session_state.page = "Resume Analyzer"

    if st.sidebar.button("🎓 Career Guidance"):
        st.session_state.page = "Career Guidance"

    if st.sidebar.button("💼 Job Platforms  "):
        st.session_state.page = "Job Platforms"
    
    if st.sidebar.button(" AI Resume Builder "):
        st.session_state.page = "AI Resume Builder"


    # ---------- Default Page ----------
    if "page" not in st.session_state:
        st.session_state.page = "Home"


    # ---------- Page Routing ----------
    if st.session_state.page == "Home":
        home_page()

    elif st.session_state.page == "Resume Analyzer":
        resume_analyzer()

    elif st.session_state.page == "Career Guidance":
        career_page()

    elif st.session_state.page == "Job Platforms":
        jobs_page()
    


    # ---------- Footer ----------
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👨‍💻 Developer")
    st.sidebar.write("Vikas Barigidad")
    st.sidebar.write("AI & ML Enthusiast 🚀")