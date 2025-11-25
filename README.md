# Metro Ticketing System with Face Recognition

A comprehensive metro ticketing system that uses facial recognition technology for seamless entry and exit, integrated with a web interface for account management and transactions.

## Features

- **Face Recognition Entry/Exit**: Automatic fare detection using facial recognition at metro stations
- **Web Interface**: User-friendly interface for account management and money top-up
- **Transaction Management**: Complete transaction history and balance tracking
- **Admin Desktop System**: Desktop application for station management and user registration
- **Firebase Integration**: Real-time database for user accounts, transactions, and face encodings

## Prerequisites

### Desktop System

- Python 3.8+
- OpenCV
- face_recognition library
- Firebase Admin SDK
- tkinter (usually comes with Python)

### User Web Interface

- Node.js 14+
- npm or yarn
- React
- Firebase SDK

## Installation

### 1. Firebase Setup

**IMPORTANT**: You need to obtain your Firebase credentials before running this project.

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project (or create a new one)
3. Go to **Project Settings** > **Service Accounts**
4. Click **Generate New Private Key**
5. Save the downloaded JSON file as `firebase-credentials.json`
6. Place it in the **root directory** of the project

**Note**: Never commit `firebase-credentials.json` to version control. It's already added to `.gitignore`.

### 2. Desktop System Setup

```bash
cd desktop-system

# Install required Python packages
pip install opencv-python
pip install face-recognition
pip install firebase-admin
pip install numpy
```

**Update file paths**: Open each Python file and update the Firebase credentials path to match your system:

```python
cred = credentials.Certificate("./firebase-credentials.json")
```

### 3. User Web Interface Setup

#### Frontend (React App)

```bash
cd user-side/client

# Install dependencies
npm install
# or
yarn install

# Install react-router-dom (if not already installed)
npm install react-router-dom
```

**Create `.env` file** in `user-side/client/` directory:

```env
REACT_APP_FIREBASE_API_KEY=your_api_key_here
REACT_APP_FIREBASE_AUTH_DOMAIN=your_auth_domain_here
REACT_APP_FIREBASE_DATABASE_URL=your_database_url_here
REACT_APP_FIREBASE_PROJECT_ID=your_project_id_here
REACT_APP_FIREBASE_STORAGE_BUCKET=your_storage_bucket_here
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id_here
REACT_APP_FIREBASE_APP_ID=your_app_id_here
```

Get these values from your Firebase project settings.

**Start the React app**:

```bash
npm start
# or
yarn start
```

The app will run on `http://localhost:3000`

#### Backend (Flask Server)

```bash
cd user-side/server

# Install required packages
pip install flask
pip install firebase-admin
pip install face-recognition
pip install opencv-python

# Update the Firebase credentials path in app.py
# Then run the server
python app.py
```

The server will run on `http://localhost:5000`

## 🎯 Usage

### For Station Operators (Desktop System)

1. **Launch Admin Interface**:

   ```bash
   python gui1.py
   ```

   - Login with admin credentials
   - Add new operators
   - Set up cameras for entry/exit stations

2. **Launch User Registration Interface**:

   ```bash
   python gui2.py
   ```

   - Register new users with face encodings
   - Add money to user accounts
   - Manage user data

3. **Station Operations**:
   - Entry station: Automatically runs via `entry.py`
   - Exit station: Automatically runs via `zexitFinalS1.py`
   - Fare is calculated based on entry and exit stations

### For Users (Web Interface)

1. Open browser and navigate to `http://localhost:3000`
2. **Register**: Create a new account
3. **Login**: Access your dashboard
4. **Add Money**: Top up your metro card
5. **Add Face**: Register your face for recognition (redirects to server interface)
6. Use metro stations with face recognition for seamless travel

## Firestore Collections

The system uses the following Firestore collections:

- `credentials`: Admin/operator login credentials
- `accounts`: User account balances
- `face_encodings`: Stored face recognition data
- `entry_info`: Entry station logs
- `exit_info`: Exit station logs
- `last_station`: Last known station for each user
- `transactions`: Complete transaction history

## Fare Structure

Default fare charges between stations:

- Station A ↔ Station B: ₹10
- Station B ↔ Station C: ₹5
- Station A ↔ Station C: ₹12

_Modify charges in `zexitFinalS1.py` as needed._

## Security Notes

- **Never commit** `firebase-credentials.json` to version control
- **Never commit** `.env` files with actual credentials
- Keep your Firebase API keys secure
- Update Firebase security rules for production deployment
- Use environment variables for all sensitive data

### Firebase authentication errors

- Verify `firebase-credentials.json` is in the correct location
- Check that all environment variables are set correctly in `.env`
- Ensure Firebase rules allow read/write access
