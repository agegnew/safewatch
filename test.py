import os
import base64
import openai
from ultralytics import YOLO  # Install this if not done: pip install ultralytics
import cv2

# Set up OpenAI API key and base URL
openai.api_key = "0245a6ef-96a6-4314-9b02-bff7f89ef985"
openai.api_base = "https://api.sambanova.ai/v1"

# YOLO model setup
model_path = "./AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"  # Update if path changes
video_source = "./AIMODELS/YOLOv8-Fire-and-Smoke-Detection/fire.mp4"  # Replace with your video source
detection_threshold = 0.5  # Confidence threshold for fire detection
consecutive_detections = 10  # Number of detections required
detected_frames = []

# Load YOLO model
try:
    print(f"Loading YOLO model from {model_path}...")
    yolo_model = YOLO(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    exit()

# Process video and detect fire
def detect_fire():
    print(f"Opening video source: {video_source}...")
    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print("Error: Cannot open video source.")
        return

    detection_count = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or unable to read frame.")
            break

        frame_count += 1
        print(f"Processing frame {frame_count}...")

        # Run YOLO prediction on the frame
        try:
            results = yolo_model.predict(frame, conf=detection_threshold, verbose=False)
            print(f"Results for frame {frame_count}: {results}")
        except Exception as e:
            print(f"Error during prediction: {e}")
            break

        # Check for fire detection in results
        if len(results[0].boxes) > 0:  # If any detections
            detection_count += 1
            detected_frames.append(frame)

            print(f"Fire detected: {detection_count} detections so far.")
            
            # If required detections are reached
            if detection_count >= consecutive_detections:
                print(f"Required detections reached: {detection_count}. Sending to SambaNova.")
                # Save the frame to send to SambaNova
                image_path = "detected_fire_frame.jpg"
                cv2.imwrite(image_path, frame)
                send_to_sambanova(image_path)
                break

    cap.release()
    cv2.destroyAllWindows()

# Send image to SambaNova
def send_to_sambanova(image_path):
    print(f"Preparing to send image at {image_path} to SambaNova.")
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}. Please provide a valid file.")
        return

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Define the payload
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Do u see a fire on my parking this is a parking owned by me and this are camera recoreds."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }
    ]

    # Send the request
    try:
        print("Sending request to SambaNova...")
        response = openai.ChatCompletion.create(
            model="Llama-3.2-11B-Vision-Instruct",
            messages=messages,
            temperature=0.1,
            top_p=0.1,
        )
        # Print the response
        print("SambaNova Response:", response["choices"][0]["message"]["content"])
    except Exception as e:
        print(f"Error occurred while sending to SambaNova: {e}")

# Main execution
if __name__ == "__main__":
    detect_fire()
