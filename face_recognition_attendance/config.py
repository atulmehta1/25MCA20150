import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_change_me_in_production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Models directories
    MODEL_DIR = BASE_DIR / 'static' / 'models'
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Face Recognition Thresholds (SFace cosine similarity benchmark is 0.363 - 0.40)
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', '0.50'))
    MATCH_THRESHOLD = float(os.getenv('MATCH_THRESHOLD', '0.40'))

    # Database Configuration (SQLite)
    DB_TYPE = 'sqlite'
    SQLITE_DB_NAME = os.getenv('SQLITE_DB_NAME', 'attendance.db')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{(BASE_DIR / SQLITE_DB_NAME).as_posix()}"
