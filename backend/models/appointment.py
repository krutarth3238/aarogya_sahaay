from datetime import datetime
import uuid
from .database import db

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    asha_worker_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)

    # Appointment Details
    appointment_date = db.Column(db.DateTime, nullable=False, index=True)
    appointment_type = db.Column(db.String(50), nullable=False)  # checkup, vaccination, emergency
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled

    # Location and Notes
    location = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    reminder_sent = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'appointment_date': self.appointment_date.isoformat(),
            'appointment_type': self.appointment_type,
            'status': self.status,
            'location': self.location,
            'notes': self.notes
        }
