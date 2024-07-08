import cv2
import streamlit as st
import numpy as np
from PIL import Image #Python Imaging Library (PIL), used for opening, manipulating, and saving images.
from predict import predict_image
import time

def add_custom_css():
    st.markdown(
        """
        <style>
        .stApp {
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
            st.image(image, caption="Uploaded Image", use_column_width=True)#displays uploaded image
            if st.button('Classify Image', key="classify_image"):
                st.write("Classifying...")
                with st.spinner('Processing...'):
                    time.sleep(2)  # simulate a delay for processing
                    result, probability = predict_image(image)#calls the prediction function on the image
                    st.write(f"Result: {result}")
                    st.write(f"Probability: {probability:.2f}")

                    # to generate and display detailed report
                    st.subheader("Detailed Analysis Report:")
                    if result == "Malignant":
                        st.write("The lesion shows signs of malignancy. Please consult a dermatologist.")
                        st.write("Probability of malignancy: {:.2f}".format(probability))
                    else:
                        st.write("Good news! The lesion appears benign however regular monitoring is still recommended.")
                        st.write("Probability of lession being benign: {:.2f}".format(probability))
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='content'>", unsafe_allow_html=True)
        st.header("Real-Time Scanning", anchor=None)
        # st.write("This functionality is under development.")
        if st.button("Start Camera", key="start_camera"):
            st.session_state["camera_running"] = True
        if st.session_state.get("camera_running", False):
            display_camera_feed()
        st.markdown("</div>", unsafe_allow_html=True)

def display_camera_feed():
    cap = cv2.VideoCapture(0)#opens the camera

    if not cap.isOpened():
        st.error("Unable to open the camera.")
        return

    stframe = st.empty()#empty Streamlit container where the camera feed will be displayed
    capture_button = st.button("Capture", key="capture_image")
    stop_button = st.button("Stop Camera", key="stop_camera_feed")

    while st.session_state.get("camera_running", False) and cap.isOpened():#as long as camera is running and is successfully opened
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image. Exiting...")
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB", use_column_width=True)

        if capture_button:
            st.session_state["captured_image"] = frame #stores captured frame in the session state.
            st.session_state["camera_running"] = False
            cap.release()
            break

        if stop_button:
            st.session_state["camera_running"] = False
            cap.release()
            break

    cap.release()

    if "captured_image" in st.session_state:
        img = st.session_state["captured_image"] #retrieves the captured image from the session state
        img_pil = Image.fromarray(img)  # Converts the NumPy array to a PIL Image.
        st.image(img_pil, caption='Captured Image', use_column_width=True)#displays the captured image.
        st.write("Classifying...")
        with st.spinner('Processing...'):
            time.sleep(2)  # Simulate a delay for processing
            result, probability = predict_image(img_pil)
            st.write(f"Result: {result}")
            st.write(f"Probability: {probability:.2f}")

            # generate and display detailed report
            st.subheader("Detailed Analysis Report:")
            if result == "Malignant":
                st.write("The lesion shows signs of malignancy. Please consult a dermatologist.")
                st.write("Probability of malignancy: {:.2f}".format(probability))
            else:
                st.write("The lesion appears benign. Regular monitoring is recommended.")
                st.write("Probability of malignancy: {:.2f}".format(probability))