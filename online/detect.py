import os
import time
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
import cv2  

# Load the EfficientNet model
model_path = "/home/animal/libseek-thermal/build/examples/efficientnet_animal_detector_v2.h5" #change this path according to your model location, as it is my model location where i had put it on raspberry pi.
model = load_model(model_path)

def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))  
    img_array = np.array(img, dtype=np.float32)  
    img_array = np.expand_dims(img_array, axis=0)  
    img_array = (img_array - 127.5) / 127.5  
    return img_array

def detect_animal(image_path):
    img_array = preprocess_image(image_path)
    prediction = model.predict(img_array)[0][0]  

    if prediction < 0.5:
        os.system('espeak "Living Presence detected"')
        return f"Living Presence Detected in {image_path}"
    else:
        os.system('espeak "No Living Presence detected"')
        return f"No Living Presence Detected in {image_path}"

def apply_color_map(image_path):
    grayscale_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    colorized_img = cv2.applyColorMap(grayscale_img, cv2.COLORMAP_JET)
    color_image_path = f"color_{os.path.basename(image_path)}"  
    cv2.imwrite(color_image_path, colorized_img)
    return color_image_path

def main(image_paths):
    results = []
    for image_path in image_paths:
        if not os.path.exists(image_path):
            results.append(f"Image {image_path} not found.")
            continue
        color_image_path = apply_color_map(image_path)  
        detection_result = detect_animal(color_image_path)  
        results.append(detection_result)
    return "\n".join(results)

if __name__ == "__main__":
    import sys
    image_paths = sys.argv[1:]
    if not image_paths:
        print("No images provided for detection.")
        sys.exit(1)
    print(main(image_paths))
