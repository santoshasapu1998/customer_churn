import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(
    page_title="Data page",
    layout="wide"
)

st.title("Customer Churn Database - Vodafone")

@st.cache_resource(show_spinner='Connecting to database...')
def init_connection():
    try:
        connection = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=" + st.secrets['DB_SERVER'] + ";"
            "DATABASE=" + st.secrets['DB_NAME'] + ";"
            "UID=" + st.secrets['DB_LOGIN'] + ";"
            "PWD=" + st.secrets['DB_PASSWORD']
        )
        return connection
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

connection = init_connection()

@st.cache_data(show_spinner='Running query...')
def running_query(query, _connection):
    try:
        with _connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame.from_records(rows, columns=[column[0] for column in cursor.description])
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def get_all_column():
    sql_query = "SELECT * FROM LP2_Telco_churn_first_3000"
    return running_query(sql_query, connection)

df = get_all_column()

if df.empty:
    st.error("No data retrieved from the database.")
else:
    numerical_columns = df.select_dtypes(include=['number']).columns
    categorical_columns = df.select_dtypes(exclude=['number']).columns

    option = st.selectbox('Select columns to display', options=['All columns', 'Numerical columns', 'Categorical columns'])

    if option == 'All columns':
        st.write(df)
    elif option == 'Numerical columns':
        st.write(df[numerical_columns])
    elif option == 'Categorical columns':
        st.write(df[categorical_columns])