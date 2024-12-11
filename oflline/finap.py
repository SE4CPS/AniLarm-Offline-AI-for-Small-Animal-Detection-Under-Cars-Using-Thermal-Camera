import subprocess
import os
import time
from PIL import Image, ImageTk
import cv2  # OpenCV for color grading
import tkinter as tk
from tkinter import scrolledtext, Label, Frame
from threading import Thread
import numpy as np
from tensorflow.keras.models import load_model
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Load the `.h5` model
model_path = "/home/animal/libseek-thermal/build/examples/efficientnet_animal_detector_v2.h5" #change this path according to your model location, as it is my model location where i had put it on raspberry pi.
model = load_model(model_path)

# Encryption setup
key_file = "encryption.key"
if not os.path.exists(key_file):
    with open(key_file, "wb") as kf:
        kf.write(get_random_bytes(32)) 

with open(key_file, "rb") as kf:
    encryption_key = kf.read()
    
# Encryption function
def encrypt_file(file_path):
    cipher = AES.new(encryption_key, AES.MODE_CBC)
    with open(file_path, "rb") as f:
        data = f.read()
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    encrypted_file_path = f"{file_path}.enc"
    with open(encrypted_file_path, "wb") as ef:
        ef.write(iv + encrypted_data)
    os.remove(file_path) 
    return encrypted_file_path

# Decryption function
def decrypt_file(file_path):
    with open(file_path, "rb") as ef:
        iv = ef.read(16)
        encrypted_data = ef.read()
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    decrypted_file_path = file_path.replace(".enc", "")
    with open(decrypted_file_path, "wb") as df:
        df.write(data)
    return decrypted_file_path


def preprocess_image(image_path):
    img = Image.open(image_path).resize((224, 224))  
    img_array = np.array(img, dtype=np.float32)  
    img_array = np.expand_dims(img_array, axis=0)  
    img_array = (img_array - 127.5) / 127.5  
    return img_array
# Run inference using the `.h5` model
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


def run_detection(app_textbox, image_label_left, image_label_right):
    try:
        viewer_process = subprocess.Popen(['sudo', './seek_viewer'])
        time.sleep(10)  

        viewer_process.terminate()
        captured_images = []
        start_time = time.time()
        image_count = 0

        while time.time() - start_time < 10:
            image_path = f"output_{image_count}.png"
            subprocess.run(['sudo', './seek_snapshot', '-o', image_path], check=True)
            encrypted_image_path = encrypt_file(image_path)  
            captured_images.append(encrypted_image_path)
            image_count += 1
            time.sleep(1)  

        for i, encrypted_image_path in enumerate(captured_images):
            decrypted_image_path = decrypt_file(encrypted_image_path)  

            if not os.path.exists(decrypted_image_path):
                app_textbox.insert(tk.END, f"Image {decrypted_image_path} not found.\n")
                continue

            color_image_path = apply_color_map(decrypted_image_path)  
            detection_result = detect_animal(color_image_path)  
            app_textbox.insert(tk.END, f"{detection_result}\n")

            color_image = Image.open(color_image_path)
            color_image = color_image.resize((150, 150))  
            photo = ImageTk.PhotoImage(color_image)
            if i % 2 == 0:
                image_label_left.config(image=photo)
                image_label_left.image = photo
            else:
                image_label_right.config(image=photo)
                image_label_right.image = photo

            os.remove(decrypted_image_path)  
            if os.path.exists(color_image_path):
                os.remove(color_image_path) 
    except Exception as e:
        app_textbox.insert(tk.END, f"Error occurred: {str(e)}\n")

# Main GUI Application
def main():
    app = tk.Tk()
    app.title("Animal Detection App")
    app.geometry("800x600")

    run_button = tk.Button(app, text="Run Animal Detection", command=lambda: Thread(target=run_detection, args=(result_textbox, result_image_label_left, result_image_label_right)).start())
    run_button.pack(pady=10)

    result_textbox = scrolledtext.ScrolledText(app, width=70, height=10, wrap=tk.WORD)
    result_textbox.pack(pady=10)

    image_frame = Frame(app)
    image_frame.pack(pady=10)

    result_image_label_left = Label(image_frame)
    result_image_label_left.pack(side=tk.LEFT, padx=5)

    result_image_label_right = Label(image_frame)
    result_image_label_right.pack(side=tk.RIGHT, padx=5)

    app.mainloop()

if __name__ == "__main__":
    main()
