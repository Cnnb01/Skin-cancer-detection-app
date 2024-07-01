import streamlit as st
from PIL import Image
import cv2
import numpy as np
from predict import predict_image

def app():
    st.title('Skin Cancer Detection Scanner')
    st.subheader('Upload an image or scan in real-time to detect skin cancer')
    st.markdown("""
    ### Welcome to the Skin Cancer Detection Scanner
    Skin cancer is one of the most common types of cancer worldwide. Early detection can significantly increase the chances of successful treatment. This application allows you to upload an image or scan in real-time to detect skin cancer.
    """)

    #creating two columns, to upload and to scan
    col1, col2 = st.columns(2)

    #uploading functionality
    with col1:
        st.header("Upload Image")
        uploaded_image = st.file_uploader("Upload an image.")
        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.write("Classifying...")
            #calling prediction function here
            result = predict_image(image)
            st.write(f"Result: {result}")

    #scanning functionality
    with col2:
        st.header("Real-Time Scanning")
        st.write("This functionality is under development.")
        if st.button("Start Camera"):
            capture_image()

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
            result = predict_image(img)  # Call your model prediction function here
            st.write(f"Result: {result}")
            break