
import streamlit as st

st.title("My Awesome App")

# Feature 1: Your button and balloons
if st.button("Click Me"):
    st.balloons()

# Feature 2: A brand new number slider
number = st.slider("Pick a number", 1, 100)
st.write(f"You picked: {number}")
