#CORRECT 

import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import time
import sys
import base64

# Initialize Firebase app
cred = credentials.Certificate("/Users/ankitbhavarthe/metro-ticketing-system/firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def load_encodings_from_database():
    encodings = {}
    # Load face encodings from Firestore
    try:
        face_encodings_ref = db.collection('face_encodings').get()
        for doc in face_encodings_ref:
            data = doc.to_dict()
            name = doc.id
            encoding_base64 = data['encoding']
            encoding = np.frombuffer(base64.b64decode(encoding_base64), dtype=np.float64).reshape(-1, 128)
            encodings[name] = encoding
    except Exception as e:
        print("Failed to load face encodings:", e)
    return encodings

def main(station=None):
    if not station:
        station = input("Which station are you at? (A/B/C): ")

    known_encodings = load_encodings_from_database()

    while True:
        video_capture = cv2.VideoCapture(0)

        ret, frame = video_capture.read()

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Get the current time
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')

        # Loop through each face encoding found in the frame
        for face_location, face_encoding in zip(face_locations, face_encodings):
            # Compare with known encodings from the database
            for name, known_encoding_list in known_encodings.items():
                for known_encoding in known_encoding_list:
                    # Compare face encoding with known encodings
                    match = face_recognition.compare_faces([known_encoding], face_encoding)

                    if match[0]:
                        # Save the information to Firestore
                        try:
                            db.collection('entry_info').add({
                                'name': name,
                                'station': station,
                                'time': current_time
                            })
                            print("Entry information saved successfully!")
                            name = name
                            entry_station = station

                            try:
                                db.collection('last_station').document(name).set({
                                    'last_station': entry_station,
                                    'name': name
                                    
                                })
                                print("Last station information saved successfully!")
                            except Exception as e:
                                print("Failed to save last station information:", e)



                        except Exception as e:
                            print("Failed to save entry information:", e)

                        # Draw a box around the face
                        top, right, bottom, left = face_location
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                        # Display the name above the face
                        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)

                        break
                else:
                    continue
                break
            else:
                # Draw a box around the face
                top, right, bottom, left = face_location
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Display "Unknown" below the face
                cv2.putText(frame, 'Unknown', (left + 6, bottom + 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Release video capture
        video_capture.release()

        # Break the loop if 'q' is pressed
        # if cv2.waitKey(0) & 0xFF == ord('q'):
        break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1])
