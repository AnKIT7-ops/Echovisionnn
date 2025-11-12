# Configuration settings for the project
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update for your system
MODEL_PATH = "yolov8n.pt"  # YOLOv8n model for CPU testing

# Camera source can be:
# - an integer index (0, 1, 2, ...)
# - a video file path (e.g., "test.mp4")
# - an IP/RTSP/HTTP stream URL
# Set this to the desired camera index or URL
CAMERA_SOURCE = 0

# Preferred camera capture resolution (match your sensor aspect ratio to avoid cropping)
CAMERA_FRAME_WIDTH = 1280
CAMERA_FRAME_HEIGHT = 720

# Optional: scale the displayed window (1.0 = original capture size)
DISPLAY_SCALE = 1.0