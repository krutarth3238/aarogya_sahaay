import os
from datetime import timedelta

class Config:
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///aarogya_sahayak.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # Redis Config
    REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
    REDIS_PORT = int(os.environ.get('REDIS_PORT') or 6379)

    # File Upload Config
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

    # WhatsApp API Config
    WHATSAPP_API_URL = os.environ.get('WHATSAPP_API_URL') or 'https://graph.facebook.com/v18.0'
    WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')
    WHATSAPP_PHONE_ID = os.environ.get('WHATSAPP_PHONE_ID')

    # SMS API Config (Twilio)
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')

    # AI/ML Config
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

    # Emergency Services Config
    EMERGENCY_HOTLINE = '108'  # India Emergency Number
    AMBULANCE_API_URL = os.environ.get('AMBULANCE_API_URL')

    # Multilingual Config
    LANGUAGES = ['en', 'hi', 'bn', 'te', 'ta']  # English, Hindi, Bengali, Telugu, Tamil

    # Health Prediction Config
    PREDICTION_MODEL_PATH = 'models/health_prediction_model.pkl'
    RISK_THRESHOLD_HIGH = 0.8
    RISK_THRESHOLD_MEDIUM = 0.5

    # Logging Config
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
