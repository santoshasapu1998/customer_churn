import pandas as pd
import joblib
import streamlit as st

st.set_page_config(
    page_title="Predict Customer Churn",
    layout="wide"
)

st.title("Predict Customer Churn!")

# Load models and encoder
@st.cache_resource
def random_forest_pipeline():
    pipeline = joblib.load('Models/random_forest.joblib')
    return pipeline

def knn_pipeline():
    pipeline = joblib.load('Models/knn.joblib')
    return pipeline

def select_model():
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox('Select a model', options=['Random Forest', 'KNeighbors'], key='selected_model')
    with col2:
        pass

    if st.session_state['selected_model'] == 'Random Forest':
        pipeline = random_forest_pipeline()
    else:
        pipeline = knn_pipeline()

    encoder = joblib.load('Models/encoder.joblib')

    return pipeline, encoder

def save_prediction(data):
    df = pd.DataFrame(data)
    try:
        history_df = pd.read_csv('history.csv')
        history_df = pd.concat([history_df, df], ignore_index=True)
    except FileNotFoundError:
        history_df = df
    history_df.to_csv('history.csv', index=False)

def make_prediction(pipeline, encoder):      
    gender = st.session_state['gender']
    senior_citizen = st.session_state['senior_citizen']
    partner = st.session_state['partner']
    dependents = st.session_state['dependents']
    tenure = st.session_state['tenure']
    paperless_billing = st.session_state['paperless_billing']
    payment_method = st.session_state['payment_method']
    monthly_charges = st.session_state['monthly_charges']
    total_charges = st.session_state['total_charges']
    phone_service = st.session_state['phone_service']
    multiple_lines = st.session_state['multiple_lines']
    internet_service = st.session_state['internet_service']
    online_security = st.session_state['online_security']
    online_backup = st.session_state['online_backup']
    device_protection = st.session_state['device_protection']
    tech_support = st.session_state['tech_support']
    streaming_tv = st.session_state['streaming_tv']
    streaming_movies = st.session_state['streaming_movies']
    contract = st.session_state['contract']
    
    data = {'gender': [gender], 'seniorcitizen': [senior_citizen], 'partner': [partner], 'dependents': [dependents],
       'tenure': [tenure], 'phoneservice': [phone_service], 'multiplelines': [multiple_lines], 'internetservice': [internet_service],
       'onlinesecurity': [online_security], 'onlinebackup': [online_backup], 'deviceprotection': [device_protection], 'techsupport': [tech_support],
       'streamingtv': [streaming_tv], 'streamingmovies': [streaming_movies], 'contract': [contract], 'paperlessbilling': [paperless_billing],
       'paymentmethod': [payment_method], 'monthlycharges': [monthly_charges], 'totalcharges': [total_charges]}
    
    # Make a DataFrame
    df = pd.DataFrame(data)

    # Define Probability and Prediction
    pred = pipeline.predict(df)
    pred_int = int(pred[0])
    prediction = encoder.inverse_transform([pred_int])
    probability = pipeline.predict_proba(df)
    st.session_state['prediction'] = pred_int
    st.session_state['probability'] = probability

    # Save the prediction data
    data['prediction'] = pred_int
    data['probability'] = probability[0][1]  # assuming binary classification
    save_prediction(data)
    
    return prediction, probability

if 'prediction' not in st.session_state:
    st.session_state['prediction']= None
if 'probability' not in st.session_state:
    st.session_state['probability']= None

def display_form():
    pipeline, encoder = select_model()

    with st.form('input_features'):
        col1, col2 = st.columns(2)
        with col1:
            st.write('### Customer Details')
            st.selectbox('Gender', options=['Male', 'Female'], key='gender')
            st.selectbox('Senior Citizen', options=['Yes', 'No'], key='senior_citizen')
            st.selectbox('Partner', options=['Yes', 'No'], key='partner')
            st.selectbox('dependents', options=['Yes', 'No'], key='dependents')
            st.number_input('Tenure (months)', min_value=0, max_value=100, step=1, key='tenure')
            st.write('### Payment Methods')
            st.selectbox('Paperless Billing', options=['Yes', 'No'], key='paperless_billing')
            st.selectbox('Payment Method', options=['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], key='payment_method')
            st.number_input('Monthly Charges ($)', min_value=0.0, format="%.2f", key='monthly_charges')
            st.number_input('Total Charges ($)', min_value=0.0, format="%.2f", key='total_charges')
        with col2:
            st.write('### Packages Subscribed To')
            st.selectbox('Phone Service', options=['Yes', 'No'], key='phone_service')
            st.selectbox('Multiple Lines', options=['Yes', 'No'], key='multiple_lines')
            st.selectbox('Internet Service', options=['DSL', 'Fiber optic', 'No'], key='internet_service')
            st.selectbox('Online Security', options=['Yes', 'No'], key='online_security')
            st.selectbox('Online Backup', options=['Yes', 'No'], key='online_backup')
            st.selectbox('Device Protection', options=['Yes', 'No'], key='device_protection')
            st.selectbox('Tech Support', options=['Yes', 'No'], key='tech_support')
            st.selectbox('Streaming TV', options=['Yes', 'No'], key='streaming_tv')
            st.selectbox('Streaming Movies', options=['Yes', 'No'], key='streaming_movies')
            st.selectbox('Contract', options=['Month-to-month', 'One year', 'Two year'], key='contract')
            
        st.form_submit_button('Submit', on_click=make_prediction, kwargs=dict(pipeline=pipeline, encoder=encoder))

if __name__ == '__main__':
    display_form()
    prediction = st.session_state['prediction']
    if not prediction:
        st.write('### Predictions')
        st.divider()
    else:
        st.write(f'###{prediction}')
    st.write(st.session_state)