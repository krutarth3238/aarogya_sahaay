from datetime import datetime
import uuid
from .database import db

class CommunicationLog(db.Model):
    __tablename__ = 'communication_logs'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Communication Details
    type = db.Column(db.String(20), nullable=False)  # whatsapp, sms, email
    recipient = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, sent, delivered, failed

    # Metadata
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    delivered_at = db.Column(db.DateTime, nullable=True)
    external_id = db.Column(db.String(100), nullable=True)  # ID from WhatsApp/SMS provider

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'recipient': self.recipient,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }
