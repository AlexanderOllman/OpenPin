from picamera2 import Picamera2
from datetime import datetime
from io import BytesIO

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start()

print("Camera is ready. Press Enter to capture an image, or type 'exit' to quit.")

while True:
    user_input = input()
    
    if user_input.lower() == 'exit':
        print("Exiting the program.")
        break
    
    # Create a BytesIO object to hold the image data
    my_stream = BytesIO()
    
    # Capture the image to the BytesIO stream
    picam2.capture_file(my_stream, format='jpeg')
    
    # Reset the stream position to the beginning
    my_stream.seek(0)
    
    # Generate a filename with the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"capture_{timestamp}.jpg"
    
    # Save the image from the stream to a file
    with open(filename, 'wb') as f:
        f.write(my_stream.getvalue())
    
    print(f"Image captured: {filename}")
    
    # If you want to process the image data in memory, you can do so here
    # For example: image_data = my_stream.getvalue()
    
    # Clear the stream for the next capture
    my_stream.close()

picam2.stop()