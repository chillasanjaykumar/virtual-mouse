# 🖐️ Virtual Mouse Using Hand Gestures
This project allows users to control mouse actions using hand gestures captured via a webcam, eliminating the need for a physical mouse.

📌 Features
✅ Cursor Movement
✅ Left Click
✅ Right Click
✅ Double Click
✅ Scroll Up / Down
✅ Hold and Drag
✅ Zoom In / Out

🛠️ Technologies Used
Python
OpenCV – For image capture and processing
MediaPipe – For hand tracking and landmarks detection
Pynput, Mouse, PyAutoGUI – For simulating mouse and keyboard actions
NumPy – For coordinate mapping

📷 How It Works
Webcam captures real-time video.
MediaPipe detects hand and identifies 21 landmarks.
Gestures are recognized based on finger positions.
Each gesture is mapped to a specific mouse action.
Smooth cursor movement is handled using interpolation and averaging.

🔧 Requirements
Python 3.7+
Webcam
RAM: Minimum 2GB
Processor: i5 or equivalent

🔄 Installation
bash
pip install opencv-python mediapipe pynput numpy pyautogui mouse
▶️ Run the Project
bash
python thesis1.py
Make sure thesis2.py is in the same directory as thesis1.py
