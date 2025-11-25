# CORRECT

import tkinter as tk
from tkinter import messagebox, ttk
import firebase_admin
from firebase_admin import credentials, firestore
import subprocess

# Initialize Firebase Admin SDK
cred = credentials.Certificate("/Users/ankitbhavarthe/metro-ticketing-system/firebase-credentials.json")  # Path to your Firebase service account key
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_credentials(username, password):
    try:
        # Add document to 'credentials' collection in Firestore
        db.collection('credentials').document(username).set({'password': password})
        messagebox.showinfo("Save Successful", "New user added successfully")
    except Exception as e:
        messagebox.showerror("Save Failed", f"Error: {e}")

def check_credentials(event=None):
    username = username_entry.get()
    password = password_entry.get()
    doc_ref = db.collection('credentials').document(username)
    doc = doc_ref.get()
    if doc.exists and doc.to_dict()['password'] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        # Hide the login frame and show the main menu frame
        login_frame.pack_forget()
        main_menu_frame.pack()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def logout():
    # If logout, show the login frame and hide the main menu
    main_menu_frame.pack_forget()
    login_frame.pack()



def save_user_credentials():
    # Get username and password from the entry fields
    username = added_username_entry.get()
    password = added_password_entry.get()

    # Check if username and password are not empty
    if username and password:
        # Save the credentials to Firestore
        save_credentials(username, password)
    else:
        messagebox.showerror("Error", "Username and password cannot be empty")

def add_user():
    # If add user, hide the main menu frame and show the add user frame
    main_menu_frame.pack_forget()
    add_user_frame.pack()

    # Add widgets to the add user frame
    global added_username_entry, added_password_entry
    add_user_frame_heading = ttk.Label(add_user_frame, text="Add New User", font=('Arial', 12, 'bold'))
    add_user_frame_heading.grid(row=0, columnspan=2, pady=10)

    new_username_label = ttk.Label(add_user_frame, text="New Username:")
    new_username_label.grid(row=1, column=0, pady=10)
    added_username_entry = ttk.Entry(add_user_frame)
    added_username_entry.grid(row=1, column=1, pady=10)

    new_password_label = ttk.Label(add_user_frame, text="New Password:")
    new_password_label.grid(row=2, column=0, pady=10)
    added_password_entry = ttk.Entry(add_user_frame, show="*")
    added_password_entry.grid(row=2, column=1, pady=10)

    save_button = ttk.Button(add_user_frame, text="Save", command=save_user_credentials)
    save_button.grid(row=3, columnspan=2, pady=10)

    # Add button to return to main menu
    return_to_main_menu_button = ttk.Button(add_user_frame, text="Return to Main Menu", command=go_to_main_menu)
    return_to_main_menu_button.grid(row=4, columnspan=2, pady=10)


def set_camera():
    # If set camera, hide the main menu frame and show the camera frame
    main_menu_frame.pack_forget()
    set_camera_frame.pack()

    # Check if the button is already added
    if not hasattr(set_camera_frame, 'return_to_main_menu_button'):
        # Add button to return to main menu
        set_camera_frame.return_to_main_menu_button = ttk.Button(set_camera_frame, text="Return to Main Menu", command=go_to_main_menu)
        set_camera_frame.return_to_main_menu_button.pack()

# def save_set_camera():
#     # selected_camera = camera_var.get()
#     selected_station = station_var.get()
#     selected_placement = placement_var.get()

#     # Call code 2 as a subprocess with the selected information as arguments
#     # subprocess.Popen(["python", "4.py", selected_camera, selected_station, selected_placement])
#     subprocess.Popen(["python", "4.py", selected_station, selected_placement])

def save_set_camera():
    selected_station = station_var.get()
    selected_placement = placement_var.get()

    if selected_placement == "Entry":
        # Call code 1 as a subprocess with the selected information as arguments
        subprocess.Popen(["python", "./entry.py", selected_station])
    elif selected_placement == "Exit":
        # Call code 2 as a subprocess with the selected information as arguments
        subprocess.Popen(["python", "./zexitFinalS1.py", selected_station])


def quit_application():
    # Quit the application
    root.quit()

def go_to_main_menu():
    add_user_frame.pack_forget()
    set_camera_frame.pack_forget()
    main_menu_frame.pack()

# Create the main window
root = tk.Tk()
root.title("Login App")

# Determine the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the width and height of the window to be 50% of the screen
root.geometry(f"{screen_width//2}x{screen_height//2}")

# Create frames for login, main menu, add user, set camera, and station
login_frame = ttk.Frame(root)
login_frame.pack(fill=tk.BOTH, expand=True)

main_menu_frame = ttk.Frame(root)

add_user_frame = ttk.Frame(root)

set_camera_frame = ttk.Frame(root)

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

# Add set camera button
set_camera_button = ttk.Button(main_menu_frame, text="Set Camera", command=set_camera)
set_camera_button.pack(pady=10)

# Add option to add a new user
add_user_button = ttk.Button(main_menu_frame, text="Add User", command=add_user)
add_user_button.pack(pady=10)

# Add option to logout program
logout_button = ttk.Button(main_menu_frame, text="Logout", command=logout)
logout_button.pack(pady=10)

# Hide the main menu frame initially
main_menu_frame.pack_forget()

# Add widgets to the set camera frame
camera_label = ttk.Label(set_camera_frame, text="Select Camera:")
camera_label.pack(pady=10)

camera_var = tk.StringVar()
camera_dropdown = ttk.Combobox(set_camera_frame, textvariable=camera_var, state='readonly')
camera_dropdown['values'] = ("Camera 1","Camera 2")  # Only "Camera 1" option
camera_dropdown.pack(pady=10)

station_label = ttk.Label(set_camera_frame, text="Select Station:")
station_label.pack()

station_var = tk.StringVar()
station_dropdown = ttk.Combobox(set_camera_frame, textvariable=station_var, state='readonly')
station_dropdown['values'] = ("A", "B", "C")
station_dropdown.pack(pady=10)

placement_label = ttk.Label(set_camera_frame, text="Placement:")
placement_label.pack()

placement_var = tk.StringVar()
placement_dropdown = ttk.Combobox(set_camera_frame, textvariable=placement_var, state='readonly')
placement_dropdown['values'] = ("Entry", "Exit")
placement_dropdown.pack(pady=10)

save_camera_button = ttk.Button(set_camera_frame, text="Save", command=save_set_camera)
save_camera_button.pack(pady=10)

# Hide the set camera frame initially
set_camera_frame.pack_forget()

root.mainloop()
