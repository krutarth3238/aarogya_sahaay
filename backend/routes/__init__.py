from .auth import auth_bp
from .health import health_bp
from .emergency import emergency_bp
from .communication import communication_bp
from .admin import admin_bp

__all__ = ['auth_bp', 'health_bp', 'emergency_bp', 'communication_bp', 'admin_bp']
