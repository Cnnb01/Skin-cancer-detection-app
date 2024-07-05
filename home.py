import streamlit as st
from PIL import Image
import cv2
import numpy as np
from predict import predict_image
import time

def add_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://yourimageurl.com/background.jpg");
            background-size: cover;
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center; 
            color: white; 
            font-size: 2.5em;
            margin-bottom: 0;
        }
        .subtitle {
            text-align: center; 
            color: white; 
            font-size: 1.5em;
            margin-top: 0;
        }
        .content {
            background-color: rgba(0, 0, 0, 0.5); 
            padding: 20px; 
            border-radius: 10px;
            margin: 20px 0;
        }
        .content h3 {
            color: white;
        }
        .content p {
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def app():
    add_custom_css()

    st.markdown("<h1 class='title'>Skin Cancer Detection Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Upload an image or scan in real-time to detect skin cancer</h2>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class='content'>
        <h3>Welcome to the Skin Cancer Detection Scanner</h3>
        <h4>Early detection saves lives.</h4>
        <p>Skin cancer is one of the most common cancers worldwide. Early detection
    can significantly increase the chances of successful treatment. This application
    allows you to upload an image or scan in real-time to receive a preliminary
    assessment of potential skin cancer.</p>

    <p>**Disclaimer:** This application is not intended to be a substitute for professional
    medical diagnosis. Always consult a dermatologist for any concerns about your skin health.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='content'>", unsafe_allow_html=True)
        st.header("Upload Image", anchor=None)
        uploaded_image = st.file_uploader("Upload an image.")
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.write("Classifying...")
            with st.spinner('Processing...'):
                time.sleep(2)  # Simulate a delay for processing
                result = predict_image(image)
                st.write(f"Result: {result}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='content'>", unsafe_allow_html=True)
        st.header("Real-Time Scanning", anchor=None)
        st.write("This functionality is under development.")
        if st.button("Start Camera"):
            capture_image()
        st.markdown("</div>", unsafe_allow_html=True)

def capture_image():
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture image")
            break
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB", use_column_width=True)
        if st.button("Capture"):
            img = frame
            cap.release()
            st.image(img, caption='Captured Image', use_column_width=True)
            st.write("Classifying...")
            with st.spinner('Processing...'):
                time.sleep(2)  # Simulate a delay for processing
                result = predict_image(img)  # Call your model prediction function here
                st.write(f"Result: {result}")
            break