import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from lime import lime_image
from skimage.segmentation import mark_boundaries

# Load the model
model_path = r".\efficientnet_animal_detector_v2.h5" #please keep your file path where the model from my google drive is downloaded to your PC
model = load_model(model_path)

# Function to preprocess image
def preprocess_image(img_path):
    img = load_img(img_path, target_size=(224, 224))  
    img_array = img_to_array(img) / 255.0  
    return img_array

# Function to predict class probabilities for LIME
def predict_fn(images):
    images = np.array([preprocess_input(img) for img in images])  
    return model.predict(images)

# Load and preprocess the image
img_path = "final test.jpg"
original_img = preprocess_image(img_path)  

# Create LIME explainer
explainer = lime_image.LimeImageExplainer()

# Run LIME explanation
explanation = explainer.explain_instance(
    original_img.astype('double'),  
    predict_fn,  
    top_labels=1, 
    hide_color=0,  
    num_samples=1000  
)

# Get the superpixels contributing to the classification
temp, mask = explanation.get_image_and_mask(
    explanation.top_labels[0], positive_only=True, num_features=10, hide_rest=False
)

# Convert mask to visualization
highlighted_image = mark_boundaries(temp, mask)

# Display results
plt.figure(figsize=(10, 5))

# Original Image
plt.subplot(1, 2, 1)
plt.imshow(original_img)
plt.title("Original Image")
plt.axis("off")

# LIME Explanation
plt.subplot(1, 2, 2)
plt.imshow(highlighted_image)
plt.title("LIME Explanation - Important Regions")
plt.axis("off")

plt.show()