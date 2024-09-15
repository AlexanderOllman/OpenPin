from flask import Flask, render_template_string, Response
import json
import random
import base64
import numpy as np
import openai
from io import BytesIO
from PIL import Image
import os
from picamera2 import Picamera2
from libcamera import controls


# api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI()

# Initialize the camera
picam2 = Picamera2()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config)
picam2.start()

print("Camera is ready. Press Enter to capture an image, or type 'exit' to quit.")


def capture_frame():
    # Capture a frame
    frame = picam2.capture_array()
    
    # Increase brightness
    picam2.set_controls({"Brightness": 1})  # Adjust as needed
    
    print(f"Captured frame shape: {frame.shape}")
    return frame

def encode_image(frame):
    # Convert to RGB (picamera2 captures in RGB format)
    image = Image.fromarray(frame)
    
    # Save image to bytes
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    
    return base64.b64encode(img_byte_arr).decode('utf-8')

def send_image(frame):
    base64_image = encode_image(frame)
    
    system_prompt = "describe what is in this image"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": system_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    
    content = response.choices[0].message.content
    return content


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

    frame = my_stream.getvalue()

    response = send_image(frame)

    print(f"Response: {response}")
    
    # If you want to process the image data in memory, you can do so here
    # For example: image_data = my_stream.getvalue()
    
    # Clear the stream for the next capture
    my_stream.close()

# Don't forget to stop the camera when you're done
picam2.stop()