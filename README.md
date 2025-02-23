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
   git clone https://github.com/QKing-Official/LightHub.git
```

2.  pip install -r requirements.txt (or run the .bat/.sh file)
    
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
LightHub
├── app.py #The main application that handles the backend and connects it to the frontend.
├── db.py #The file to set up the database.
├── (database.db) #This file will appear after you ran db.py.
├── start.bat #simplified requirements instalation and running for windows based systems.
├── start.sh #simplified requirements installation and running for linux based systems.
├── static #This folder contains the uploads of the users and the favicon.ico.
│   ├── favicon.ico #The image on the webbrowser tab.
│   └── uploads #The folder with all the uploads of the users.
│       └── 1 #The first userID. The server makes more when needed.
│           └── test_video.mp4 #The default test video.
└── templates #All the pages of the site
    ├── admin.html #(password protected) The admin panel where admins can delete videos. Only accesible from admin account.
    ├── engine.html #The page where information about the video engine is displayed and you get redirected to when the video url is incorrect.
    ├── index.html #The landing page with videos listed.
    ├── login.html #The page where you can login.
    ├── manage.html #The page where video owners can delete their videos.
    ├── signup.html #The page where you can signup.
    ├── styles.css #The styles for the website. (I think its not used anymore, but I'll keep it here in case it's needed.
    ├── upload.html #The page where users can upload videos. Only logged in users can upload videos.
    └── video.html #The engine that renders videos.
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
 
    *  To acces the Admin Panel, go to http://127.0.0.1:5000/admin. (You need to be logged in as Admin, <ins>admin</ins> is default username with <ins>adminpassword</ins> as password).
    
    *   The Admin Panel is available for admins to manage all content.
        
    *   Admins can delete any video that violates the platform's policies or for general management purposes.
        

Contributing
------------

Contributions to LightHub are welcome! Feel free to fork the repository, submit pull requests, or suggest improvements
