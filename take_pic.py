import cv2
import os
import base64
import requests
from dotenv import load_dotenv
import PIL.Image
import io

# Capture and save a picture from the webcam
def capture_picture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Error opening webcam")
    ret, frame = cap.read()
    if not ret:
        raise Exception("Error reading frame")
    cv2.imshow("Webcam", frame)
    while True:
        if cv2.waitKey(1) == ord('c'):
            cv2.imwrite("picture.jpg", frame)
            break
    cap.release()
    cv2.destroyAllWindows()

# Load and display an image
def load_and_display_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception("Error loading image")
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Send image to OctoAI for background subtraction
def send_to_octoai(image_path, api_url):
    load_dotenv()
    OCTOAI_API_TOKEN = os.getenv('OCTOAI_API_TOKEN')
    image = PIL.Image.open(image_path)
    image_buffer = io.BytesIO()
    image.save(image_buffer, format='JPEG')
    image_bytes = image_buffer.getvalue()
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    payload = {
        "init_image": encoded_image,
        "bgcolor": (255, 255, 255, 0)
    }
    headers = {
        "Authorization": f"Bearer {OCTOAI_API_TOKEN}",
        "Content-Type": "application/json",
        "X-OctoAI-Queue-Dispatch": "true"
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(response.text)
    img_info = response.json()["image_b64"]
    img_bytes = base64.b64decode(img_info)
    img = PIL.Image.open(io.BytesIO(img_bytes))
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img.save("result_image.png")

# Main execution
if __name__ == "__main__":
    capture_picture()
    send_to_octoai("picture.jpg", "https://image.octoai.run/background-removal")
    load_and_display_image("result_image.png")
