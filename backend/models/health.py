from datetime import datetime
import uuid
from .database import db

class HealthRecord(db.Model):
    __tablename__ = 'health_records'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    recorded_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)

    # Vital Signs
    blood_pressure_systolic = db.Column(db.Integer, nullable=True)
    blood_pressure_diastolic = db.Column(db.Integer, nullable=True)
    heart_rate = db.Column(db.Integer, nullable=True)
    temperature = db.Column(db.Float, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    oxygen_saturation = db.Column(db.Float, nullable=True)

    # Symptoms and Notes
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    # AI Predictions
    risk_score = db.Column(db.Float, nullable=True)
    risk_level = db.Column(db.String(10), nullable=True)  # low, medium, high
    ai_recommendations = db.Column(db.Text, nullable=True)

    # Metadata
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'blood_pressure': f"{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}" if self.blood_pressure_systolic else None,
            'heart_rate': self.heart_rate,
            'temperature': self.temperature,
            'weight': self.weight,
            'symptoms': self.symptoms,
            'risk_level': self.risk_level,
            'risk_score': self.risk_score,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }
