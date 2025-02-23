import sqlite3
import os

# Database file path
DB_PATH = 'database.db'
UPLOAD_FOLDER = 'static/uploads/'  # Ensure videos are stored correctly

def create_tables():
    """Initialize database and create necessary tables if they do not exist."""
    # Ensure the database exists
    if not os.path.exists(DB_PATH):
        open(DB_PATH, 'w').close()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Create `users` table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        ''')

        # Create `videos` table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            video_path TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        ''')

        conn.commit()
    
    print(f"✅ Database '{DB_PATH}' initialized and tables created.")

def insert_sample_data():
    """Insert a sample user and video for testing if the tables are empty."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if there's any user data already
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]

        if user_count == 0:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?);", ("test_user", "password123"))
            conn.commit()
            print("✅ Sample user added: test_user")

        # Get the user ID
        cursor.execute("SELECT id FROM users WHERE username = ?;", ("test_user",))
        user_id = cursor.fetchone()[0]

        # Check if video data exists
        cursor.execute("SELECT COUNT(*) FROM videos;")
        video_count = cursor.fetchone()[0]

        if video_count == 0:
            sample_video_path = os.path.join(UPLOAD_FOLDER, f"{user_id}/test_video.mp4")

            # Ensure the directory exists
            user_video_folder = os.path.dirname(sample_video_path)
            os.makedirs(user_video_folder, exist_ok=True)

            cursor.execute("INSERT INTO videos (user_id, title, video_path) VALUES (?, ?, ?);", 
                           (user_id, "Sample Video", sample_video_path))
            conn.commit()
            print(f"✅ Sample video added: {sample_video_path}")

if __name__ == "__main__":
    create_tables()
    insert_sample_data()
