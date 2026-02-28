import streamlit as st
import numpy as np
from textblob import TextBlob
import pickle

# Load trained model
with open("sentiment_model.pkl", "rb") as file:
    model = pickle.load(file)

st.title("Airline Review Sentiment Predictor")

review = st.text_area("Enter a review:")
if st.button("Predict Sentiment"):
    sentiment_score = TextBlob(review).sentiment.polarity
    prediction = model.predict(np.array([[sentiment_score, len(review.split()), 5, 10]]))  # Example input
    st.write(f"Predicted Sentiment: {prediction[0]}")
