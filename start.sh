#!/bin/bash

# Install Flask
pip install flask

# Run the database script and then the application
python db.py && python app.py