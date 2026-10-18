import streamlit as st

st.title("My First Streamlit App 🚀")
st.write("Hello! Welcome to my web app built with Python and Streamlit.")

# Add a simple interactive widget
name = st.text_input("What is your name?")

if name:
    st.success(f"Nice to meet you, {name}! Your app is working perfectly.")
