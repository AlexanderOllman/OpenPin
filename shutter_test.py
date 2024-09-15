from picamera2 import Picamera2
import time
from datetime import datetime

picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start()

print("Camera is ready. Press Enter to capture an image, or type 'exit' to quit.")

while True:
    user_input = input()
    
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    
    # Generate a filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    
    # Capture the image
    picam2.capture_file(filename)
    print(f"Image captured: {filename}")

picam2.stop()