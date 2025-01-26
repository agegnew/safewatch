# Emergency Detection System MVP

## Overview

This is the Minimum Viable Product (MVP) for our **Emergency Detection System**, focusing on fire detection. The system uses machine learning to analyze video streams or live camera feeds to detect fire occurrences. Once a fire is detected, the system sends the information to the SambaNova API for further processing and displays the results.

While this MVP is limited to fire detection, it has the potential to be expanded into a comprehensive emergency detection system capable of identifying other hazards like smoke or gas leaks.

---

## System Information

- **Python Version**: 3.10.9
- **OpenAI Library Version**: 0.28.0

---

## How to Use

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-repo/emergency-detection.git
   ```


2. Navigate to the repository directory:
   ```bash
   cd <folder name>
   ```

3. Clone the submodules:
   ```bash
   git submodule update --init --recursive
   ```

4. Use the commands listed below to execute the desired functionality. install any modules that is not installed on your machine if there is any error please.

---

## Bash Executable Commands

### 1. **Detect Fire with Video Feed and Alerts**
```bash
py test3.py
```
- **Description**: Analyzes a video for fire detection and displays the video feed in real time.
- **Functionality**:
  - Detects fire occurrences in the video.
  - Displays the video while processing.
  - Shows an alert after receiving the response from SambaNova API.

---

### 2. **Detect Fire Using Laptop Camera**
```bash
py cctvtest.py
```
- **Description**: Detects fire in real time using a laptop camera as input.
- **Functionality**:
  - Captures live video feed from the laptop camera.
  - Detects fire and sends results to SambaNova API.
  - Shows an alert if the fire detection is accurate.

---

### 3. **Detect Fire from Video and Display Result**
```bash
py test2.py
```
- **Description**: Analyzes a video file to detect fire occurrences.
- **Functionality**:
  - Processes the video.
  - Sends fire detection results to SambaNova API.
  - Displays the detection result.

---

### 4. **Run the Website Platform**
```bash
cd server
py server.py
```
- **Description**: Starts the web-based platform for fire detection.
- **Functionality**:
  - Launches a website interface for fire detection.
  - Provides an alternative user-friendly way to interact with the system.

---

## Future Scope

The current system is focused solely on fire detection. In the future, we plan to:
- Extend detection capabilities to identify other emergencies like smoke, gas leaks, and more.
- Integrate advanced AI models for higher accuracy.
- Support additional hardware and platforms for broader usability.

---

Stay tuned for updates as we expand the system's capabilities!

