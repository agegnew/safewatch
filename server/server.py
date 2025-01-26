from flask import Flask, request, render_template, jsonify, Response
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import cv2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv'}

# YOLO model setup
model_path = "../AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"
detection_threshold = 0.5

try:
    print(f"Loading YOLO model from {model_path}...")
    yolo_model = YOLO(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit()

# Helper function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to render the homepage
@app.route("/", methods=["GET", "POST"])
def upload_and_play():
    if request.method == "POST":
        if "video" not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files["video"]
        if file.filename == "":
            return jsonify({"error": "No selected file"})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)
            return jsonify({"filename": filename, "video_url": f"/uploads/{filename}"})

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)

# Route to process and stream the video with YOLO
@app.route("/process/<filename>")
def process_video(filename):
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    def generate():
        cap = cv2.VideoCapture(filepath)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # YOLO model inference
            results = yolo_model.predict(frame, conf=detection_threshold, verbose=False)
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                cls = results[0].names[int(box.cls[0])]
                if cls == "Fire" and confidence > detection_threshold:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, f"{cls} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Encode frame as JPEG
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

        cap.release()

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

# Route to serve uploaded video files
@app.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    return Response(open(os.path.join(app.config["UPLOAD_FOLDER"], filename), "rb"), mimetype="video/mp4")

# Route to display the stored videos page
@app.route("/stored_videos")
def get_stored_videos():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("stored_videos.html", files=files)





# @app.route("/stored_videos")
# def get_stored_videos():
#     files = os.listdir(app.config["UPLOAD_FOLDER"])
#     return render_template("stored_videos.html", files=files, sambanova_response=sambanova_response)





# @app.route("/stored_videos")
# def get_stored_videos():
#     files = os.listdir(app.config["UPLOAD_FOLDER"])
#     return render_template("stored_videos.html", files=files, sambanova_response=sambanova_response)


@app.route("/live-feed")
def get_live_feed():
    return render_template("live-feed.html")  # Replace with your actual implementation when ready


@app.route("/emergency-counts")
def get_emergency_counts():
    return render_template("emergency-counts.html")  # Adjust based on your actual implementation


@app.route("/live-camera")
def live_camera_feed():
    def generate():
        cap = cv2.VideoCapture(0)  # Use 0 for the default laptop webcam
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # YOLO model inference
            results = yolo_model.predict(frame, conf=detection_threshold, verbose=False)
            for box in results[0].boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = box.conf[0]
                cls = results[0].names[int(box.cls[0])]

                if cls == "Fire" and confidence > detection_threshold:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(frame, f"{cls} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()

            yield (b"--frame\r\n"
                   b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

        cap.release()

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")



if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)