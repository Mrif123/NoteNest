# 📝 NoteNest

**NoteNest** is a web-based note-taking application designed to help users efficiently create, manage, and organize their notes. With a user-friendly interface and essential features, NoteNest ensures that your important thoughts and ideas are always accessible.

## 🌟 Features

- **Create Notes**: Easily add new notes with a simple and intuitive interface.
- **Edit Notes**: Modify existing notes to keep information up-to-date.
- **Delete Notes**: Remove notes that are no longer needed.
- **Organize Notes**: Categorize and sort notes for better organization.

## 🛠️ Technologies Used

- **Backend**: Python with Flask framework
- **Frontend**: HTML, CSS, and JavaScript
- **Database**: SQLite for data storage

## 🚀 Getting Started

Follow these steps to set up the project locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Mrif123/NoteNest.git
   cd NoteNest
Create a Virtual Environment:

bash
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows, use 'env\Scripts\activate'
Install Dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Set the Flask App Environment Variable:

bash
Copy
Edit
export FLASK_APP=app.py  # On Windows, use 'set FLASK_APP=app.py'
Initialize the Database:

bash
Copy
Edit
flask init-db
Run the Application:

bash
Copy
Edit
flask run
The application will be accessible at http://127.0.0.1:5000/.

📁 Project Structure
plaintext
Copy
Edit
NoteNest/
│
├── static/
│   ├── css/
│   └── js/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── ...
│
├── app.py
├── requirements.txt
└── README.md
static/: Contains static files like CSS and JavaScript.
templates/: Holds HTML templates for rendering pages.
app.py: Main application file.
requirements.txt: List of Python dependencies.
🤝 Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.
Please ensure your code adheres to the project's coding standards and includes appropriate tests
