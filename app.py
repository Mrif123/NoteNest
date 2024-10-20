from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Create GitHub OAuth blueprint
github_bp = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    scope=["read:user", "user:email"]  # Adjust scopes as needed
)
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok, resp.text
    user_info = resp.json()
    return f"You are logged in as {user_info['login']} on GitHub"

@app.route("/login")
def login():
    return redirect(url_for("github.login"))

if __name__ == "__main__":
    print("GITHUB_CLIENT_ID:", os.getenv("GITHUB_CLIENT_ID"))
    print("GITHUB_CLIENT_SECRET:", os.getenv("GITHUB_CLIENT_SECRET"))
    app.run(debug=True)
