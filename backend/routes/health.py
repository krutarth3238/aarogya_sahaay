from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, HealthRecord, Appointment
from datetime import datetime
import json

health_bp = Blueprint('health', __name__)

@health_bp.route('/records', methods=['POST'])
@jwt_required()
def create_health_record():
    """Create a new health record"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        # Create health record
        record = HealthRecord(
            patient_id=data.get('patient_id', user_id),
            recorded_by=user_id,
            blood_pressure_systolic=data.get('blood_pressure_systolic'),
            blood_pressure_diastolic=data.get('blood_pressure_diastolic'),
            heart_rate=data.get('heart_rate'),
            temperature=data.get('temperature'),
            weight=data.get('weight'),
            height=data.get('height'),
            symptoms=data.get('symptoms'),
            notes=data.get('notes')
        )

        db.session.add(record)
        db.session.flush()

        # AI Health Risk Prediction
        try:
            if current_app.health_predictor:
                prediction_result = current_app.health_predictor.predict_risk(record)
                record.risk_score = prediction_result['risk_score']
                record.risk_level = prediction_result['risk_level']
                record.ai_recommendations = json.dumps(prediction_result['recommendations'])
        except Exception as e:
            print(f"AI prediction failed: {e}")
            record.risk_level = 'unknown'

        db.session.commit()

        return jsonify({
            'message': 'Health record created successfully',
            'record': record.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@health_bp.route('/records', methods=['GET'])
@jwt_required()
def get_health_records():
    """Get health records for a patient"""
    try:
        user_id = get_jwt_identity()
        patient_id = request.args.get('patient_id', user_id)

        # Check if user can access these records
        current_user = User.query.get(user_id)
        if current_user.role != 'asha' and patient_id != user_id:
            return jsonify({'error': 'Access denied'}), 403

        records = HealthRecord.query.filter_by(patient_id=patient_id).order_by(
            HealthRecord.recorded_at.desc()
        ).limit(20).all()

        return jsonify({
            'records': [record.to_dict() for record in records]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@health_bp.route('/appointments', methods=['POST'])
@jwt_required()
def book_appointment():
    """Book an appointment"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        appointment = Appointment(
            patient_id=user_id,
            appointment_date=datetime.fromisoformat(data['appointment_date']),
            appointment_type=data['appointment_type'],
            location=data.get('location'),
            notes=data.get('notes')
        )

        db.session.add(appointment)
        db.session.commit()

        return jsonify({
            'message': 'Appointment booked successfully',
            'appointment': appointment.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@health_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)

        if current_user.role == 'patient':
            # Patient stats
            total_records = HealthRecord.query.filter_by(patient_id=user_id).count()
            recent_record = HealthRecord.query.filter_by(patient_id=user_id).order_by(
                HealthRecord.recorded_at.desc()
            ).first()

            stats = {
                'total_health_records': total_records,
                'recent_vitals': recent_record.to_dict() if recent_record else None,
                'risk_level': recent_record.risk_level if recent_record else 'unknown'
            }
        else:
            # ASHA/Admin stats
            stats = {
                'total_patients': User.query.filter_by(role='patient').count(),
                'total_records': HealthRecord.query.count(),
                'high_risk_patients': HealthRecord.query.filter_by(risk_level='high').count()
            }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
