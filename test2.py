import os
import base64
import openai
from ultralytics import YOLO
import cv2

# Set up OpenAI API key and base URL
openai.api_key = "0245a6ef-96a6-4314-9b02-bff7f89ef985"
openai.api_base = "https://api.sambanova.ai/v1"

# YOLO model setup
model_path = "./AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"
video_source = "./AIMODELS/YOLOv8-Fire-and-Smoke-Detection/fire.mp4"
detection_threshold = 0.5
required_detections = 3  # Fire must be detected for at least 3 frames
consecutive_count = 0

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

    frame_count = 0
    last_frame = None

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
        except Exception as e:
            print(f"Error during prediction: {e}")
            break

        # Validate fire detection
        fire_detected = False
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                confidence = box.conf[0]
                cls = results[0].names[int(box.cls[0])]
                print(f"Detected: {cls} with confidence {confidence:.2f}")

                if cls == "Fire" and confidence > detection_threshold:
                    fire_detected = True
                    last_frame = frame  # Save the frame with the detection

        if fire_detected:
            consecutive_count += 1
            print(f"Consecutive fire detections: {consecutive_count}")
        else:
            consecutive_count = 0

        # Trigger if fire is detected for required frames
        if consecutive_count >= required_detections:
            print("Fire hazard detected. Sending to SambaNova.")
            image_path = "detected_fire_frame.jpg"
            cv2.imwrite(image_path, last_frame)
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
                {"type": "text", "text": "This is a fire-detected image. Please evaluate the accuracy of this detection and assess how dangerous it is. Respond in the format:\n\nhazard: \"fire\"\nlevel: \"<risk-level>\" (e.g., false alarm, minor fire, major fire)."},
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
        # Parse and format the response
        result = response["choices"][0]["message"]["content"]
        print("SambaNova Response:")
        print(result)
    except Exception as e:
        print(f"Error occurred while sending to SambaNova: {e}")

# Main execution
if __name__ == "__main__":
    detect_fire()
