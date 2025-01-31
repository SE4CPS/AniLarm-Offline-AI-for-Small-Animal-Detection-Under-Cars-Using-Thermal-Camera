import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input

# Load the model
model_path = r".\efficientnet_animal_detector_v2.h5" #please keep your file path where the model from my google drive is downloaded to your PC
model = load_model(model_path)

# Function to preprocess image
def preprocess_image(img_path):
    img = load_img(img_path, target_size=(224, 224))  
    img_array = img_to_array(img)                     
    img_array = np.expand_dims(img_array, axis=0)     
    img_array = preprocess_input(img_array)           
    return img_array

# Function to compute Integrated Gradients
def integrated_gradients(model, image, target_class_index, steps=50, baseline=None):
    """ Computes Integrated Gradients for the given image """
    if baseline is None:
        baseline = tf.zeros_like(image)  

    # Generate interpolated images
    interpolated_images = tf.stack([
        baseline + (float(i) / steps) * (image - baseline)
        for i in range(steps + 1)
    ], axis=0) 

    interpolated_images = tf.squeeze(interpolated_images, axis=1)  

    with tf.GradientTape() as tape:
        tape.watch(interpolated_images)
        preds = model(interpolated_images)
        target_preds = preds[:, target_class_index]

    grads = tape.gradient(target_preds, interpolated_images)
    avg_grads = tf.reduce_mean(grads, axis=0)
    integrated_grad = (image - baseline) * avg_grads

    return integrated_grad.numpy()  
# Load and preprocess the image
img_path = "final test.jpg"
img_array = preprocess_image(img_path)

# Predict the class
prediction = model.predict(img_array)
predicted_class = 0 if prediction[0] < 0.5 else 1  
result = "Animal detected" if predicted_class == 0 else "No Animal detected"
print(f"Prediction: {result}")

# Compute Integrated Gradients
integrated_grads = integrated_gradients(model, img_array, target_class_index=predicted_class)

# Normalize attributions for visualization
attributions = np.abs(integrated_grads[0])
attributions /= np.ptp(attributions)  
# Convert grayscale attributions to heatmap
heatmap = cv2.applyColorMap(np.uint8(255 * attributions), cv2.COLORMAP_JET)

# Load original image
original_image = cv2.imread(img_path)
original_image = cv2.resize(original_image, (224, 224))

# Overlay heatmap on image
overlay = cv2.addWeighted(original_image, 0.6, heatmap, 0.4, 0)

# Display images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))  
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))  
plt.title("Integrated Gradients Attribution")
plt.axis("off")

plt.show()