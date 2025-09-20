from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, HealthRecord
from functools import wraps

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role not in ['admin', 'asha']:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_dashboard_stats():
    """Get admin dashboard statistics"""
    try:
        stats = {
            'total_users': User.query.count(),
            'total_patients': User.query.filter_by(role='patient').count(),
            'total_asha_workers': User.query.filter_by(role='asha').count(),
            'total_health_records': HealthRecord.query.count(),
            'high_risk_patients': HealthRecord.query.filter_by(risk_level='high').count()
        }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    """Get list of users"""
    try:
        role = request.args.get('role')
        query = User.query

        if role:
            query = query.filter_by(role=role)

        users = query.limit(100).all()

        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
