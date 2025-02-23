import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Hardcoded admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'adminpassword'  # You can change this to your desired admin password

# Define allowed file extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}

# Set up the upload folder in the app's config
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Set max file size (e.g., 100MB)

# Initialize the Flask secret key
app.secret_key = os.urandom(24)

# Database configuration
DB_PATH = 'database.db'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def connect_db():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()

    # Convert video data to strings
    videos = [(video[0], str(video[1]), video[2], str(video[3])) for video in videos]

    print("Videos data:", videos)  # Debugging statement
    return render_template('index.html', videos=videos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials for admin user
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['user_id'] = 1
            session['username'] = username
            return redirect(url_for('index'))
        
        # Add regular user login logic here
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username is already taken
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            return "Username already taken, please choose a different one."
        
        # Hash the password and store the user in the database
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        file = request.files['file']

        if file and allowed_file(file.filename):
            # Secure the title to use as the file name
            filename = secure_filename(title + os.path.splitext(file.filename)[1])  # Ensure the file extension stays the same
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(session['user_id']))  # Create user-specific folder

            # Create the folder if it doesn't exist
            if not os.path.exists(user_folder):
                os.makedirs(user_folder)

            file_path = os.path.join(user_folder, filename)
            file.save(file_path)

            # Save the file path relative to 'static'
            video_path = os.path.join('static', 'uploads', str(session['user_id']), filename)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO videos (user_id, title, video_path) VALUES (?, ?, ?)",
                           (session['user_id'], title, video_path))
            conn.commit()
            conn.close()

            return redirect(url_for('index'))

    return render_template('upload.html')


@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('username') != ADMIN_USERNAME:
        return redirect(url_for('index'))  # Ensure that only the admin can access this page

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos")
    videos = cursor.fetchall()
    conn.close()

    return render_template('admin.html', videos=videos)

@app.route('/delete_video/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    user_id = session['user_id']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch the video path from the database
    cursor.execute('SELECT video_path FROM videos WHERE id = ? AND user_id = ?', (video_id, user_id))
    video = cursor.fetchone()

    if video:
        # Extract the file path
        video_path = video[0]

        # Remove the video file from the server
        if os.path.exists(video_path):
            os.remove(video_path)

        # Delete video from the database
        cursor.execute('DELETE FROM videos WHERE id = ? AND user_id = ?', (video_id, user_id))
        conn.commit()

    conn.close()

    return redirect(url_for('manage'))  # Redirect back to the manage page
    
@app.route('/delete_video_admin/<int:video_id>', methods=['POST'])
def delete_video_admin(video_id):
    if 'username' not in session or session.get('username') != ADMIN_USERNAME:
        return redirect(url_for('index'))  # Ensure that only the admin can access this page

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch the video path from the database
    cursor.execute('SELECT video_path FROM videos WHERE id = ?', (video_id,))
    video = cursor.fetchone()

    if video:
        # Extract the file path
        video_path = video[0]

        # Remove the video file from the server
        if os.path.exists(video_path):
            os.remove(video_path)

        # Delete video from the database
        cursor.execute('DELETE FROM videos WHERE id = ?', (video_id,))
        conn.commit()

    conn.close()

    return redirect(url_for('admin'))  # Redirect back to the admin page
    
@app.route('/manage')
def manage():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    # Get user ID from session and fetch videos for that user
    user_id = session['user_id']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get all videos uploaded by the user
    cursor.execute('SELECT * FROM videos WHERE user_id = ?', (user_id,))
    videos = cursor.fetchall()

    conn.close()

    return render_template('manage.html', videos=videos)    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/video/<int:video_id>')
def video(video_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch the video information based on video_id
    cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
    video = cursor.fetchone()

    if video:
        # Fetch the username based on user_id (assuming video[1] is user_id)
        cursor.execute("SELECT username FROM users WHERE id = ?", (video[1],))
        user = cursor.fetchone()

        if user:
            # Construct the correct video URL
            video_path = video[3]  # e.g., 'static/uploads/1/test_video.mp4'
            title = video[2]  # Video title
            username = user[0]  # Username

            # Normalize path: convert backslashes to forward slashes
            video_path = video_path.replace('\\', '/')

            # Remove 'static/' from the beginning of the path
            relative_video_path = video_path.lstrip('static/')

            return render_template("video.html", video_path=relative_video_path, title=title, username=username)
        else:
            return redirect(url_for('engine'))  # Redirect to engine.html if user not found
    else:
        return redirect(url_for('engine'))  # Redirect to engine.html if video not found
        
@app.route('/engine')
def engine():
    return render_template('engine.html')        

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
