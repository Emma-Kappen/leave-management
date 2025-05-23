import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use SQLite for testing, can be changed to MySQL later
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///leave_mgmt.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "secret-key")

