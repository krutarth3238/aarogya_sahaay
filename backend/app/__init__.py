from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, ma
from app.config import config


def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    # No ma.init_app(app) call here
    
    # Enable CORS
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Register blueprints and routes
    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
