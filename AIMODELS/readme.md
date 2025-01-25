# Fire and Smoke Detection using YOLOv8

## Requirements

1. **Python**: Make sure you have Python 3.10 installed.
2. **Dependencies**:
   - Install the required dependencies:

     pip install ultralytics

## How to Run the Fire and Smoke Detection

### 1. **Trained Model**
   - Ensure the trained model is available in the `runs/detect/train/weights/` directory.
   - The trained model files are:
     - `best.pt`: The best-performing model from training.
     - `last.pt`: The final model after training.

---

### 2. **Run Detection on Images**
   - Use the following command to detect fire and smoke in a single image:

     yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=<path_to_image>

     Replace `<path_to_image>` with the path to your image file (e.g., `fire3.jpg`).

---

### 3. **Run Detection on Video Files**
   - To process a video file for fire and smoke detection:

     yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=<path_to_video>

     Replace `<path_to_video>` with the path to your video file (e.g., `fire4.mp4`).

---

### 4. **Real-Time Detection with CCTV/Camera**
   - For real-time detection from a webcam or CCTV feed:

     yolo task=detect mode=predict model=runs/detect/train/weights/best.pt source=0

     - Replace `0` with the appropriate device index or RTSP/HTTP stream URL for your CCTV.

