from flask import Flask, render_template_string, Response
import json
import random
import base64
import cv2
import numpy as np
import openai
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

api_key = os.environ.get("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def capture_frame():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()

    if ret:
        # Increase brightness
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, 30)  # Increase brightness by 30
        v[v > 255] = 255  # Cap at 255 to avoid overflow
        final_hsv = cv2.merge((h, s, v))
        frame = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

        print(f"Captured frame shape: {frame.shape}")
    else:
        print("Failed to capture frame")
    
    return frame

def encode_image(frame):
    # Ensure the frame is in BGR color space (OpenCV default)
    if len(frame.shape) == 2:  # If grayscale, convert to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    
    _, buffer = cv2.imencode('.jpg', frame)
    img_bytes = BytesIO(buffer).getvalue()
    return base64.b64encode(img_bytes).decode('utf-8')

def get_quiz_data(frame):
    base64_image = encode_image(frame)
    
    # system_prompt = "Under California Driving Law, what is the answer to this question? Provide your answer in json format, with fields 'question', 'answer', and 'answering_letter'."
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
    print("Raw response:", content)  # For debugging
