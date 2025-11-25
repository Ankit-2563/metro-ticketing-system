import os
import base64
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import face_recognition

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/Users/ankitbhavarthe/metro-ticketing-system/firebase-credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def get_face_encodings(file_path):
    image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    return face_encodings

@app.route('/')
def index():
    return 'Welcome to the Face Recognition API'

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        name = request.form.get('name')

        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not name:
            return jsonify({"error": "No name provided"}), 400

        if file:
            # Save the file
            upload_dir = os.path.join(os.getcwd(), "uploads")
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            file_path = os.path.join(upload_dir, file.filename)
            file.save(file_path)

            # Get face encodings
            face_encodings = get_face_encodings(file_path)

            # Serialize face encodings to base64-encoded strings
            encoded_encodings = [base64.b64encode(encoding).decode('utf-8') for encoding in face_encodings]

            # Store face encodings in Firestore with user-provided name as document ID
            for encoded_encoding in encoded_encodings:
                doc_ref = db.collection(u'face_encodings').document(name)
                doc_ref.set({
                    u'name': name,
                    u'encoding': encoded_encoding,
                    u'file_path': file_path
                })

            return jsonify({"message": "File uploaded and face encodings stored successfully"}), 200
    else:
        return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == '__main__':
    app.run(debug=True)
