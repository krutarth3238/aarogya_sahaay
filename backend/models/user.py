from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .database import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    phone_number = db.Column(db.String(15), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profile Information
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    profile_photo = db.Column(db.String(255), nullable=True)

    # Role and Location
    role = db.Column(db.String(20), nullable=False, default='patient')  # patient, asha, admin
    village = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)

    # Preferences
    preferred_language = db.Column(db.String(5), default='hi')
    emergency_contact = db.Column(db.String(15), nullable=True)

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    health_records = db.relationship('HealthRecord', backref='patient', lazy='dynamic')
    appointments = db.relationship('Appointment', backref='patient', lazy='dynamic')
    emergency_alerts = db.relationship('EmergencyAlert', backref='patient', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'village': self.village,
            'district': self.district,
            'preferred_language': self.preferred_language,
            'profile_photo': self.profile_photo,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
