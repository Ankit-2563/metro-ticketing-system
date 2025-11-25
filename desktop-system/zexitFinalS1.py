import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
import time
import sys
import base64
import subprocess

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

def save_transaction(name, amount, transaction_type, transaction_time):
    # Reference the existing "transactions" collection and add a new document
    db.collection("transactions").add({
        'name': name,
        'amount': amount,
        'transaction_type': transaction_type,
        'transaction_time': transaction_time
    })
    print("Transaction saved successfully.")

def get_last_station_from_last_station(name):
    try:
        last_station_ref = db.collection('last_station').document(name).get()
        if last_station_ref.exists:
            return last_station_ref.to_dict().get('last_station')
            print(last_station)
        else:
            print("No last station found for", name)
            return None
    except Exception as e:
        print("Failed to get last station from last_station:", e)
        return None

def main(station=None):
    if not station:
        station = input("Which station are you at? (A/B/C): ")

    known_encodings = load_encodings_from_database()

    # Dictionary to store the last known station for each person
    last_station = {}

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
                        # Save exit information to Firestore
                        try:
                            db.collection('exit_info').add({
                                'name': name,
                                'station': station,
                                'time': current_time
                            })
                            print("Exit information saved successfully!")
                            
                            # Get last station from entry_info
                            entry_station = get_last_station_from_last_station(name)
                            print("Last station for", name, ":", entry_station)
                            if entry_station:
                                charge = calculate_charge(entry_station, station, name)
                                if charge < 0:
                                    transaction_time = time.strftime('%Y-%m-%d %H:%M:%S')
                                    transaction_type = f"Travelled from {entry_station} to {station}"
                                    save_transaction(name, charge, transaction_type, transaction_time)
                                    last_station[name] = station  # Update last station in memory
                            else:
                                # If entry station is not found, store the current station as entry station
                                last_station[name] = station
                                # Also store the last station in entry_info
                                db.collection('entry_info').add({'name': name, 'station': station, 'time': current_time})

                        except Exception as e:
                            print("Failed to save exit information:", e)

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

def calculate_charge(entry_station, exit_station, name):
    # Dictionary to hold charge information
    charges = {
        ('A', 'B'): -10,
        ('B', 'C'): -5,
        ('A', 'C'): -12,
        ('B', 'A'): -10,
        ('C', 'B'): -5,
        ('C', 'A'): -12
    }

    charge = charges.get((entry_station, exit_station), 0)
    
    # Call deduct.py script to process the charge
    subprocess.run(["python", "deduct.py", str(charge), name])

    return charge

if __name__ == "__main__":
    if len(sys.argv) < 2:
        main()
    else:
        main(sys.argv[1])
