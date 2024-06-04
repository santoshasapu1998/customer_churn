import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(
    page_title="Data page",
    page_icon=":house:",
    layout="wide"
)

st.title("Customer Churn Database - Vodafone")

@st.cache_resource(show_spinner='connecting to database...')
def init_connection():
    return pyodbc.connect(
        "DRIVER = {SQL Server}: SERVER="
        + st.secrets['DB_SERVER']
        + "; DATABASE="
        + st.secrets['DB_NAME']
        + "; UID="
        + st.secrets['DB_LOGIN']
        + "; PWD="
        + st.secrets['DB_PASSWORD']
    )


connection = init_connection()

@st.cache_data(show_spinner='running_query...')
def running_query(query):
    with connection.cursor() as c:
        c.execute(query)
        rows = c.fetchall()
        df = pd.DataFrame.from_records(rows, columns=[column[0] for column in c.description])

    return df

sql_query = "SELECT * FROM dbo.LP2_Telco_churn_first_3000"

rows = running_query(sql_query)

st.write(rows)