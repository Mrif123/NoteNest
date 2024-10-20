from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()  # Load environment variables before the app runs

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Configure OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://127.0.0.1:5000/auth/callback',
    client_kwargs={'scope': 'openid email profile',
                   'response_type': 'code'},
)

# Configure the PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

# Create tables for Users and Notes if they don't exist
def create_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    # Create Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL
        );
    """)

    # Create Notes table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            content TEXT,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

# OAuth login route
@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    print("Redirecting to:", redirect_uri)  # Debug log
    return google.authorize_redirect(redirect_uri)

# OAuth callback route
@app.route('/auth/callback')
def auth_callback():
    token = google.authorize_access_token()
    print("Token received:", token)
    user_info = google.parse_id_token(token)
    print("User info:", user_info)
    # Extract email and other details
    user_email = user_info['email']

    # Check if the user exists, if not, create the user
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE email = %s;", (user_email,))
    user = cur.fetchone()

    if not user:
        cur.execute("INSERT INTO users (email) VALUES (%s) RETURNING id;", (user_email,))
        user = cur.fetchone()
        conn.commit()

    user_id = user[0]
    session['user_email'] = user_email
    session['user_id'] = user_id

    cur.close()
    conn.close()

    return redirect(url_for('index'))

# Home route to display notes for a specific user
@app.route('/')
def index():
    if 'user_email' not in session:
        return redirect(url_for('login'))

    user_email = session['user_email']
    user_id = session['user_id']

    # Get the notes of the current user
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notes WHERE user_id = %s;", (user_id,))
    notes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('index.html', notes=notes, user_email=user_email)

# Route to add a new note
@app.route('/add', methods=['POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    title = request.form['title']
    content = request.form['content']
    user_id = session['user_id']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO notes (title, content, user_id) VALUES (%s, %s, %s);", (title, content, user_id))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))

# Delete a note
@app.route('/delete/<int:id>')
def delete_note(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s;", (id,))
    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
