#!/usr/bin/env python3
"""
Alternative entry point for the Aarogya Sahayak Flask application.
Use this for development or when you want to run with different configurations.
"""

import os
from app import create_app

if __name__ == '__main__':
    app, socketio = create_app()

    # Get configuration from environment
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'

    print(f"Starting Aarogya Sahayak Backend on {host}:{port}")
    print(f"Debug mode: {debug}")

    # Initialize database tables
    with app.app_context():
        from models import db
        db.create_all()
        print("Database tables created/verified")

    # Run the application
    socketio.run(app, host=host, port=port, debug=debug)
