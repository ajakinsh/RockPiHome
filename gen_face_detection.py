import face_recognition
biden_image = face_recognition.load_image_file("biden.jpg")
larson1 = face_recognition.load_image_file("larson1.png")
larson2 = face_recognition.load_image_file("larson2.jpg")

biden_encoding = face_recognition.face_encodings(biden_image)[0]
larson1_encoding = face_recognition.face_encodings(larson1)[0]
larson2_encoding = face_recognition.face_encodings(larson2)[0]

results1 = face_recognition.compare_faces([biden_encoding], larson1_encoding) # compare biden with larson
results2 = face_recognition.compare_faces([larson1_encoding], larson2_encoding) # compare larson with image

print("Test 1:", results1)
print("\nTest 2:", results2)