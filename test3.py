import os
import base64
import openai
from ultralytics import YOLO
import cv2
import threading
import tkinter as tk

# Set up OpenAI API key and base URL
openai.api_key = "7c328a65-098f-49cb-9ac5-54139bcb7288"
openai.api_base = "https://api.sambanova.ai/v1"

# YOLO model setup
model_path = "./AIMODELS/YOLOv8-Fire-and-Smoke-Detection/runs/detect/train/weights/best.pt"
video_source = "./AIMODELS/YOLOv8-Fire-and-Smoke-Detection/fire.mp4"
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

# GUI Notification for Fire Hazard
def show_notification():
    def close_alert():
        window.destroy()
        global alert_triggered
        alert_triggered = False

    window = tk.Tk()
    window.title("Fire Alert")
    window.geometry("800x600")
    window.configure(bg="red")
    window.attributes("-topmost", True)  # Ensure window is always on top

    label = tk.Label(window, text="FIRE HAZARD DETECTED!", bg="red", fg="white", font=("Helvetica", 24, "bold"))
    label.pack(pady=20)

    def blink():
        while alert_triggered:
            current_color = label.cget("bg")
            new_color = "white" if current_color == "red" else "red"
            label.configure(bg=new_color)
            window.configure(bg=new_color)
            window.update()
            window.after(500)

    blink_thread = threading.Thread(target=blink, daemon=True)
    blink_thread.start()

    button = tk.Button(window, text="Dismiss", command=close_alert, font=("Helvetica", 14))
    button.pack(pady=10)

    window.mainloop()

# Play video and process detection
def play_video_with_detection(video: str):
    global consecutive_count, alert_triggered
    cap = cv2.VideoCapture(video)
    if not cap.isOpened():
        print("Error: Cannot open video source.")
        return

    frame_count = 0
    last_frame = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Restarting video...")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video
            continue

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
                if cls == "Fire" and confidence > detection_threshold:
                    fire_detected = True
                    last_frame = frame

        if fire_detected:
            consecutive_count += 1
        else:
            consecutive_count = 0

        # Trigger if fire is detected for required frames
        if consecutive_count >= required_detections and not alert_triggered:
            print("Fire hazard detected. Sending to SambaNova.")
            image_path = "detected_fire_frame.jpg"
            cv2.imwrite(image_path, last_frame)
            response = send_to_sambanova(image_path)

            if "hazard: \"fire\"" in response.lower() and "level: " in response.lower():
                alert_triggered = True
                notification_thread = threading.Thread(target=show_notification, daemon=True)
                notification_thread.start()
            else:
                print("False alarm or undetermined risk level. Continuing detection.")

        # Overlay red border if alert is triggered
        if alert_triggered:
            frame = cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 0, 255), 50)

        cv2.imshow("Fire Detection - Video Feed", frame)

        if cv2.waitKey(30) & 0xFF == ord("q"):  # Press 'q' to stop
            break

    cap.release()
    cv2.destroyAllWindows()

# Send image to SambaNova
def send_to_sambanova(image_path):
    print(f"Preparing to send image at {image_path} to SambaNova.")
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}. Please provide a valid file.")
        return "Error: Image not found"

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Define the payload
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "This is a fire-detected image. Please evaluate the accuracy of this detection and assess how dangerous it is. Respond ONLY in this format:\n\nhazard: \"fire\"\nlevel: \"<risk-level>\" (e.g., false alarm, minor fire, major fire). No other text or explanations are needed."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}    
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
        result = response["choices"][0]["message"]["content"]
        print("SambaNova Response:")
        print(result)
        return result
    except Exception as e:
        print(f"Error occurred while sending to SambaNova: {e}")
        return "Error: Unable to process request"

# Main execution
if __name__ == "__main__":
    play_video_with_detection(video_source)
