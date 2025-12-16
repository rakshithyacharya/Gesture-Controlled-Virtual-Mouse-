# Gesture-Controlled-Virtual-Mouse-
my discriptions
1. Hardware Requirements
Webcam: An external USB webcam or a built-in laptop camera is essential to capture the video feed.

Processor (CPU): A standard modern processor (Intel i3/i5 or AMD equivalent) is sufficient. MediaPipe is optimized to be lightweight, but a decent CPU ensures smooth performance without lag.

RAM: Minimum 4GB (8GB recommended) to run the operating system, Python environment, and image processing smoothly.

2. Software Requirements
Operating System: Windows, macOS, or Linux (The project is cross-platform, though pyautogui works best on Windows/macOS).

Programming Language: Python (Version 3.7 or higher recommended).

IDE / Code Editor: PyCharm, VS Code, or any Python-compatible editor.

3. Python Library Requirements
These are the specific packages you installed. If you were creating a requirements.txt file for this project, it would contain:

opencv-python: For image processing and accessing the camera.

mediapipe: For hand tracking and landmark detection.

pyautogui: For controlling the mouse cursor and click events.

numpy (Usually installed automatically with OpenCV, used for math operations).

4. Functional Requirements (What the system must do)
Hand Detection: The system must detect a human hand in the video frame in real-time.

Landmark Tracking: The system must accurately identify the tip of the Index Finger (ID 8) and Thumb (ID 4).

Cursor Mapping: The system must map the coordinates of the index finger from the camera frame to the computer screen resolution.

Click Action: The system must trigger a mouse click when the distance between the thumb and index finger falls below a specific threshold (e.g., 35 pixels).
