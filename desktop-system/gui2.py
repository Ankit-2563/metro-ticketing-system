import tkinter as tk
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, firestore
import subprocess
import threading
import cv2
import face_recognition
import base64


# Initialize Firebase app
cred = credentials.Certificate("/Users/ankitbhavarthe/metro-ticketing-system/firebase-credentials.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Define add_money_frame as a global variable
add_money_frame = None

# Function to handle adding money
def add_money():
    global add_money_frame, added_name_entry, amount_entry  # Declare global variables

    # If add money, hide the main menu frame and show the add money frame
    main_menu_frame.pack_forget()
    add_money_frame = ttk.Frame(root)
    add_money_frame.pack()

    # Define added_name_entry and amount_entry as global variables
    added_name_entry = ttk.Entry(add_money_frame)
    amount_entry = ttk.Entry(add_money_frame)

    def save_added_money(go_to_main_menu_func):
        added_name = added_name_entry.get()
        amount = amount_entry.get()
        try:
            # Query Firestore to find the document with the given name
            query = db.collection('accounts').where('name', '==', added_name).limit(1)
            docs = query.stream()

            # If document found, update the amount
            for doc in docs:
                current_amount = doc.to_dict().get('amount', 0)
                new_amount = current_amount + float(amount)
                # Update the document with the new amount
                doc.reference.update({'amount': new_amount})
                print("Transaction saved successfully!")
                messagebox.showinfo("Transaction Success", f"Transaction saved successfully. New amount for {added_name}: {new_amount}")
                go_to_main_menu_func()  # Call the provided function to return to the main menu
                return

            # If no document found for the given name, create a new document
            db.collection('accounts').add({
                'name': added_name,
                'amount': float(amount),  # Convert amount to float if needed
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            print("Transaction saved successfully!")
            messagebox.showinfo("Transaction Success", f"Transaction saved successfully for new user {added_name}.")
            go_to_main_menu_func()  # Call the provided function to return to the main menu
        except Exception as e:
            print("Failed to save transaction:", e)
            messagebox.showerror("Transaction Failed", "Failed to save transaction. Please try again.")


    # Add widgets to the add money frame
    add_money_frame_heading = ttk.Label(add_money_frame, text="Add Money", font=('Arial', 12, 'bold'))
    add_money_frame_heading.grid(row=0, columnspan=2, pady=10)

    new_name_label = ttk.Label(add_money_frame, text="Your Name:")
    new_name_label.grid(row=1, column=0, pady=10)
    added_name_entry.grid(row=1, column=1, pady=10)

    amount_label = ttk.Label(add_money_frame, text="Amount:")
    amount_label.grid(row=2, column=0, pady=10)
    amount_entry.grid(row=2, column=1, pady=10)

    save_money_button = ttk.Button(add_money_frame, text="Save", command=lambda: save_added_money(go_to_main_menu))
    save_money_button.grid(row=3, columnspan=2, pady=10)

    # Add button to return to main menu
    return_to_main_menu_button = ttk.Button(add_money_frame, text="Return to Main Menu", command=go_to_main_menu)
    return_to_main_menu_button.grid(row=4, columnspan=2, pady=10)


# Function to save transaction asynchronously
def save_transaction_thread(name, amount):
    process = subprocess.Popen(["python", "8.py", name, amount])
    process.communicate()

# Function to save credentials
def save_credentials(username, password):
    try:
        db.collection('credentials').document(username).set({
            'password': password
        })
        messagebox.showinfo("Save Successful", "New user added successfully")
    except Exception as e:
        print(e)
        messagebox.showerror("Save Failed", "Failed to add user")

# Function to check user credentials
def check_credentials(event=None):
    username = username_entry.get()
    password = password_entry.get()
    try:
        doc_ref = db.collection('credentials').document(username)
        doc = doc_ref.get()
        if doc.exists and doc.to_dict()['password'] == password:
            # If login successful, hide the login frame and show the main menu
            login_frame.pack_forget()
            main_menu_frame.pack()
            label_menu.config(text=f"Welcome to Metro Ticketing through Face Recognition Application, {username}!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except Exception as e:
        print(e)
        messagebox.showerror("Login Failed", "An error occurred while checking credentials")

# Function to handle logout
def logout():
    # If logout, show the login frame and hide the main menu
    main_menu_frame.pack_forget()
    login_frame.pack()

# Function to handle saving added face
# Function to handle saving added face
# Function to handle saving added face
def check_existing_name(added_name, callback):
    try:
        doc_ref = db.collection('face_encodings').document(added_name)
        doc = doc_ref.get()
        callback(doc.exists)
    except Exception as e:
        print(e)
        messagebox.showerror("Database Error", "An error occurred while accessing the database")

def save_added_face():
    added_name = added_name_entry.get()
    
    # Define a callback function to handle the result of the database check
    def on_name_checked(result):
        if result:
            messagebox.showerror("Name Exists", "Name already exists in the database. Please enter a different name.")
        else:
            # Call the function to capture the user's face and store the encoding
            capture_and_store_face_encoding(added_name)
            go_to_main_menu()
    
    # Start a new thread to check if the name exists in the database
    threading.Thread(target=check_existing_name, args=(added_name, on_name_checked)).start()

# Function to capture the user's face and store the encoding in Firestore
def capture_and_store_face_encoding(name):
    # Capture the user's face using a camera
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    
    # Find the face location and encoding
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    if len(face_encodings) > 0:
        # Convert the face encoding to base64 for storage
        encoding_base64 = base64.b64encode(face_encodings[0]).decode('utf-8')
        
        try:
            # Store the face encoding in Firestore
            db.collection('face_encodings').document(name).set({
                'encoding': encoding_base64
            })
            print(f"Face encoding saved successfully for {name}!")
            messagebox.showinfo("Face Saved", f"Face encoding saved successfully for {name}!")
                # Create a new document in the 'accounts' collection with initial amount as 0
            try:
                db.collection('accounts').add({
                    'name': name,  # Initialize name as empty string, it will be updated later
                    'amount': 0,  # Initialize amount as 0
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
                print("New account created successfully!")
            except Exception as e:
                print("Failed to create new account:", e)
        except Exception as e:
            print("Failed to save face encoding:", e)
            messagebox.showerror("Error", "Failed to save face encoding. Please try again.")
    else:
        print("No face detected.")
        messagebox.showerror("Error", "No face detected. Please make sure your face is visible.")
    
    # Release video capture
    video_capture.release()
    cv2.destroyAllWindows()


# Function to open register/add face window
def open_register_face_window():
    # Hide the main menu frame and show the register/add face frame
    main_menu_frame.pack_forget()
    register_face_frame.pack()


# Rest of the code...


# Function to quit the application
def quit_application():
    root.quit()

# Function to go to the main menu
def go_to_main_menu():
    global add_money_frame
    if add_money_frame:
        add_money_frame.pack_forget()
    register_face_frame.pack_forget()
    main_menu_frame.pack()

# Create the main window
root = tk.Tk()
root.title("Login App")

# Determine the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the width and height of the window to be 50% of the screen
root.geometry(f"{screen_width//2}x{screen_height//2}")

# Create frames for login, main menu, add user, register/add face
login_frame = ttk.Frame(root)
login_frame.pack(fill=tk.BOTH, expand=True)

main_menu_frame = ttk.Frame(root)

register_face_frame = ttk.Frame(root)

# Add widgets to the login frame
heading_label = ttk.Label(login_frame, text="Welcome to Metro Ticketing through Face Recognition Application", font=('Arial', 14, 'bold'))
heading_label.pack(pady=(50, 20))

subheading_label = ttk.Label(login_frame, text="Enter your Credentials", font=('Arial', 10, 'bold'))
subheading_label.pack()

username_label = ttk.Label(login_frame, text="Username:")
username_label.pack()

username_entry = ttk.Entry(login_frame)
username_entry.pack()

password_label = ttk.Label(login_frame, text="Password:")
password_label.pack()

password_entry = ttk.Entry(login_frame, show="*")
password_entry.pack()

login_button = ttk.Button(login_frame, text="Login", command=check_credentials)
login_button.pack(pady=10)

def on_enter_key(event):
    check_credentials()

username_entry.bind('<Return>', on_enter_key)
password_entry.bind('<Return>', on_enter_key)

# Add option to quit program in the login frame
quit_button_login = ttk.Button(login_frame, text="QUIT", command=quit_application)
quit_button_login.pack(pady=10)

# Add widgets to the main menu frame
# Add label to main menu frame for the greeting
label_menu = ttk.Label(main_menu_frame, text="Welcome")
label_menu.pack(pady=10)

# Add option to add money
add_money_button = ttk.Button(main_menu_frame, text="Add Money", command=add_money)
add_money_button.pack(pady=10)

# Add option to register/add face
register_face_button= ttk.Button(main_menu_frame, text="Register / Add Face", command=open_register_face_window)
register_face_button.pack(pady=10)

# Add option to logout program
logout_button = ttk.Button(main_menu_frame, text="Logout", command=logout)
logout_button.pack(pady=10)

# Hide the main menu frame initially
main_menu_frame.pack_forget()

# Add widgets to the register/add face frame
register_face_label = ttk.Label(register_face_frame, text="Register / Add Face", font=('Arial', 12, 'bold'))
register_face_label.grid(row=0, columnspan=2, pady=10)

name_label = ttk.Label(register_face_frame, text="Your Name:")
name_label.grid(row=1, column=0, pady=10)
added_name_entry = ttk.Entry(register_face_frame)
added_name_entry.grid(row=1, column=1, pady=10)

# Add button to save added face
save_face_button = ttk.Button(register_face_frame, text="Save", command=save_added_face)
save_face_button.grid(row=2, columnspan=2, pady=10)

# Add button to return to main menu from register/add face frame
return_to_main_menu_button = ttk.Button(register_face_frame, text="Return to Main Menu", command=go_to_main_menu)
return_to_main_menu_button.grid(row=3, columnspan=2, pady=10)

# Hide the register/add face frame initially
register_face_frame.pack_forget()

root.mainloop()
