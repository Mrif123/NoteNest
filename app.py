from flask import Flask, redirect, url_for, session
from flask_dance.contrib.google import make_google_blueprint, google
import firebase_admin
from firebase_admin import credentials, db
import os
from dotenv import load_dotenv

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
load_dotenv()

app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Set up the Google OAuth blueprint with explicit scope URLs
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["https://www.googleapis.com/auth/userinfo.email", "openid", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_to="google_login"
)
app.register_blueprint(google_bp, url_prefix="/login")

# Initialize Firebase Admin SDK
cred = credentials.Certificate('notenest-147d2-firebase-adminsdk-c8sy5-a829ae7413.json')  # Path to your service account key
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://notenest-147d2-default-rtdb.firebaseio.com/'  # Replace with your database URL
})

# Route to write data to Firebase
@app.route('/write_email')
def write_email():
    # Check if the user is logged in
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    # Use session data instead of making an API call
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    
    # Check if the email already exists in Firebase
    users_ref = db.reference('users')
    users = users_ref.get()

    # Look for the email in the users data
    existing_user_id = None
    if users:
        for user_id, user_data in users.items():
            if user_data.get('email') == user_email:
                existing_user_id = user_id
                break

    # If the email already exists, retrieve the user ID and store it in the session
    if existing_user_id:
        session['auto_increment_user_id'] = existing_user_id
        return f"User with email {user_email} already exists. Retrieved User ID: {existing_user_id}"

    # If the email doesn't exist, create a new user
    counter_ref = db.reference('user_counter')
    current_id = counter_ref.get()

    if current_id is None:
        current_id = 0  # Initialize if not present

    # Increment the counter for the new user
    new_user_id = current_id + 1
    
    # Update the counter in Firebase
    counter_ref.set(new_user_id)

    # Write user data to Firebase with the new auto-incremented user_id
    user_ref = db.reference(f'users/{new_user_id}')
    user_ref.set({
        'username': user_name,
        'email': user_email,
        'user_id': new_user_id  # Add the user_id field
    })

    # Store the new user_id in the session
    session['auto_increment_user_id'] = new_user_id

    return f"User info written successfully! Name: {user_name}, Email: {user_email}, User ID: {new_user_id}"

@app.route('/write_note')
def write_note():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    # Use session data for the user
    user_email = session.get('user_email')
    user_name = session.get('user_name')
    user_id = session.get('auto_increment_user_id')  # Use the auto-incremented user ID

    # For simplicity, hardcode or get the note title and content as query parameters
    note_title = "My Third Note"  # Replace with real data from a form or request
    note_content = "This is the content of my first note."  # Replace with real data from a form or request

    # Call the helper function to create user and add a note
    create_user_and_note(user_id, user_name, user_email, note_title, note_content)

    return f"Note titled '{note_title}' created successfully for {user_name}."

# Helper function to create user and add a note to Firebase
def create_user_and_note(user_id, username, email, note_title, note_content):
    user_ref = db.reference(f'users/{user_id}')
    user_ref.set({
        'username': username,
        'email': email
    })
    
    note_ref = db.reference(f'notes/{user_id}')  # Notes are stored per user
    note_ref.push({
        'title': note_title,
        'content': note_content
    })

    print(f"User {username} and their note created successfully.")

# Route to read data from Firebase
@app.route('/read')
def read_data():
    if not google.authorized:
        return redirect(url_for("google.login"))

    # Retrieve the user ID from the session
    user_id = session.get('auto_increment_user_id')

    if not user_id:
        return "No user ID found in session."

    # Fetch the notes for the specific user from Firebase
    notes_ref = db.reference(f'notes/{user_id}')
    user_notes = notes_ref.get()

    if not user_notes:
        return f"No notes found for user ID: {user_id}"

    return f"Notes for User ID {user_id}: {user_notes}"


# OAuth login route
@app.route('/google_login')
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()

    # Safely access 'sub', 'email', and 'name' fields
    user_id = user_info.get('sub', 'unknown_user')  # Use Google user ID
    user_name = user_info.get('name', 'No name provided')
    user_email = user_info.get('email', 'No email provided')

    # Store the user data in the session
    session['user_id'] = user_id
    session['user_email'] = user_email
    session['user_name'] = user_name

    return f"Logged in as {user_name} ({user_email})"


if __name__ == "__main__":
    app.run(debug=True)
