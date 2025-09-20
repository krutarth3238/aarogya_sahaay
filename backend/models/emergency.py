from datetime import datetime
import uuid
from .database import db

class EmergencyAlert(db.Model):
    __tablename__ = 'emergency_alerts'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Emergency Details
    alert_type = db.Column(db.String(50), nullable=False)  # medical, accident, disaster
    severity = db.Column(db.String(10), nullable=False)  # low, medium, high, critical
    description = db.Column(db.Text, nullable=True)

    # Location
    location_lat = db.Column(db.Float, nullable=True)
    location_lng = db.Column(db.Float, nullable=True)
    address = db.Column(db.String(255), nullable=True)

    # Response
    status = db.Column(db.String(20), default='active')  # active, responded, resolved
    responder_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    response_time = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    resolved_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'description': self.description,
            'location': {
                'lat': self.location_lat,
                'lng': self.location_lng,
                'address': self.address
            },
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }
