from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

communication_bp = Blueprint('communication', __name__)

@communication_bp.route('/whatsapp/send', methods=['POST'])
@jwt_required()
def send_whatsapp_message():
    """Send WhatsApp message"""
    try:
        data = request.get_json()
        recipient = data.get('recipient')
        message = data.get('message')

        if not recipient or not message:
            return jsonify({'error': 'Recipient and message required'}), 400

        success = False
        if current_app.whatsapp:
            success = current_app.whatsapp.send_message(recipient, message)

        return jsonify({
            'message': 'WhatsApp message sent' if success else 'Message failed',
            'success': success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/sms/send', methods=['POST'])
@jwt_required()
def send_sms_message():
    """Send SMS message"""
    try:
        data = request.get_json()
        recipient = data.get('recipient')
        message = data.get('message')

        if not recipient or not message:
            return jsonify({'error': 'Recipient and message required'}), 400

        success = False
        if current_app.sms:
            success = current_app.sms.send_sms(recipient, message)

        return jsonify({
            'message': 'SMS sent' if success else 'SMS failed',
            'success': success
        }), 200 if success else 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@communication_bp.route('/broadcast', methods=['POST'])
@jwt_required()
def broadcast_message():
    """Broadcast health message to community"""
    try:
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)

        if current_user.role not in ['asha', 'admin']:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({'error': 'Message required'}), 400

        # Get patients in the area
        patients = User.query.filter_by(
            village=current_user.village,
            role='patient'
        ).all()

        recipients = [p.phone_number for p in patients]

        # Send messages
        sms_results = []
        whatsapp_results = []

        if current_app.sms:
            sms_results = current_app.sms.send_bulk_sms(recipients, message)

        if current_app.whatsapp:
            whatsapp_results = current_app.whatsapp.send_bulk_message(recipients, message)

        return jsonify({
            'message': 'Broadcast sent',
            'recipients_count': len(recipients),
            'sms_results': sms_results,
            'whatsapp_results': whatsapp_results
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
