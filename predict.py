import streamlit as st
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

# Load your trained model
model = load_model('model.h5')

def predict_image(image):
    # Convert image to grayscale
    # image = image.convert('L')  # 'L' mode is for grayscale
    # image = image.resize((128, 128))  # Adjust the size to match your model's input size
    # image = np.array(image) / 255.0
    # image = np.expand_dims(image, axis=-1)  # Add channel dimension (1, 128, 128, 1)
    # image = np.expand_dims(image, axis=0)
    image_gray = image.convert('L')  # 'L' mode is for grayscale
    image_resized = image_gray.resize((128, 128))  # Adjust size to match model input
    image_array = np.array(image_resized) / 255.0
    image_input = np.expand_dims(image_array, axis=-1)  # Add channel dimension
    image_input = np.expand_dims(image_input, axis=0)   # Add batch dimension

    
    # Perform inference
    # results = model.predict(image)
    # Perform inference
    results = model.predict(image_input)
    predicted_class = np.argmax(results)
    probability = results[0][predicted_class]  # Probability of the predicted class

    # Determine the classification result
    if predicted_class == 1:
        result = "Malignant"
    else:
        result = "Benign"

    return result, probability
    # Process the results (this will depend on the output format of your model)
    # Here we assume it returns a list of probabilities for each class
    # result = "Malignant" if np.argmax(results) == 1 else "Benign"
    
    # return result