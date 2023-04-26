import face_recognition
import cv2

# Load the reference image
reference_image = face_recognition.load_image_file("jess.jpg")
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Open a connection to the default camera
video_capture = cv2.VideoCapture(5)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


# Wait for the camera to warm up
while True:
    for i in range(10):
        video_capture.grab()
    
    # Capture a frame from the camera
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (384, 216)) # make image smaller if huge
    

    # Convert the image to RGB format
    rgb_image = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the image
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    # Draw a box around each detected face
    for top, right, bottom, left in face_locations:
        cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # Compare each detected face to the reference image
    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance = 0.6)
        if match[0]:
            print("Found Jess!")
            # Draw a green box around the matched face
            cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(small_frame, "Hi Jess", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the resulting image
    cv2.imshow('Video', small_frame)

    # Wait for a key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
video_capture.release()
cv2.destroyAllWindows()
