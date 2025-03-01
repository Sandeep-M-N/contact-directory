# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/contact_directory")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
