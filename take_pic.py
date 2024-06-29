import cv2

# Open the default webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error opening webcam")
    exit()

# Read the first frame
ret, frame = cap.read()

# Check if the frame was read correctly
if not ret:
    print("Error reading frame")
    exit()

# Display the frame
cv2.imshow("Webcam", frame)
print("starting")

# Wait for the 'c' key to be pressed
while True:
    if cv2.waitKey(1) == ord('c'):
        # Save the picture
        cv2.imwrite("picture.jpg", frame)
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
print("starting")

import cv2

# Load an image from file
image = cv2.imread("picture.jpg")

# Check if the image was loaded successfully
if image is None:
    print("Error loading image")
    exit()

# Display the loaded image
cv2.imshow("Image", image)
print("starting")
cv2.waitKey(0)
print("starting")
#cv2.destroyAllWindows()



# send to octoai for background subtraction
from dotenv import load_dotenv
import os
import base64

# Encode the image to JPEG format
success, encoded_image = cv2.imencode('.jpg', image)

# Check if the encoding was successful
if not success:
    print("Error encoding image")
    exit()

# Convert the encoded image to a bytes object
image_bytes = encoded_image.tobytes()

# Encode the bytes object to a base64 string
encoded_string = base64.b64encode(image_bytes).decode()

print("starting")
load_dotenv()
OCTOAI_API_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNkMjMzOTQ5In0.eyJzdWIiOiJjMWE5ZTYyOS04ZGQ3LTRiMjAtODRkNi03M2I0MmU5M2RlYWYiLCJ0eXBlIjoidXNlckFjY2Vzc1Rva2VuIiwidGVuYW50SWQiOiI1OTRlZGYxYS1lZDc5LTRhZWEtOWZlYi02OWI5ZmRmNGFiYWUiLCJ1c2VySWQiOiJkYmQ1ODY5My1kY2ZiLTRlMzctYjhiMi01Y2EyMDhlNTQxOTUiLCJhcHBsaWNhdGlvbklkIjoiYTkyNmZlYmQtMjFlYS00ODdiLTg1ZjUtMzQ5NDA5N2VjODMzIiwicm9sZXMiOlsiRkVUQ0gtUk9MRVMtQlktQVBJIl0sInBlcm1pc3Npb25zIjpbIkZFVENILVBFUk1JU1NJT05TLUJZLUFQSSJdLCJhdWQiOiIzZDIzMzk0OS1hMmZiLTRhYjAtYjdlYy00NmY2MjU1YzUxMGUiLCJpc3MiOiJodHRwczovL2lkZW50aXR5Lm9jdG8uYWkiLCJpYXQiOjE3MTk2OTQ1MDN9.bICfd8Rf26ZMV0Ov9b3HUx205kGDAZEHJNRrdFgMsk8xcLRSlNJjq-nwCIyKZlKVGzTjg2ZyGQFRORbFrRdHJLwM0FikaTB1xloeUQBXPn3EtYpiJM7qG0LMCcmmsu4YgbHQL36LreQgKgQr10H16USdXBxPApHawL0f2Q2oq98RcrUlD3mcfpZHQ6gkmEqU28cPVJqWiF5cPeaFxSt_qFRMtrsYLFeMdNSV0Edro2CB5XGF9qJYKi-rHUbjy79SpZbfKxJOu20iJFmEoRcjO5FFDqowJ44yleI68ghLbtqhGWX2UcEQSsapdiQ7hxShkNMMQNgckAckEiqEzWRMWg"


print(OCTOAI_API_TOKEN)


import requests
import json
import os
import base64
import time
import io
import PIL.Image
from typing import Optional, Tuple


def processtest(url):
    image = PIL.Image.open("picture.jpg")

    # Create a BytesIO buffer to hold the image data
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='JPEG')
    image_bytes = image_buffer.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    print("starting")

    payload = {
        "init_image": encoded_image,
        "bgcolor":(255, 255, 255, 0)
    }
    headers = {
        "Authorization": f"Bearer {OCTOAI_API_TOKEN}",
        "Content-Type": "application/json",
        "X-OctoAI-Queue-Dispatch": "true"
    }

    print("sending request 2")
    response = requests.post(url, headers=headers, json=payload)
    print("sending request 3")

    if response.status_code != 200:
        print(response.text)
    print(response.json())

    img_info = response.json()["image_b64"]

    img_bytes = base64.b64decode(img_info)
    img = PIL.Image.open(io.BytesIO(img_bytes))

    if img.mode == 'RGBA':
     img = img.convert('RGB')
    print("hi")

    img.save("result_image.png")
    print("hi")

processtest("https://image.octoai.run/background-removal")
