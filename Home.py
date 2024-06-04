import streamlit as st

st.set_page_config(
    page_title="Home page",
    page_icon=":house:",
    layout="wide"
)

st.title("Attrition Predictor!")

name = st.text_input("What is your name?")

st.write(f"Welcome {name}")