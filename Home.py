import streamlit as st
from includes.logo import logo

# # Set page configuration
st.set_page_config(
    page_title='Home Page',
    page_icon='🏠',
    layout="wide",
    initial_sidebar_state='expanded'
)

# Use app logo
logo()

st.write("**About us**")
st.write("""
    A team of Data scientists collabrated to build this application using past data from vodafone.
    We built this application for companies in the Telco industry that are willing to retain their customers
""")
st.write("Predict if a customer is about to churn based on known characteristics using Machine Learning.")

# Create two columns
col1, col2 = st.columns(2)

with col1:
        st.write("### Key Features",)
        st.write("""
        - **Data**: Access the data.
        - **Dashboard**: Explore interactive data visualizations for insghts.
        - **Predict**: Predict customer churn outcomes.
        - **History**: Access past predictions.

        """)
        
        st.write("### Machine Learning Integration",)
        st.write("""
                - **Accurate Predictions**: Integrate advanced ML algorithms for accurate predictions.
                - **Data-Driven Decisions**: Leverage comprehensive customer data to inform strategic initiatives.
                - **Variety**: Choose between two advanced ML algorithms for predictions""")

with col2:
        st.write("### Follow the instructions below on how to run application")
        st.code("""
          activate virtual environment
          ./venv/Scripts/activate
          streamlit run Home.py
    """)
        st.write("### User Benefits",)
        st.write("""
        - **Accurate Prediction**: Reduce churn rate.
        - **Data-Driven Decisions**: Inform strategic initiatives.
        - **Enhanced Insights**: Understand customer behavior.
        """)
        
        with st.expander("Need Help?", expanded=False):
               st.link_button('Repository on Github', url='https://github.com/Moriahasare/Customer_Churn_Streamlit_App')
               st.markdown('[E-mail](mailto:moriahasare@gmail.com)')
