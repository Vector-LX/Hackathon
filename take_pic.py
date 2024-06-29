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

# Wait for the 'c' key to be pressed
while True:
    if cv2.waitKey(1) == ord('c'):
        # Save the picture
        cv2.imwrite("picture.jpg", frame)
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()

import cv2

# Load an image from file
image = cv2.imread("picture.jpg")

# Check if the image was loaded successfully
if image is None:
    print("Error loading image")
    exit()

# Display the loaded image
cv2.imshow("Image", image)
cv2.waitKey(0)
#cv2.destroyAllWindows()