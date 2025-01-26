# from urllib import request
# import os
# import flask
# from flask import request, redirect, url_for, render_template
# #import test3
# from werkzeug.utils import secure_filename
#
#
# app = flask.Flask(__name__)
#
#
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv'}
#
# def check_video_format(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route("/")
# def get_home_page():
#     return flask.render_template("index.html")
#
#
# @app.route("/stored-videos", methods=['GET', 'POST'])
# def get_stored_videos():
#     if request.method == 'POST':
#         if 'video' not in request.files:
#             return 'No file part'
#         file = request.files['video']
#
#         if file.filename == '':
#             return 'No selected file'
#
#         # Если файл корректен, сохраняем его
#         if file and check_video_format(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('get_stored_videos'))
#
#     # Отображаем страницу с видео
#     return render_template("stored_videos.html")
#
# # @app.route("/stored-videos")
# # def get_stored_video(video_id):
# #     test3.play_video_with_detection()
#
#
#
# app.run(host="0.0.0.0", port=5000)

# import os
# import base64
# import openai
# from ultralytics import YOLO
# import cv2
# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import threading
#
# # Flask app setup
# app = Flask(__name__)
#
# # State for fire alert
# alert_triggered = False
#
# # YOLO model setup
# model_path = "../AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"
# detection_threshold = 0.5
# required_detections = 3
# consecutive_count = 0
#
# # Load YOLO model
# try:
#     print(f"Loading YOLO model from {model_path}...")
#     yolo_model = YOLO(model_path)
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading YOLO model: {e}")
#     exit()
#
# @app.route("/")
# def get_home_page():
#     return render_template("index.html")
#
# @app.route("/stored-videos", methods=['GET', 'POST'])
# def get_stored_videos():
#     if request.method == 'POST':
#         file = request.files['video']
#         if file:
#             filename = os.path.join("uploads", file.filename)
#             file.save(filename)
#             # Start video processing in a new thread
#             threading.Thread(target=process_video, args=(filename,), daemon=True).start()
#             return redirect("/stored-videos")
#     return render_template("stored_videos.html")
#
# @app.route("/alert-status")
# def alert_status():
#     return jsonify({"alert_triggered": alert_triggered})
#
# def process_video(video_path):
#     global consecutive_count, alert_triggered
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("Error: Cannot open video.")
#         return
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         try:
#             results = yolo_model.predict(frame, conf=detection_threshold, verbose=False)
#         except Exception as e:
#             print(f"Error during prediction: {e}")
#             break
#
#         fire_detected = False
#         if len(results[0].boxes) > 0:
#             for box in results[0].boxes:
#                 if results[0].names[int(box.cls[0])] == "Fire" and box.conf[0] > detection_threshold:
#                     fire_detected = True
#                     break
#
#         if fire_detected:
#             consecutive_count += 1
#         else:
#             consecutive_count = 0
#
#         if consecutive_count >= required_detections:
#             alert_triggered = True
#             break
#
#     cap.release()
#
# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, redirect, url_for, render_template, flash
# import os
# import base64
# import openai
# from werkzeug.utils import secure_filename
# from ultralytics import YOLO
# import cv2
#
# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Это необходимо для работы flash сообщений
#
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv'}
#
# # YOLO model setup
# model_path = "../AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"
# detection_threshold = 0.5
# required_detections = 3  # Fire must be detected for at least 3 frames
# consecutive_count = 0
# alert_triggered = False
#
# # Load YOLO model
# try:
#     print(f"Loading YOLO model from {model_path}...")
#     yolo_model = YOLO(model_path)
#     print("Model loaded successfully.")
# except Exception as e:
#     print(f"Error loading YOLO model: {e}")
#     exit()
#
# # Function to detect fire
# def detect_fire(video_path):
#     global consecutive_count, alert_triggered
#     cap = cv2.VideoCapture(video_path)
#     if not cap.isOpened():
#         print("Error: Cannot open video source.")
#         return
#
#     frame_count = 0
#     last_frame = None
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         frame_count += 1
#         results = yolo_model.predict(frame, conf=detection_threshold, verbose=False)
#
#         # Validate fire detection
#         fire_detected = False
#         if len(results[0].boxes) > 0:
#             for box in results[0].boxes:
#                 confidence = box.conf[0]
#                 cls = results[0].names[int(box.cls[0])]
#                 if cls == "Fire" and confidence > detection_threshold:
#                     fire_detected = True
#                     last_frame = frame
#
#         if fire_detected:
#             consecutive_count += 1
#         else:
#             consecutive_count = 0
#
#         if consecutive_count >= required_detections and not alert_triggered:
#             # Fire detected, trigger alert
#             alert_triggered = True
#             flash('🔥 FIRE HAZARD DETECTED! 🚨', 'danger')  # Flask flash message
#             break
#
#     cap.release()
#
# # Route to handle video upload and detection
# @app.route("/", methods=['GET', 'POST'])
# def get_home_page():
#     if request.method == 'POST':
#         if 'video' not in request.files:
#             return 'No file part'
#         file = request.files['video']
#
#         if file.filename == '':
#             return 'No selected file'
#
#         if file and check_video_format(file.filename):
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
#
#             # Run the fire detection logic
#             detect_fire(file_path)
#             return redirect(url_for('get_home_page'))
#
#     return render_template("index.html")
#
# @app.route("/stored_videos")
# def get_stored_videos():
#     # Код для отображения сохраненных видео
#     return render_template("stored_videos.html")
#
#
# # Helper function to check video format
# def check_video_format(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
import os
import base64
import openai
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Это необходимо для работы flash сообщений

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv'}

# YOLO model setup
model_path = "../AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"
detection_threshold = 0.5
required_detections = 3  # Fire must be detected for at least 3 frames
consecutive_count = 0
alert_triggered = False

# Load YOLO model
try:
    print(f"Loading YOLO model from {model_path}...")
    yolo_model = YOLO(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit()

# Function to detect fire
def detect_fire(video_path):
    global consecutive_count, alert_triggered
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video source.")
        return

    frame_count = 0
    last_frame = None
    fire_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        results = yolo_model.predict(frame, conf=detection_threshold, verbose=False)

        # Validate fire detection
        fire_detected = False
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                confidence = box.conf[0]
                cls = results[0].names[int(box.cls[0])]
                if cls == "Fire" and confidence > detection_threshold:
                    fire_detected = True
                    last_frame = frame

        if fire_detected:
            consecutive_count += 1
        else:
            consecutive_count = 0

        if consecutive_count >= required_detections and not alert_triggered:
            # Fire detected, trigger alert
            alert_triggered = True
            return 'fire_detected'  # Returning the alert response directly

    cap.release()

    if not fire_detected:
        return 'no_fire_detected'  # No fire detected in the video

# Route to handle video upload and detection
@app.route("/", methods=['GET', 'POST'])
def get_home_page():
    if request.method == 'POST':
        if 'video' not in request.files:
            return 'No file part'
        file = request.files['video']

        if file.filename == '':
            return 'No selected file'

        if file and check_video_format(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Run the fire detection logic
            result = detect_fire(file_path)
            if result == 'fire_detected':
                flash('🔥 FIRE HAZARD DETECTED! 🚨', 'danger')
            elif result == 'no_fire_detected':
                flash('No fire detected in this video.', 'info')

            return jsonify({'result': result})

    return render_template("index.html")

@app.route("/stored_videos")
def get_stored_videos():
    return render_template("stored_videos.html")



@app.route("/live-feed")
def get_live_feed():
    return render_template("live-feed.html")

@app.route("/emergency-counts")
def get_emergency_counts():
        return render_template("emergency-counts.html")





# Helper function to check video format
def check_video_format(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)
