import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-stock-ai-key-2026-secure')
    
    # SQLite default, or use MySQL if MYSQL_URL is set
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(BASE_DIR, 'stock_system.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder for custom datasets
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'datasets', 'uploads')
    DATASET_FOLDER = os.path.join(BASE_DIR, 'datasets')
    MODELS_DIR = os.path.join(BASE_DIR, 'models_saved')
    
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max upload
    ALLOWED_EXTENSIONS = {'csv', 'txt'}
    
    # Pre-configured stocks
    SUPPORTED_STOCKS = {
        'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'currency': 'USD'},
        'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology', 'currency': 'USD'},
        'GOOGL': {'name': 'Alphabet Inc. (Google)', 'sector': 'Communication Services', 'currency': 'USD'},
        'TSLA': {'name': 'Tesla Inc.', 'sector': 'Consumer Cyclical', 'currency': 'USD'},
        'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Consumer Cyclical', 'currency': 'USD'},
        'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Semiconductors', 'currency': 'USD'},
    }
