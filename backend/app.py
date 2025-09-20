import os
import logging
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from datetime import datetime, timedelta
import redis

# Import blueprints
from routes.auth import auth_bp
from routes.health import health_bp
from routes.emergency import emergency_bp
from routes.communication import communication_bp
from routes.admin import admin_bp
from models.database import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    # Redis for caching and real-time features
    try:
        redis_client = redis.Redis(
            host=app.config['REDIS_HOST'], 
            port=app.config['REDIS_PORT'], 
            decode_responses=True
        )
        app.redis = redis_client
    except Exception as e:
        print(f"Redis connection failed: {e}")
        app.redis = None

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    app.register_blueprint(emergency_bp, url_prefix='/api/emergency')
    app.register_blueprint(communication_bp, url_prefix='/api/communication')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Health prediction AI service
    from services.ai_prediction import HealthPredictionService
    app.health_predictor = HealthPredictionService()

    # Communication services
    from services.whatsapp_service import WhatsAppService
    from services.sms_service import SMSService
    app.whatsapp = WhatsAppService()
    app.sms = SMSService()

    @app.route('/')
    def index():
        return jsonify({
            'message': 'Aarogya Sahayak Backend API',
            'version': '1.0.0',
            'status': 'running',
            'timestamp': datetime.utcnow().isoformat(),
            'endpoints': {
                'auth': '/api/auth/*',
                'health': '/api/health/*',
                'emergency': '/api/emergency/*',
                'communication': '/api/communication/*',
                'admin': '/api/admin/*'
            }
        })

    @app.route('/api/health-check')
    def health_check():
        try:
            # Test database connection
            db.session.execute('SELECT 1')

            # Test Redis connection
            redis_status = 'connected' if app.redis and app.redis.ping() else 'disconnected'

            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'redis': redis_status,
                'timestamp': datetime.utcnow().isoformat()
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }), 500

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()

    # Create tables
    with app.app_context():
        db.create_all()

    # Run with SocketIO for real-time features
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
