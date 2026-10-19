import random
import streamlit as st

st.title("AMEN SCHOOL ULTIMATE CBT PORTAL")

# Example master question bank containing questions for all topics
# (Replace or expand this with your actual database or dictionary)
master_question_bank = {
    "States of Matter": [
        {
            "text": (
                "How do kinetic molecular theory parameters affect real gas"
                " behavior under high pressure?"
            ),
            "options": [
                "No effect",
                "Significant deviation due to particle volume",
                "Perfect ideality",
                "Infinite expansion",
            ],
        },
        {
            "text": "What causes gases to deviate from ideal behavior at very low temperatures?",
            "options": [
                "Intermolecular attractive forces become significant",
                "Kinetic energy increases infinitely",
                "Particle volume becomes zero",
                "Pressure drops to absolute zero",
            ],
        },
        # Add more unique questions for States of Matter here...
    ],
    "Organic Chemistry": [
        {
            "text": "What is the primary product of the hydration of an alkene?",
            "options": ["Alcohol", "Alkane", "Alyne", "Carboxylic acid"],
        },
        {
            "text": "Which functional group characterizes a ketone?",
            "options": [
                "Carbonyl group bonded to two carbon atoms",
                "Hydroxyl group",
                "Carboxyl group",
                "Amino group",
            ],
        },
        # Add more unique questions for Organic Chemistry here...
    ],
}

# --- TOPIC SELECTION ---
selected_topic = st.selectbox(
    "Choose a Topic", list(master_question_bank.keys())
)

# --- RESET BUTTON & STATE MANAGEMENT ---
# If the user changes the topic or clicks reset, we clear the old quiz session state
if "current_topic" not in st.session_state or st.session_state.current_topic != selected_topic:
  st.session_state.current_topic = selected_topic
  # Randomly pick unique questions from the selected topic (e.g., up to 20 questions)
  topic_bank = master_question_bank.get(selected_topic, [])
  st.session_state.quiz_questions = random.sample(
      topic_bank, min(len(topic_bank), 20)
  )

if st.button("Reset Quiz & Get New Questions"):
  topic_bank = master_question_bank.get(selected_topic, [])
  st.session_state.quiz_questions = random.sample(
      topic_bank, min(len(topic_bank), 20)
  )
  st.rerun()

# --- DISPLAY QUIZ QUESTIONS UNIQUELY ---
st.write(f"### {selected_topic} Practice Test")

# We loop safely using enumerate so Q1, Q2, Q3... all pull distinct items from our randomized list
for i, q in enumerate(st.session_state.quiz_questions):
  st.markdown(f"**Q{i+1}: {q['text']}**")

  # Unique key per question ensures choices don't bleed into each other or repeat
  st.radio(
      label=f"Select answer for Q{i+1}",
      options=q["options"],
      key=f"question_{selected_topic}_{i}",
  )
  st.markdown("---")
