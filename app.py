import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# Function to load the pre-trained model
@st.cache(allow_output_mutation=True)
def load_model():
    model = pickle.load(open('phishing.pkl', 'rb'))
    return model

# Function to make predictions
@st.cache(allow_output_mutation=True)
def predict_phishing(_model, url):
    # Preprocess the URL (tokenization, stemming, etc.)
    # Implement your preprocessing steps here

    # Make prediction using the loaded model
    prediction = _model.predict([url])
    return prediction[0]

def main():
    # Load the pre-trained model
    model = load_model()

    # Data structure to store past URLs and predictions
    history = []

    # Custom HTML and CSS styling
    custom_styles = """
    <style>
    body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4; /* Light gray */
        margin: 0;
        padding: 0;
    }
    .container {
        max-width: 800px;
        margin: 50px auto;
        padding: 20px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }
    .title {
        text-align: center;
        color: #333333; /* Dark gray */
        margin-bottom: 20px;
    }
    .input-container {
        margin-bottom: 20px;
    }
    .input-field {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .button {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
        padding: 10px;
        font-size: 16px;
        color: #fff;
        background-color: #4CAF50; /* Green */
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .button:hover {
        background-color: #45a049; /* Darker green on hover */
    }
    .spinner {
        border: 4px solid rgba(0, 0, 0, 0.1);
        border-left-color: #333;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        animation: spin 1s linear infinite;
        margin-right: 10px;
        display: none; /* Initially hidden */
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .red-background {
        background-color: #FF0000 !important; /* Red */
    }
    </style>
    """

    # Display custom styles
    st.markdown(custom_styles, unsafe_allow_html=True)

    # Sidebar - Phishing Info
    st.sidebar.title("Phishing Info")
    with open("phishing_info.md", "r") as file:
        phishing_info = file.read()
    st.sidebar.markdown(phishing_info)

    # Main content with dynamic background color
    st.markdown("<div id='main-container'></div>", unsafe_allow_html=True)

    # Title
    st.markdown("<script>document.getElementById('main-container').className += ' container';</script>", unsafe_allow_html=True)
    st.markdown("<h1 class='title'>Phishing Website Detection</h1>", unsafe_allow_html=True)

    # Image
    st.markdown("<script>document.getElementById('main-container').style.backgroundColor = '#f4f4f4';</script>", unsafe_allow_html=True)
    st.image('security.png', width=200, caption='Security')

    # Input field
    url = st.text_input('Enter the URL of the website:', value='', help='e.g., https://example.com')

    # Button with spinner
    button_html = """
    <div id='predict-button' class='button' onclick='disableButton()'>
        <div class='spinner'></div>
        Check for Phishing
    </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)

    # Progress bar
    progress_bar = st.progress(0)

    # Prediction result
    prediction_result = st.empty()

    if st.button('', key='predict-button-hidden'):
        with st.spinner('Making prediction...'):
            # Simulate a time-consuming task (replace this with your actual prediction task)
            for i in range(100):
                time.sleep(0.02)  # Simulate computation time
                progress_bar.progress(i + 1)

            # Make prediction
            prediction = predict_phishing(model, url)

            # Update history
            history.append((url, prediction))

            # Display the prediction result
            if prediction == 'bad':
                prediction_result.markdown("<p class='result error-message'>⚠️ This website is classified as a phishing website.</p>", unsafe_allow_html=True)
                st.markdown("<script>document.getElementById('main-container').className += ' red-background';</script>", unsafe_allow_html=True)  # Change background color to red
            else:
                prediction_result.markdown("<p class='result success-message'>✅ This website is classified as not a phishing website.</p>", unsafe_allow_html=True)
                st.markdown("<script>document.getElementById('main-container').className = document.getElementById('main-container').className.replace(' red-background', '');</script>", unsafe_allow_html=True)  # Remove red background color if not phishing

    # Display history
    st.write("### Prediction History")
    if history:
        for url, prediction in history:
            st.write(f"- **URL:** {url}, **Prediction:** {prediction}")
    else:
        st.write("No past predictions.")

if __name__ == '__main__':
    main()
