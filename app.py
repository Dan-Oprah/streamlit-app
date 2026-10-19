import streamlit as st
import random
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AMEN SCHOOL ULTIMATE CBT PORTAL",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SESSION STATE INITIALIZATION & OWNER ACCOUNT ---
if "users" not in st.session_state:
    st.session_state.users = {
        "sunmonuabiodun01@gmail.com": {
            "name": "Sunmonu Amen Oluwatobi",
            "password": "At4#5666",
            "college": "COLPHYS (Physical Sciences)",
            "department": "Computer Science",
            "sex": "Male",
            "dob": "2005-01-01",
            "target_cgpa": 5.0,
            "serial_number": "205001",
            "access_verified": True,
            "unlocked_bonus": True,
            "role": "owner"
        }
    } 

if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "registration_counter" not in st.session_state:
    st.session_state.registration_counter = 205001 
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {
        "Sunmonu Amen (205001)": 500,
        "205012 (Mech Eng)": 450,
        "205045 (Microbio)": 420,
        "205008 (Agric Econ)": 390
    }

# --- MASTER DATABASE ---
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
                {"q": "Which quantum number describes the shape of an orbital?", "options": ["Principal (n)", "Azimuthal/Angular (l)", "Magnetic (m)", "Spin (s)"], "ans": "Azimuthal/Angular (l)", "expl": "Azimuthal quantum number determines the subshell shape."},
            ],
            "Mole Concept & Stoichiometry": [
                {"q": "What is the molar mass of Carbon dioxide (CO2)? [C=12, O=16]", "options": ["28 g/mol", "44 g/mol", "32 g/mol", "56 g/mol"], "ans": "44 g/mol", "expl": "12 + (16 * 2) = 44 g/mol."},
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

# --- THEME STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    p, span, label, div, .stRadio label { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# MAIN APP ROUTING & CLEAN OWNER ENTRY
# ==========================================
if st.session_state.current_user is None:
    st.title("🎓 AMEN SCHOOL ULTIMATE CBT PORTAL (FUNAAB)")
    st.info("Welcome to the 100-Level Premium EdTech Portal.")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Founder / Owner Access")
        if st.button("🚀 One-Click Owner Login (Sunmonu Amen)"):
            st.session_state.current_user = "sunmonuabiodun01@gmail.com"
            st.rerun()
            
    with col2:
        st.subheader("📖 AMEN SCHOOL ULTIMATE GUIDE")
        st.write("The premier academic survival blueprint for FUNAAB freshmen targeting 4.5+ CGPA.")

else:
    current_user_data = st.session_state.users[st.session_state.current_user]
    
    col_top1, col_top2 = st.columns([3, 1])
    with col_top1:
        st.write(f"👤 **Portal Owner:** {current_user_data['name']} (`{current_user_data['serial_number']}`)")
    with col_top2:
        if st.button("Log Out"):
            st.session_state.current_user = None
            st.rerun()
            
    st.markdown("---")
    
    # --- ADMIN / OWNER RESTRICTED TABS ---
    if current_user_data["role"] == "owner":
        tabs = st.tabs(["📚 CBT Portal", "⏱️ Exam Mode", "🌍 Leaderboard", "📊 GPA", "🤖 AI & Voice", "🎁 Bonus", "👑 Admin Control Center"])
    else:
        tabs = st.tabs(["📚 CBT Portal", "⏱️ Exam Mode", "🌍 Leaderboard", "📊 GPA", "🤖 AI & Voice", "🎁 Bonus"])

    # --- TAB 1: CBT PORTAL ---
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
                st.success(f"Score: {score} / {len(questions_pool)}")
                for idx, q in enumerate(questions_pool):
                    st.info(f"💡 **Explanation for Q{idx+1}:** {q['expl']}")

    # --- TAB 2: EXAM MODE ---
    with tabs[1]:
        st.header("⏱️ CBT Exam Simulation Mode")
        if st.button("Start 30-Minute Exam Simulation"):
            st.warning("⚠️ Exam Session Active!")
            timer_placeholder = st.empty()
            for seconds_left in range(10, 0, -1):
                timer_placeholder.markdown(f"⏳ **Time Remaining:** {seconds_left} secs")
                time.sleep(0.1) 
            st.error("⏰ Time's up!")

    # --- TAB 3: LEADERBOARD ---
    with tabs[2]:
        st.header("🌍 Leaderboard")
        for student, pts in st.session_state.leaderboard.items():
            st.write(f"• **{student}**: `{pts} pts`")

    # --- TAB 4: GPA CALCULATOR ---
    with tabs[3]:
        st.header("📊 Target CGPA Calculator")
        test_score = st.number_input("Your CA Score (Max 30)", 0, 30, 20)
        desired_total = st.slider("Desired Total Score", 50, 100, 70)
        st.info(f"💡 Needed Exam Score: **{desired_total - test_score} / 70**")

    # --- TAB 5: AI TUTOR ---
    with tabs[4]:
        st.header("🤖 Amen AI Tutor & Voice Reader")
        if st.button("🔊 Read Question Aloud"):
            st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
            st.success("AI Voice Agent reading question...")

    # --- TAB 6: BONUS ---
    with tabs[5]:
        st.header("🎁 Share & Unlock Bonus")
        st.success("✅ Bonus Archive Unlocked & Active!")

    # --- TAB 7: ADMIN CONTROL CENTER (RESTRICTED TO OWNER ONLY) ---
    if current_user_data["role"] == "owner":
        with tabs[6]:
            st.header("👑 Admin & Owner Control Center")
            st.write("🔒 **Restricted Access:** Only Sunmonu Amen Oluwatobi can manage revenue and student activity here.")
            st.metric("Total Registered Students", len(st.session_state.users))
            st.metric("Total Revenue Generated", f"₦{len(st.session_state.users) * 1500:,}")
            
            st.subheader("📋 Registered Users Log:")
            for email, details in st.session_state.users.items():
                st.write(f"• **Name:** {details.get('name', 'N/A')} | **Serial:** `{details['serial_number']}` | **College:** {details['college']}")
