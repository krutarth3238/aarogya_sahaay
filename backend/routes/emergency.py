from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, EmergencyAlert
from datetime import datetime

emergency_bp = Blueprint('emergency', __name__)

@emergency_bp.route('/alert', methods=['POST'])
@jwt_required()
def create_emergency_alert():
    """Create emergency alert"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        alert = EmergencyAlert(
            patient_id=user_id,
            alert_type=data.get('alert_type', 'medical'),
            severity=data.get('severity', 'high'),
            description=data.get('description'),
            location_lat=data.get('location_lat'),
            location_lng=data.get('location_lng'),
            address=data.get('address')
        )

        db.session.add(alert)
        db.session.commit()

        # Get patient information
        patient = User.query.get(user_id)

        # Send emergency notifications
        if patient.emergency_contact:
            try:
                message = f"🚨 आपातकाल: {patient.full_name} को तत्काल सहायता चाहिए। स्थान: {alert.address or 'GPS shared'}"
                if current_app.sms:
                    current_app.sms.send_sms(patient.emergency_contact, message)
                if current_app.whatsapp:
                    current_app.whatsapp.send_message(patient.emergency_contact, message)
            except Exception as e:
                print(f"Emergency notification failed: {e}")

        return jsonify({
            'message': 'Emergency alert created successfully',
            'alert': alert.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@emergency_bp.route('/alerts', methods=['GET'])
@jwt_required()
def get_emergency_alerts():
    """Get emergency alerts"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)

        if current_user.role == 'patient':
            alerts = EmergencyAlert.query.filter_by(patient_id=user_id).order_by(
                EmergencyAlert.created_at.desc()
            ).all()
        else:
            # ASHA/Admin sees all alerts
            alerts = EmergencyAlert.query.order_by(
                EmergencyAlert.created_at.desc()
            ).limit(50).all()

        return jsonify({
            'alerts': [alert.to_dict() for alert in alerts]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
