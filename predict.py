import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load your trained model
model = load_model('model.h5')

def predict_image(image):
    # Convert image to grayscale
    image = image.convert('L')  # 'L' mode is for grayscale
    image = image.resize((128, 128))  # Adjust the size to match your model's input size
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=-1)  # Add channel dimension (1, 128, 128, 1)
    image = np.expand_dims(image, axis=0)
    
    # Perform inference
    results = model.predict(image)
    
    # Process the results (this will depend on the output format of your model)
    # Here we assume it returns a list of probabilities for each class
    result = "Malignant" if np.argmax(results) == 1 else "Benign"
    
    return result