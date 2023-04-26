import face_recognition
import cv2

# Open a connection to the default camera
video_capture = cv2.VideoCapture(0)

# Wait for the camera to warm up
while True:
    # Capture a frame from the camera
    ret, frame = video_capture.read()

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
video_capture.release()
cv2.destroyAllWindows()

# Convert the image to RGB format
rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

# Detect faces in the image
face_locations = face_recognition.face_locations(rgb_image)

# Draw a box around each detected face
for top, right, bottom, left in face_locations:
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

# Save the image as a JPEG file
cv2.imwrite('image.jpg', frame)
