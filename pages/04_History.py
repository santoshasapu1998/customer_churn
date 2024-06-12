import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Prediction History",
    layout="wide"
)

st.title("Prediction History")

# Load the prediction history
def load_history():
    try:
        history_df = pd.read_csv('history.csv')
        return history_df
    except FileNotFoundError:
        return pd.DataFrame()

history_df = load_history()

if history_df.empty:
    st.write("No prediction history available.")
else:
    st.write(history_df)
    st.download_button(
        label="Download history as CSV",
        data=history_df.to_csv(index=False),
        file_name='prediction_history.csv',
        mime='text/csv',
    )
