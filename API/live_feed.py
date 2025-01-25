import cv2
import depthai as dai
from fastapi import APIRouter, HTTPException
from ultralytics import YOLO
import threading

router = APIRouter()

# Load the YOLOv8 model (fire detection model)
model = YOLO('AIMODELS\Accident-Detection-Model/runs/detect/train/weights/best.pt')  # Replace with the actual model path

# Global variables to store frames
output_frame = None
lock = threading.Lock()


def process_laptop_camera():
    """
    Capture frames from the laptop's built-in camera and process them with YOLOv8.
    """
    global output_frame, lock
    cap = cv2.VideoCapture(0)  # Laptop camera

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        # Perform fire detection
        results = model(frame)

        # Annotate detections
        annotated_frame = results[0].plot()

        # Save the processed frame
        with lock:
            output_frame = annotated_frame

    cap.release()


def process_depthai_camera():
    """
    Capture frames from the DepthAI camera and process them with YOLOv8.
    """
    global output_frame, lock

    # Create DepthAI pipeline
    pipeline = dai.Pipeline()

    # Define camera source and output
    cam_rgb = pipeline.create(dai.node.ColorCamera)
    xout_video = pipeline.create(dai.node.XLinkOut)
    xout_video.setStreamName("video")

    # Camera properties
    cam_rgb.setBoardSocket(dai.CameraBoardSocket.RGB)
    cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    cam_rgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

    # Link camera output
    cam_rgb.video.link(xout_video.input)

    with dai.Device(pipeline) as device:
        video_queue = device.getOutputQueue('video')

        while True:
            video_frame = video_queue.get()
            frame = video_frame.getCvFrame()

            # Perform fire detection
            results = model(frame)

            # Annotate detections
            annotated_frame = results[0].plot()

            # Save the processed frame
            with lock:
                output_frame = annotated_frame


@router.get("/api/live-feed/{camera_number}")
async def get_live_feed(camera_number: int):
    """
    Handle live feed based on the camera number provided in the URL path.
    """
    global output_frame, lock

    if camera_number == 1:
        # Start a thread for the laptop camera
        threading.Thread(target=process_laptop_camera, daemon=True).start()
    elif camera_number == 2:
        # Start a thread for the DepthAI camera
        threading.Thread(target=process_depthai_camera, daemon=True).start()
    else:
        raise HTTPException(status_code=400, detail="Invalid camera selection")

    # Yield frames as MJPEG
    def generate():
        global output_frame, lock
        while True:
            with lock:
                if output_frame is None:
                    continue
                # Encode the frame as JPEG
                _, buffer = cv2.imencode('.jpg', output_frame)
                frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    return generate()
