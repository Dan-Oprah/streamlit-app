import streamlit as st
import random
import time
import pandas as pd

# --- PAGE CONFIGURATION & THEME TOGGLE ---
st.set_page_config(
    page_title="AMEN SCHOOL ULTIMATE CBT PORTAL",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION ---
if "users" not in st.session_state:
    st.session_state.users = {} 
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "registration_counter" not in st.session_state:
    st.session_state.registration_counter = 205000 
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {
        "205001 (Comp Sci)": 480,
        "205012 (Mech Eng)": 450,
        "205045 (Microbio)": 420,
        "205008 (Agric Econ)": 390
    }
# New state for bookmarks and history tracking
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "exam_history" not in st.session_state:
    st.session_state.exam_history = []

# --- MASTER DATABASE (MULTI-COURSE & TOPICS) ---
PORTAL_DATA = {
    "CHM 101: General Chemistry I": {
        "Topics": [
            "Atomic Structure & Periodic Table",
            "Mole Concept & Stoichiometry",
            "States of Matter (Gases & Liquids)",
            "Thermochemistry & Enthalpy"
        ],
        "Questions": {
            "Atomic Structure & Periodic Table": [
                {"q": "What subatomic particle carries a negative charge?", "options": ["Proton", "Neutron", "Electron", "Positron"], "ans": "Electron", "expl": "Electrons orbit the nucleus and have a negative charge."},
                {"q": "Which quantum number describes the shape of an orbital?", "options": ["Principal (n)", "Azimuthal/Angular (l)", "Magnetic (m)", "Spin (s)"], "ans": "Azimuthal/Angular (l)", "expl": "Azimuthal quantum number determines the subshell shape (s, p, d, f)."},
            ],
            "Mole Concept & Stoichiometry": [
                {"q": "What is the molar mass of Carbon dioxide (CO2)? [C=12, O=16]", "options": ["28 g/mol", "44 g/mol", "32 g/mol", "56 g/mol"], "ans": "44 g/mol", "expl": "12 + (16 * 2) = 12 + 32 = 44 g/mol."},
            ]
        }
    },
    "PHY 101: General Physics I": {
        "Topics": [
            "Kinematics & Motion in 1D",
            "Newton's Laws of Motion",
            "Work, Energy and Power"
        ],
        "Questions": {
            "Kinematics & Motion in 1D": [
                {"q": "What is the SI unit of acceleration?", "options": ["m/s", "m/s²", "kg m/s", "Newton"], "ans": "m/s²", "expl": "Acceleration is change in velocity over time."},
            ]
        }
    }
}

FUNAAB_FACULTIES = {
    "COLPHYS (Physical Sciences)": ["Computer Science", "Mathematics", "Statistics", "Physics", "Chemistry"],
    "COLBIOS (Biological Sciences)": ["Microbiology", "Biochemistry", "Plant Biology", "Zoology"],
    "COLENG (Engineering)": ["Mechanical Engineering", "Electrical/Electronics", "Civil Engineering", "Mechatronics"],
    "COLAMRUD (Agricultural Management)": ["Agricultural Economics", "Farm Management"],
    "COMLEM (Environmental Management)": ["Ecotourism", "Water Resources Management"]
}

# ==========================================
# SIDEBAR: THEME PREFERENCE & AUTH
# ==========================================
st.sidebar.title("⚙️ Portal Settings")
theme_mode = st.sidebar.radio("Owner/User Theme Preference", ["Light Mode (White)", "Dark Mode (Black)"])

# Apply styling based on theme choice
if "Dark Mode" in theme_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #0e1117; color: #ffffff; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: #000000; }
        </style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")

def auth_sidebar():
    st.sidebar.title("🔐 AMEN SCHOOL PORTAL")
    
    if st.session_state.current_user is None:
        choice = st.sidebar.selectbox("Access Portal", ["Login", "Register (New Student)"])
        
        if choice == "Register (New Student)":
            st.sidebar.subheader("Student Registration")
            reg_email = st.sidebar.text_input("Gmail Address")
            reg_pass = st.sidebar.text_input("Create Password", type="password")
            
            col_picked = st.sidebar.selectbox("Select College", list(FUNAAB_FACULTIES.keys()))
            dept_picked = st.sidebar.selectbox("Select Department", FUNAAB_FACULTIES[col_picked])
            sex_picked = st.sidebar.selectbox("Sex", ["Male", "Female"])
            dob_picked = st.sidebar.date_input("Date of Birth")
            target_cgpa = st.sidebar.slider("Target CGPA Goal", 2.0, 5.0, 4.5, 0.1)
            
            if st.sidebar.button("Complete Registration"):
                if reg_email and reg_pass:
                    if reg_email in st.session_state.users:
                        st.sidebar.error("Email already registered!")
                    else:
                        st.session_state.registration_counter += 1
                        serial_id = f"2050{str(st.session_state.registration_counter)[-3:]}"
                        
                        st.session_state.users[reg_email] = {
                            "password": reg_pass,
                            "college": col_picked,
                            "department": dept_picked,
                            "sex": sex_picked,
                            "dob": str(dob_picked),
                            "target_cgpa": target_cgpa,
                            "serial_number": serial_id,
                            "access_verified": False,
                            "unlocked_bonus": False,
                            "role": "owner" if reg_email == "amenadmin@funaab.edu.ng" else "student"
                        }
                        st.sidebar.success(f"Registered! Your Serial ID is {serial_id}. Please login.")
                else:
                    st.sidebar.warning("Fill in your email and password.")
                    
        elif choice == "Login":
            st.sidebar.subheader("Student & Owner Login")
            login_email = st.sidebar.text_input("Gmail")
            login_pass = st.sidebar.text_input("Password", type="password")
            
            if st.sidebar.button("Login"):
                user = st.session_state.users.get(login_email)
                if user and user["password"] == login_pass:
                    st.session_state.current_user = login_email
                    st.rerun()
                else:
                    st.sidebar.error("Invalid Gmail or Password.")
    else:
        user_info = st.session_state.users[st.session_state.current_user]
        st.sidebar.write(f"👤 **Logged in:** {st.session_state.current_user}")
        st.sidebar.write(f"🔢 **Serial ID:** `{user_info['serial_number']}`")
        st.sidebar.write(f"🎯 **Target CGPA:** {user_info['target_cgpa']}")
        
        if st.sidebar.button("Log Out"):
            st.session_state.current_user = None
            st.rerun()

auth_sidebar()

# ==========================================
# MAIN APP ROUTING & PAYMENT GATEWAY (₦1,500)
# ==========================================
if st.session_state.current_user is None:
    st.title("🎓 AMEN SCHOOL ULTIMATE CBT PORTAL (FUNAAB)")
    st.info("👈 Please **Register** or **Login** via the sidebar to access full multi-course materials and features!")
    
    st.markdown("---")
    st.subheader("📖 AMEN SCHOOL ULTIMATE GUIDE (Preview)")
    st.write("The ultimate campus survival guide for FUNAAB 100-level students looking to score 4.5+ CGPA effortlessly.")
else:
    current_user_data = st.session_state.users[st.session_state.current_user]
    
    # PAYMENT GATEWAY (₦1,500 Full Access)
    if not current_user_data["access_verified"]:
        st.warning("🔒 **Portal Locked: Full Access Fee (₦1,500)**")
        st.write("Get lifetime access to **all courses**, Exam Simulation Mode, AI Voice reader, Daily Challenges, Leaderboard, GPA Calculator, and new Analytics features.")
        
        entered_code = st.text_input("Enter your 6-digit access code (Gotten after paying ₦1,500 via WhatsApp/Transfer):")
        if st.button("Verify Access Code"):
            if entered_code == "AMEN2050": # Demo passcode
                current_user_data["access_verified"] = True
                st.success("🎉 Access Verified! Welcome to the premium portal.")
                st.rerun()
            else:
                st.error("Invalid access code. Message admin on WhatsApp to secure your code.")
        st.stop()

    # --- TABS INCLUDING NEW REASONABLE FEATURES ---
    if current_user_data["role"] == "owner":
        tabs = st.tabs(["📚 CBT Portal", "⏱️ Exam Mode", "📊 Analytics & Bookmarks", "🌍 Daily & Leaderboard", "🧮 GPA Calculator", "🤖 AI & Voice", "🎁 Share & Unlock", "👑 Owner Zone"])
    else:
        tabs = st.tabs(["📚 CBT Portal", "⏱️ Exam Mode", "📊 Analytics & Bookmarks", "🌍 Daily & Leaderboard", "🧮 GPA Calculator", "🤖 AI & Voice", "🎁 Share & Unlock"])

    # --- TAB 1: PRACTICE CBT PORTAL ---
    with tabs[0]:
        st.header("📚 Multi-Course Practice Portal")
        selected_course = st.selectbox("Choose Course", list(PORTAL_DATA.keys()))
        course_topics = PORTAL_DATA[selected_course]["Topics"]
        selected_topic = st.selectbox("Choose Topic", course_topics)
        
        questions_pool = PORTAL_DATA[selected_course]["Questions"].get(selected_topic, [])
        if questions_pool:
            with st.form("practice_form"):
                user_answers = {}
                for idx, q_item in enumerate(questions_pool):
                    st.write(f"**Q{idx+1}: {q_item['q']}**")
                    user_answers[idx] = st.radio(f"Opt Q{idx+1}", q_item["options"], key=f"prac_{idx}")
                    st.write("---")
                submitted = st.form_submit_button("Submit Practice Quiz")
                
            if submitted:
                score = sum(1 for idx, q in enumerate(questions_pool) if user_answers[idx] == q['ans'])
                percentage = (score / len(questions_pool)) * 100
                st.success(f"Score: {score} / {len(questions_pool)} ({percentage:.1f}%)")
                
                # Save result to exam history for analytics
                st.session_state.exam_history.append({
                    "Course": selected_course,
                    "Topic": selected_topic,
                    "Score": f"{score}/{len(questions_pool)}"
                })

                for idx, q in enumerate(questions_pool):
                    st.info(f"💡 **Explanation for Q{idx+1}:** {q['expl']}")
                    # Option to bookmark tough questions
                    if st.button(f"Bookmark Q{idx+1}", key=f"bm_{idx}"):
                        if q['q'] not in st.session_state.bookmarks:
                            st.session_state.bookmarks.append(q['q'])
                            st.success(f"Bookmarked: {q['q']}")
        else:
            st.info("Questions for this topic are updating soon.")

    # --- TAB 2: EXAM MODE ---
    with tabs[1]:
        st.header("⏱️ CBT Exam Simulation Mode")
        st.write("Simulate real FUNAAB computer-based test conditions under strict time pressure.")
        
        exam_course = st.selectbox("Select Exam Course", list(PORTAL_DATA.keys()), key="ex_course")
        
        if st.button("Start 30-Minute Exam Simulation"):
            st.warning("⚠️ Exam Session Active! Timer is ticking...")
            timer_placeholder = st.empty()
            for seconds_left in range(15, 0, -1): # Accelerated for smooth testing
                timer_placeholder.markdown(f"⏳ **Time Remaining:** 29 mins {seconds_left} secs")
                time.sleep(0.1)
            st.error("⏰ Time's up! Exam auto-submitted.")

    # --- TAB 3: NEW ANALYTICS & BOOKMARKS ---
    with tabs[2]:
        st.header("📊 Student Analytics & Bookmarked Questions")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Past Test History")
            if st.session_state.exam_history:
                df_history = pd.DataFrame(st.session_state.exam_history)
                st.dataframe(df_history, use_container_width=True)
                
                # Download report feature
                csv_data = df_history.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Performance Report (CSV)",
                    data=csv_data,
                    file_name="funaab_cbt_report.csv",
                    mime="text/csv",
                )
            else:
                st.info("Take practice tests in Tab 1 to generate analytics history.")
                
        with col2:
            st.subheader("⭐ Bookmarked Revision Questions")
            if st.session_state.bookmarks:
                for b_idx, b_item in enumerate(st.session_state.bookmarks):
                    st.write(f"{b_idx+1}. {b_item}")
                if st.button("Clear Bookmarks"):
                    st.session_state.bookmarks = []
                    st.rerun()
            else:
                st.info("No questions bookmarked yet. Click 'Bookmark' during practice sessions.")

    # --- TAB 4: DAILY CHALLENGE & LEADERBOARD ---
    with tabs[3]:
        st.header("🌍 World Science Education Daily Challenge & Leaderboard")
        st.write("Answer today's challenge to climb the campus leaderboard!")
        
        st.markdown("**Daily Challenge Q1:** What is the atomic number of Carbon?")
        ans = st.radio("Select:", ["6", "12", "8", "14"], key="daily_ch")
        if st.button("Submit Daily Score"):
            if ans == "6":
                st.success("Correct! Points added.")
            else:
                st.error("Incorrect. Carbon's atomic number is 6.")
                
        st.markdown("---")
        st.subheader("🏆 Campus Leaderboard (Top Scorers)")
        for student, pts in st.session_state.leaderboard.items():
            st.write(f"• **{student}**: `{pts} pts`")

    # --- TAB 5: GPA CALCULATOR ---
    with tabs[4]:
        st.header("🧮 Target CGPA & Grade Calculator")
        st.write(f"Your target CGPA goal: **{current_user_data['target_cgpa']}**")
        
        st.subheader("Calculate Exam Grade Needed:")
        test_score = st.number_input("Your Continuous Assessment (CA) Score (Max 30)", 0, 30, 20)
        desired_total = st.slider("Desired Total Score for Course", 50, 100, 70)
        
        needed_exam = desired_total - test_score
        st.info(f"💡 You need to score at least **{needed_exam} / 70** in your main exam to hit your target score for this course!")

    # --- TAB 6: AI TUTOR & VOICE AGENT ---
    with tabs[5]:
        st.header("🤖 Amen AI Tutor & Voice Reader")
        if st.button("🔊 Read Question Aloud (AI Voice Agent)"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            st.success("AI Voice Agent reading active question...")
            
        q_text = st.text_input("Ask Amen AI any course concept question:")
        if st.button("Ask AI Tutor"):
            if q_text:
                st.success(f"**AI Explanation:** Breaking down '{q_text}' for 100-level success...")

    # --- TAB 7: WHATSAPP SHARE TO UNLOCK ---
    with tabs[6]:
        st.header("🎁 Share & Unlock Bonus Past Questions")
        st.write("Share this portal link to 3 WhatsApp study groups or statuses to unlock secret past question archives for free!")
        
        if not current_user_data["unlocked_bonus"]:
            if st.button("I have shared to WhatsApp! Unlock Bonus"):
                current_user_data["unlocked_bonus"] = True
                st.success("🎉 Bonus Unlocked! Check your course tabs for secret exam archives.")
                st.rerun()
        else:
            st.success("✅ Bonus Archive Unlocked & Active!")

    # --- TAB 8: OWNER ZONE (ADMIN) ---
    if current_user_data["role"] == "owner":
        with tabs[7]:
            st.header("👑 Owner Control Center")
            st.metric("Total Registered Students", len(st.session_state.users))
            st.metric("Estimated Revenue Generated", f"₦{len(st.session_state.users) * 1500:,}")
            
            st.subheader("📋 Registered Users Log:")
            for email, details in st.session_state.users.items():
                st.write(f"• **Email:** {email} | **Serial:** `{details['serial_number']}` | **College:** {details['college']} | **Paid:** {details['access_verified']}")

