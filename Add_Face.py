import face_recognition
import sys

# Load the image
image = face_recognition.load_image_file(sys.argv[1])

# Find the face location
face_locations = face_recognition.face_locations(image)

if len(face_locations) == 0:
    print('Error: No face found in image')
elif len(face_locations) > 1:
    print('Error: Multiple faces found in image')
else:
    # Encode the face
    face_encoding = face_recognition.face_encodings(image, face_locations)[0]

    # Add the face encoding to a database
    # Replace 'face_database.txt' with the name of your face database file
    with open('face_database.txt', 'a') as f:
        f.write(','.join([str(e) for e in face_encoding]) + '\n')

    print('Face added successfully')
