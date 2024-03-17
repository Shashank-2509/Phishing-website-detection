import streamlit as st
import pickle
from urllib.parse import urlparse
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import numpy as np

st.title('Phishing Website Detection')

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# User input for prediction
message = st.text_area('Enter a link:')
prediction_button = st.button('Predict')

# Check if the prediction button is clicked
if prediction_button:
    # Extract features from the URL
    parsed_url = urlparse(message)

    # Features based on URL components
    features = [
        len(parsed_url.netloc),  # Length of the network location part
        len(parsed_url.path),    # Length of the path part
        len(parsed_url.query),   # Length of the query string part
    ]

    # Convert features to a space-separated string
    features_str = ' '.join(map(str, features))

    # Make prediction using the loaded model
    prediction = model.predict([features_str])

    # Display the prediction result
    st.subheader('Prediction:')
    if prediction[0] == 'bad':
        st.warning('This link is classified as dangerous. Exercise caution.')
    else:
        st.success('This link is classified as secure. It appears to be safe.')


