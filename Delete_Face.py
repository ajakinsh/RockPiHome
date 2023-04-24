import face_recognition

# Load the face database
# Replace 'face_database.txt' with the name of your face database file
with open('face_database.txt', 'r') as f:
    face_encodings = [list(map(float, line.strip().split(','))) for line in f.readlines()]

# Find the face location in the image
# Replace 'face.jpg' with the name of the file containing the face image
image = face_recognition.load_image_file('face.jpg')
face_locations = face_recognition.face_locations(image)

if len(face_locations) == 0:
    print('Error: No face found in image')
elif len(face_locations) > 1:
    print('Error: Multiple faces found in image')
else:
    # Encode the face
    face_encoding = face_recognition.face_encodings(image, face_locations)[0]

    # Compare the face encoding to the encodings in the database
    matches = face_recognition.compare_faces(face_encodings, face_encoding)

    if True in matches:
        # Delete the matching face encoding from the database
        index = matches.index(True)
        face_encodings.pop(index)

        # Rewrite the face database file without the deleted face encoding
        with open('face_database.txt', 'w') as f:
            for encoding in face_encodings:
                f.write(','.join([str(e) for e in encoding]) + '\n')

        print('Face deleted successfully')
    else:
        print('Error: Face not found in database')
