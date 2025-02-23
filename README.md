# LightHub

**LightHub** is a Python-based YouTube clone built using Flask. It allows users to upload, manage, and view videos, with an intuitive and modern interface. The platform also includes an **Admin Panel** for managing uploaded content. It supports video uploads, video playback, and user management functionality. This project is built with Flask, SQLite, and a custom backend for user authentication and video handling.

---

## Features

- **User Authentication**: Users can sign up, log in, and log out.
- **Video Upload**: Logged-in users can upload videos.
- **Manage Videos**: Users can manage their uploaded videos through the interface.
- **Video Playback**: Users can watch videos uploaded by others in a player interface.
- **Admin Panel**: Admins can manage all uploaded videos, including deletion.

---

## Requirements

- Python 3.7 or higher
- Flask
- SQLite (used as the database for simplicity)
- HTML, CSS, and JavaScript for the frontend

---

## Installation

1. **Clone the repository:**
```bash
   git clone https://github.com/your-username/light-hub.git
```

2.  pip install -r requirements.txt
    
2.  **Set up the database:** SQLite is used for the database. Run db.py too set up the database.
```bash
python db.py
```
     
3. Run LightHub
```bash
python app.py
```

The app should now be running on http://127.0.0.1:5000.

---    

Folder Structure
----------------
```ruby
light-hub/
│
├── static/                    # Contains static files such as images, videos, and CSS
│   ├── uploads/               # Directory where uploaded videos are stored
│   └── favicon.ico            # Application icon
│
├── templates/                  # HTML templates for rendering content
│   ├── video.html             # Template for individual video pages
│   └── engine.html            # Information about the LightHub Engine
│
├── app.py                      # Main Flask application file
├── requirements.txt            # List of required Python packages
└── create_db.py                # (Optional) A script to create the SQLite database
```

---

How to Use
----------

1.  **Sign Up / Log In:**
    
    *   Visit the homepage, sign up for an account or log in if you already have one.
        
2.  **Upload Video:**
    
    *   After logging in, you can upload videos by clicking on the "Upload Video" link in the navbar.
        
    *   Provide a title for the video and upload the video file.
        
3.  **Manage Videos:**
    
    *   Once you've uploaded videos, you can manage them through the "Manage Videos" section.
        
    *   The admin panel allows you to delete videos if necessary.
        
4.  **Watch Videos:**
    
    *   Navigate to the main page, where you can watch videos uploaded by users.
        

Admin Panel
-----------

*   **Accessing the Admin Panel:**
    
    *   The Admin Panel is available for admins to manage all content.
        
    *   Admins can delete any video that violates the platform's policies or for general management purposes.
        

Contributing
------------

Contributions to LightHub are welcome! Feel free to fork the repository, submit pull requests, or suggest improvements
