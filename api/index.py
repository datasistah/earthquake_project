import os
import sys
# Path to include Flask
sys.path.insert(0, os.path.dirname(__file__))

# Import the Flask app from app.py
from app import app

# For Vercel serverless function
handler = app
