# AniLarm: Obstacle Detection Under the Vehicle

## Introduction

AniLarm is an innovative solution designed to detect small animals hiding under vehicles using thermal imaging and machine learning. The system leverages the power of the Seek Thermal Camera and the Raspberry Pi to provide accurate and reliable detection results. By integrating an offline GUI application and an online Flask-based web application, AniLarm offers flexibility and accessibility for various use cases, ensuring urban safety and animal welfare.

---

## Features

### **Offline Application**

- Runs entirely on the Raspberry Pi without requiring internet connectivity.
- GUI-based interface for real-time detection results.
- Provides auditory alerts using a Bluetooth speaker.
- Ensures secure data handling with AES-256 encryption for thermal images.

### **Online Flask Application**

- Web-based interface accessible via a browser on the same local network.
- Allows users to trigger image capture and view detection results.
- Supports multiple image processing in a single session.

---

## Setup

### **For Offline Application (finap.py)**

1. **Prerequisites**:

   - Raspberry Pi 4 Model B with Raspbian OS installed.
   - Seek Thermal Camera.
   - Python 3.11 or later.
   - Install required dependencies:
     ```bash
     pip install tensorflow pycryptodome opencv-python pillow espeak
     ```

2. **Steps**:
   - Clone the repository:
     ```bash
     git clone https://github.com/SE4CPS/Obstacle-detection-under-the-vehicle.git
     cd Obstacle-detection-under-the-vehicle/offline
     ```
   - Run the application:
     ```bash
     python3 finap.py
     ```

### **For Online Flask Application (web_trigger.py and detect.py)**

1. **Prerequisites**:

   - Flask installed on the Raspberry Pi:
     ```bash
     pip install flask tensorflow opencv-python pillow
     ```

2. **Steps**:
   - Navigate to the `online` directory:
     ```bash
     cd Obstacle-detection-under-the-vehicle/online
     ```
   - Start the Flask server:
     ```bash
     python3 web_trigger.py
     ```
   - Access the web interface from any device on the same network:
     ```
     http://<raspberry_pi_ip>:5000
     ```

---

## How It Works

1. **Capture Images**:

   - The Seek Thermal Camera captures thermal images of the area under a vehicle.

2. **Image Encryption (Offline Application)**:

   - Images are encrypted using AES-256 for secure storage and decrypted only during inference.

3. **Model Inference**:

   - The EfficientNet model processes images to classify them as containing an animal or not.

4. **Result Display**:
   - **Offline**: Results are displayed on the GUI and announced via a Bluetooth speaker.
   - **Online**: Results are displayed on the web interface with processed images.

### Architecture Diagram(workflow)

![Architecture Diagram](docs/images/Architecture%20Diagram.jpg)

---

## Technologies Used

- **Python**: Core programming language for the application.
- **TensorFlow**: Deep learning framework used for EfficientNet model inference.
- **AES Encryption**: Ensures secure storage and processing of thermal images.
- **Flask**: Web framework for the online application.
- **Raspberry Pi**: Hardware platform for deployment.
- **Seek Thermal Camera**: Captures thermal images for animal detection.

---

## Future Enhancements

- **Improved Dataset**: Add more diversity to the dataset for better generalization.
- **Automated Updates**: Incorporate cryptographic hash verification for firmware updates.
- **Extended Applications**: Adapt the system for wildlife monitoring and industrial safety.

---

For more details, refer to the [Documentation](docs/documentation.md).
