# AniLarm: Obstacle Detection Under the Vehicle

## Table of Contents

1. [System Architecture](#system-architecture)
2. [AES-256 Encryption Explanation](#aes-256-encryption-explanation)
3. [Dataset Preparation](#dataset-preparation)
4. [Hardware Setup](#hardware-setup)
5. [Example Outputs](#example-outputs)

---

## System Architecture

AniLarm combines hardware and software components to detect small animals under vehicles using thermal imaging and machine learning.

### Key Components:

1. **Seek Thermal Camera**: Captures thermal images of the area under a vehicle.
2. **Raspberry Pi 4 Model B**: Serves as the processing unit, running the machine learning model and handling encrypted image storage.
3. **EfficientNet Model**: Pre-trained on animal and non-animal thermal images for classification.
4. **GUI and Flask Application**: Provides an offline GUI (`finap.py`) and an online web interface (`web_trigger.py`).

### Workflow:

1. Thermal images are captured using the Seek Thermal Camera.
2. Images are encrypted using AES-256 immediately after capture.
3. Decrypted images are processed by the EfficientNet model for classification.
4. Detection results are displayed on the GUI or the Flask web application, with auditory alerts provided via `espeak`.

---

## AES-256 Encryption Explanation

### Why AES-256?

- AES-256 (Advanced Encryption Standard with a 256-bit key) ensures that sensitive thermal images are securely stored and processed, preventing unauthorized access.

### How It Works:

1. **Key Generation**:

   - A 256-bit key is generated and stored securely in a local file (`encryption.key`).
   - The key is not hardcoded into the script for added security.

2. **Encryption**:

   - Each captured image is encrypted using the key and stored with a `.enc` extension.
   - This process uses the CBC (Cipher Block Chaining) mode for added security.

3. **Decryption**:
   - Images are decrypted just before processing and immediately removed after use.

### Code Snippet:

- The encryption and decryption functions are implemented in `finap.py`.

---

## Dataset Preparation

### Dataset Description:

1. **Animal Images**:
   - Captured using the Seek Thermal Camera.
   - Includes thermal images of cats, dogs, and other small animals.
2. **No Animal Images**:
   - Frames without animals to train the model for non-animal detection.

### Data Split:

- **Training Set**: 70% of the dataset for model training.
- **Validation Set**: 20% for model optimization.
- **Test Set**: 10% for evaluating model accuracy.

### Preprocessing:

- Images are resized to `224x224` pixels.
- Normalized to a range of `[-1, 1]` for EfficientNet compatibility.

---

## Hardware Setup

### Components:

1. **Raspberry Pi 4 Model B**:
   - Acts as the processing unit for both offline and online applications.
2. **Seek Thermal Camera**:
   - Captures thermal images for analysis.
3. **Bluetooth Speaker**:
   - Provides auditory alerts for detection results.
4. **Monitor**:
   - Displays the GUI application in offline mode.

### Connection Guide:

1. Connect the Seek Thermal Camera to the Raspberry Pi via USB.
2. Pair the Bluetooth speaker to the Raspberry Pi for auditory feedback.
3. Attach a monitor to the Raspberry Pi for GUI display.

---

## Example Outputs

### Offline Application:

- **Input**: A thermal image captured under a car.
- **Output**: Detection results displayed on the GUI with an auditory alert.
  - Example:
    ```
    Living Presence Detected in color_output_0.png
    No Living Presence Detected in color_output_1.png
    ```

### Online Application:

- **Input**: Thermal images captured via the Flask interface.
- **Output**: Detection results shown on the web interface.
  - Example:
    ```
    Living Presence Detected in color_output_0.png
    ```

### Accuracy:

- The EfficientNet model achieves a test accuracy of **97.83%** with a macro average F1-score of **0.98**.

---

## Future Enhancements

1. **Automated Secure Updates**:
   - Add cryptographic hash verification for software updates.
2. **Advanced Cybersecurity Features**:
   - Integrate intrusion detection systems and watchdog timers.
3. **Improved Dataset Diversity**:
   - Expand the dataset to include various animal species and environments.

---

For more details, refer to the [GitHub Repository](https://github.com/SE4CPS/Obstacle-detection-under-the-vehicle).
