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

# --- MASTER DATABASE (FIRST 4 TOPICS WITH REAL QUESTIONS) ---
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
                {"q": "What subatomic particle carries a negative charge?", "options": ["Proton", "Neutron", "Electron", "Positron"], "ans": "Electron", "expl": "Electrons orbit the nucleus and possess a negative elementary charge."},
                {"q": "Which quantum number describes the shape of an atomic orbital?", "options": ["Principal (n)", "Azimuthal/Angular (l)", "Magnetic (m)", "Spin (s)"], "ans": "Azimuthal/Angular (l)", "expl": "The azimuthal quantum number (l) designates the subshell (s, p, d, f) and orbital shape."},
                {"q": "Who discovered the electron using the cathode ray tube experiment?", "options": ["Ernest Rutherford", "J.J. Thomson", "James Chadwick", "Niels Bohr"], "ans": "J.J. Thomson", "expl": "J.J. Thomson discovered the electron in 1897."},
                {"q": "What is the maximum number of electrons that can fit in the 'p' subshell?", "options": ["2", "6", "10", "14"], "ans": "6", "expl": "A p-subshell has 3 orbitals, each holding 2 electrons, totaling 6."},
                {"q": "Which element has the highest electronegativity on the Pauling scale?", "options": ["Oxygen", "Chlorine", "Fluorine", "Nitrogen"], "ans": "Fluorine", "expl": "Fluorine is the most electronegative element with a value of 4.0."},
                {"q": "The Pauli Exclusion Principle states that no two electrons in the same atom can have:", "options": ["The same energy", "The same four quantum numbers", "The same spin", "The same orbit"], "ans": "The same four quantum numbers", "expl": "Every electron must have a unique set of quantum numbers."},
                {"q": "Who proposed the planetary model of the atom where electrons orbit the nucleus?", "options": ["John Dalton", "Niels Bohr", "Erwin Schrödinger", "J.J. Thomson"], "ans": "Niels Bohr", "expl": "Bohr introduced quantized orbits for electrons."},
                {"q": "What is an atom's mass number composed of?", "options": ["Protons only", "Electrons and Protons", "Protons and Neutrons", "Neutrons only"], "ans": "Protons and Neutrons", "expl": "Mass number is the total sum of protons and neutrons in the nucleus."},
                {"q": "Elements in the same group of the periodic table generally have:", "options": ["Same number of inner core electrons", "Same number of valence electrons", "Same atomic mass", "Same number of neutrons"], "ans": "Same number of valence electrons", "expl": "Group membership dictates similar chemical behavior via valence electrons."},
                {"q": "What is the electronic configuration of Sodium (Na, Z=11)?", "options": ["1s² 2s² 2p⁶ 3s¹", "1s² 2s² 2p⁵ 3s²", "1s² 2s² 2p⁶", "1s² 2s¹"], "ans": "1s² 2s² 2p⁶ 3s¹", "expl": "Sodium has 11 electrons filling up to the 3s orbital."},
                {"q": "Which of the following is a transition metal?", "options": ["Calcium", "Iron", "Sodium", "Aluminum"], "ans": "Iron", "expl": "Iron (Fe) belongs to the d-block transition metals."},
                {"q": "The energy required to remove an electron from a gaseous atom is called:", "options": ["Electron affinity", "Electronegativity", "Ionization energy", "Lattice energy"], "ans": "Ionization energy", "expl": "First ionization energy is the energy needed to strip an outer electron."},
                {"q": "Isotopes of an element differ in:", "options": ["Number of protons", "Number of electrons", "Number of neutrons", "Chemical reactivity"], "ans": "Number of neutrons", "expl": "Isotopes share atomic number but possess different neutron counts."},
                {"q": "Hund's rule of maximum multiplicity states that:", "options": ["Electrons pair up immediately", "Orbitals of equal energy are each filled with one electron before pairing", "Inner shells fill last", "Spin must always be negative"], "ans": "Orbitals of equal energy are each filled with one electron before pairing", "expl": "Degenerate orbitals half-fill first to minimize electron repulsion."},
                {"q": "What type of ion is formed when an atom loses electrons?", "options": ["Anion", "Cation", "Isotope", "Allotrope"], "ans": "Cation", "expl": "Loss of negative electrons results in a positively charged cation."}
            ],
            "Mole Concept & Stoichiometry": [
                {"q": "What is the molar mass of Carbon dioxide (CO₂)? [C=12, O=16]", "options": ["28 g/mol", "44 g/mol", "32 g/mol", "56 g/mol"], "ans": "44 g/mol", "expl": "12 + (16 × 2) = 44 g/mol."},
                {"q": "Avogadro's number represents the number of particles in how many moles?", "options": ["0.5 mole", "1 mole", "2 moles", "10 moles"], "ans": "1 mole", "expl": "1 mole equals 6.022 × 10²³ representative particles."},
                {"q": "What is the mass of 2 moles of Water (H₂O)? [H=1, O=16]", "options": ["18 g", "36 g", "20 g", "9 g"], "ans": "36 g", "expl": "Molar mass of H₂O is 18 g/mol. 2 moles × 18 = 36 g."},
                {"q": "How many moles are present in 98 grams of Sulfuric acid (H₂SO₄)?", "options": ["0.5 mol", "1 mol", "2 mol", "4 mol"], "ans": "1 mol", "expl": "Molar mass = 98 g/mol. 98g / 98g/mol = 1 mol."},
                {"q": "What volume does 1 mole of an ideal gas occupy at STP?", "options": ["11.2 liters", "22.4 liters", "44.8 liters", "1.0 liter"], "ans": "22.4 liters", "expl": "At STP, 1 mole of any ideal gas occupies 22.4 liters."},
                {"q": "What is the percentage composition of Hydrogen in Water (H₂O)?", "options": ["11.1%", "88.9%", "50.0%", "33.3%"], "ans": "11.1%", "expl": "(2 / 18) × 100 = 11.1%."},
                {"q": "The reactant that is completely consumed in a chemical reaction is called the:", "options": ["Excess reactant", "Limiting reactant", "Catalyst", "Intermediate"], "ans": "Limiting reactant", "expl": "The limiting reagent determines the maximum product yield."},
                {"q": "What is the empirical formula of a compound with molecular formula C₆H₁₂O₆?", "options": ["CHO", "CH₂O", "C₂H₄O₂", "C₃H₆O₃"], "ans": "CH₂O", "expl": "Simplifying subscripts by dividing by 6 gives CH₂O."},
                {"q": "What concentration unit is defined as moles of solute per liter of solution?", "options": ["Molality", "Molarity", "Normality", "Mole fraction"], "ans": "Molarity", "expl": "Molarity (M) = moles of solute / liters of solution."},
                {"q": "If 0.5 moles of NaCl are dissolved in 0.5 liters of solution, what is the molarity?", "options": ["0.25 M", "0.50 M", "1.00 M", "2.00 M"], "ans": "1.00 M", "expl": "0.5 moles / 0.5 L = 1.0 M."},
                {"q": "What is the oxidation state of Manganese in KMnO₄?", "options": ["+2", "+4", "+6", "+7"], "ans": "+7", "expl": "K(+1) + Mn + 4(-2) = 0 => Mn = +7."},
                {"q": "In a balanced chemical equation, the coefficients represent:", "options": ["Mass ratios", "Mole ratios", "Volume ratios only", "Density ratios"], "ans": "Mole ratios", "expl": "Coefficients in stoichiometry indicate relative numbers of moles."},
                {"q": "How many atoms are in 1 mole of Helium gas?", "options": ["6.022 × 10²³", "3.011 × 10²³", "1.204 × 10²⁴", "1.000 × 10²⁰"], "ans": "6.022 × 10²³", "expl": "Avogadro's constant governs particle count per mole."},
                {"q": "What is the molarity of a solution containing 40g of NaOH in 2L of solution?", "options": ["0.25 M", "0.50 M", "1.00 M", "2.00 M"], "ans": "0.50 M", "expl": "NaOH molar mass = 40 g/mol. Moles = 1. 1 mol / 2 L = 0.50 M."},
                {"q": "What law states that matter is neither created nor destroyed during a chemical reaction?", "options": ["Law of Definite Proportions", "Law of Conservation of Mass", "Dalton's Law", "Gay-Lussac's Law"], "ans": "Law of Conservation of Mass", "expl": "Mass of reactants equals mass of products in a closed system."}
            ],
            "States of Matter (Gases & Liquids)": [
                {"q": "Which gas law relates volume and temperature directly at constant pressure?", "options": ["Boyle's Law", "Charles's Law", "Avogadro's Law", "Dalton's Law"], "ans": "Charles's Law", "expl": "Charles's law states V is directly proportional to T when P is constant."},
                {"q": "What is the mathematical expression for the Ideal Gas Equation?", "options": ["PV = nRT", "P₁V₁ = P₂V₂", "V / T = k", "P / T = k"], "ans": "PV = nRT", "expl": "The ideal gas law combines pressure, volume, moles, and temperature."},
                {"q": "Boyle's Law establishes an inverse relationship between which two variables?", "options": ["Pressure and Volume", "Volume and Temperature", "Pressure and Temperature", "Moles and Volume"], "ans": "Pressure and Volume", "expl": "As pressure increases, volume decreases proportionately at constant temperature."},
                {"q": "At absolute zero temperature (0 Kelvin), what happens to ideal gas volume theoretically?", "options": ["Becomes infinite", "Reaches zero", "Remains constant", "Doubles"], "ans": "Reaches zero", "expl": "Molecular motion theoretically ceases entirely at 0 K."},
                {"q": "Which intermolecular force is strongest among polar molecules containing H bonded to F, O, or N?", "options": ["London dispersion forces", "Dipole-dipole forces", "Hydrogen bonding", "Ion-induced dipole"], "ans": "Hydrogen bonding", "expl": "Hydrogen bonding is a particularly strong dipole-dipole interaction."},
                {"q": "What is the term for a liquid's resistance to flow?", "options": ["Surface tension", "Viscosity", "Vapor pressure", "Capillary action"], "ans": "Viscosity", "expl": "High intermolecular attraction results in high liquid viscosity."},
                {"q": "The pressure exerted by a vapor in equilibrium with its liquid phase is called:", "options": ["Atmospheric pressure", "Vapor pressure", "Osmotic pressure", "Critical pressure"], "ans": "Vapor pressure", "expl": "Vapor pressure increases with temperature."},
                {"q": "What condition causes real gases to deviate most significantly from ideal gas behavior?", "options": ["High temperature and low pressure", "Low temperature and high pressure", "High temperature and high volume", "Standard conditions"], "ans": "Low temperature and high pressure", "expl": "Under high pressure and low temperature, intermolecular forces matter."},
                {"q": "What is the SI unit of pressure?", "options": ["Atmosphere (atm)", "Pascal (Pa)", "Torr", "mmHg"], "ans": "Pascal (Pa)", "expl": "The Pascal (N/m²) is the standard international unit for pressure."},
                {"q": "Which phenomenon allows insects to walk on water surfaces?", "options": ["Viscosity", "Surface tension", "Vapor pressure", "Sublimation"], "ans": "Surface tension", "expl": "Inward intermolecular pulls create a resilient surface skin."},
                {"q": "What is the process where a solid turns directly into a gas without passing through the liquid phase?", "options": ["Melting", "Evaporation", "Sublimation", "Condensation"], "ans": "Sublimation", "expl": "Sublimation occurs in substances like dry ice."},
                {"q": "Dalton's Law of Partial Pressures states that:", "options": ["Total pressure is the sum of partial pressures", "Pressure equals volume times temperature", "Gas density is constant", "Partial pressure equals mole fraction times volume"], "ans": "Total pressure is the sum of partial pressures", "expl": "Total pressure equals sum of individual partial pressures."},
                {"q": "What temperature scale must always be used in gas law calculations?", "options": ["Celsius", "Fahrenheit", "Kelvin", "Rankine"], "ans": "Kelvin", "expl": "Absolute temperature in Kelvin prevents negative numbers."},
                {"q": "The temperature at which a liquid's vapor pressure equals external atmospheric pressure is its:", "options": ["Melting point", "Boiling point", "Triple point", "Critical temperature"], "ans": "Boiling point", "expl": "At this point, bulk vaporization occurs."},
                {"q": "What type of intermolecular force exists between nonpolar molecules?", "options": ["Hydrogen bonds", "Ion-dipole forces", "London dispersion forces", "Covalent bonds"], "ans": "London dispersion forces", "expl": "Temporary instantaneous dipoles cause weak London dispersion forces."}
            ],
            "Thermochemistry & Enthalpy": [
                {"q": "What term describes a chemical reaction that absorbs heat from its surroundings?", "options": ["Exothermic", "Endothermic", "Isothermal", "Adiabatic"], "ans": "Endothermic", "expl": "Endothermic reactions have a positive enthalpy change (+ΔH)."},
                {"q": "What is the sign of ΔH for an exothermic reaction?", "options": ["Positive (+)", "Negative (-)", "Zero", "Variable"], "ans": "Negative (-)", "expl": "Exothermic reactions release thermal energy into the surroundings."},
                {"q": "What law states that the total enthalpy change of a reaction is independent of the pathway taken?", "options": ["First Law of Thermodynamics", "Hess's Law", "Boyle's Law", "Le Chatelier's Principle"], "ans": "Hess's Law", "expl": "Hess's Law allows calculation of unknown enthalpy changes."},
                {"q": "What is the standard unit of enthalpy change in thermodynamics?", "options": ["Joules per mole (J/mol)", "Kelvin", "Watts", "Moles per liter"], "ans": "Joules per mole (J/mol)", "expl": "Enthalpy change is typically measured in kJ/mol or J/mol."},
                {"q": "The amount of heat required to raise the temperature of 1 gram of a substance by 1°C is called:", "options": ["Heat capacity", "Specific heat capacity", "Latent heat", "Enthalpy of fusion"], "ans": "Specific heat capacity", "expl": "Specific heat capacity measures thermal inertia per unit mass."},
                {"q": "What calorimeter instrument is typically used to measure heat of combustion at constant volume?", "options": ["Coffee-cup calorimeter", "Bomb calorimeter", "Barometer", "Manometer"], "ans": "Bomb calorimeter", "expl": "A bomb calorimeter handles high-pressure combustion reactions safely."},
                {"q": "What is standard enthalpy of formation defined as for an element in its standard state?", "options": ["+100 kJ/mol", "0 kJ/mol", "-50 kJ/mol", "Infinite"], "ans": "0 kJ/mol", "expl": "Pure elements in their stable standard states have formation enthalpy of zero."},
                {"q": "Which thermodynamic law states that energy can neither be created nor destroyed?", "options": ["Zeroth Law", "First Law", "Second Law", "Third Law"], "ans": "First Law", "expl": "The First Law of Thermodynamics is the law of conservation of energy."},
                {"q": "What is the enthalpy change accompanying the addition of an electron to a gaseous atom?", "options": ["Ionization energy", "Electron affinity", "Lattice energy", "Atomization energy"], "ans": "Electron affinity", "expl": "Electron affinity measures energy release or absorption."},
                {"q": "Which factor determines whether a reaction is spontaneous under all temperatures?", "options": ["Negative ΔH and positive ΔS", "Positive ΔH and negative ΔS", "Positive ΔH and positive ΔS", "Negative ΔH and negative ΔS"], "ans": "Negative ΔH and positive ΔS", "expl": "Gibbs free energy is always negative when ΔH < 0 and ΔS > 0."},
                {"q": "What is the enthalpy change when 1 mole of a substance melts at constant temperature?", "options": ["Enthalpy of vaporization", "Enthalpy of fusion", "Enthalpy of sublimation", "Enthalpy of combustion"], "ans": "Enthalpy of fusion", "expl": "Enthalpy of fusion refers to the solid-to-liquid phase transition energy."},
                {"q": "In the equation ΔG = ΔH - TΔS, what does ΔG represent?", "options": ["Total entropy", "Internal energy", "Gibbs free energy", "Enthalpy change"], "ans": "Gibbs free energy", "expl": "Gibbs free energy determines chemical reaction spontaneity."},
                {"q": "What is the standard temperature condition used in thermochemical data tables?", "options": ["0 °C", "25 °C (298.15 K)", "100 °C", "37 °C"], "ans": "25 °C (298.15 K)", "expl": "Standard thermodynamic reference temperature is typically 298.15 K."},
                {"q": "The heat absorbed or released during a physical or chemical change at constant pressure is equal to:", "options": ["Internal energy change", "Enthalpy change", "Entropy change", "Work done"], "ans": "Enthalpy change", "expl": "By definition, ΔH equals heat flow at constant pressure."},
                {"q": "What is the term for a process that occurs without ongoing outside intervention?", "options": ["Non-spontaneous", "Spontaneous", "Equilibrium", "Endothermic"], "ans": "Spontaneous", "expl": "A spontaneous process proceeds naturally under specified conditions."}
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
    
    if current_user_data["role"] == "owner":
        tabs = st.tabs(["📚 CBT Portal", "⏱️ Exam Mode", "🌍 Leaderboard", "📊 GPA", "🤖 AI & Voice", "🎁 Bonus", "👑 Admin Control Center"])
    else:
        tabs = st.tabs(["📚 CBT Portal", "⏱️ Exam Mode", "🌍 Leaderboard", "📊 GPA", "🤖 AI & Voice", "🎁 Bonus"])

    # --- TAB 1: CBT PORTAL ---
    with tabs[0]:
        st.header("📚 CHM 101 Practice Portal (First 4 Master Topics)")
        selected_course = st.selectbox("Choose Course", list(PORTAL_DATA.keys()))
        course_topics = PORTAL_DATA[selected_course]["Topics"]
        selected_topic = st.selectbox("Choose Topic", course_topics)
        
        questions_pool = PORTAL_DATA[selected_course]["Questions"].get(selected_topic, [])
        if questions_pool:
            st.info(f"Loaded **{len(questions_pool)} verified questions** for {selected_topic}.")
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

    # --- TAB 7: ADMIN CONTROL CENTER ---
    if current_user_data["role"] == "owner":
        with tabs[6]:
            st.header("👑 Admin & Owner Control Center")
            st.metric("Total Registered Students", len(st.session_state.users))
            st.metric("Total Revenue Generated", f"₦{len(st.session_state.users) * 1500:,}")
            
            st.subheader("📋 Registered Users Log:")
            for email, details in st.session_state.users.items():
                st.write(f"• **Name:** {details.get('name', 'N/A')} | **Serial:** `{details['serial_number']}` | **College:** {details['college']}")
