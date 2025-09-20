from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from models import db, User
from datetime import datetime
import re
import os
from werkzeug.utils import secure_filename
import uuid

auth_bp = Blueprint('auth', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user (Patient or ASHA worker)"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['phone_number', 'password', 'full_name', 'role']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Validate phone number format (Indian)
        phone_pattern = r'^[6-9]\d{9}$'
        if not re.match(phone_pattern, data['phone_number']):
            return jsonify({'error': 'Invalid Indian phone number format'}), 400

        # Validate role
        if data['role'] not in ['patient', 'asha']:
            return jsonify({'error': 'Role must be patient or asha'}), 400

        # Check if user already exists
        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify({'error': 'Phone number already registered'}), 409

        # Create new user
        user = User(
            phone_number=data['phone_number'],
            full_name=data['full_name'],
            role=data['role'],
            email=data.get('email'),
            date_of_birth=datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date() if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            village=data.get('village'),
            district=data.get('district'),
            state=data.get('state', 'Maharashtra'),
            pincode=data.get('pincode'),
            preferred_language=data.get('preferred_language', 'hi'),
            emergency_contact=data.get('emergency_contact')
        )

        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Send welcome SMS
        try:
            welcome_message = f"स्वागत है {user.full_name}! आरोग्य सहायक में आपका पंजीकरण सफल हुआ। आपका स्वास्थ्य हमारी प्राथमिकता है।"
            if current_app.sms:
                current_app.sms.send_sms(user.phone_number, welcome_message)
        except Exception as e:
            print(f"Welcome SMS failed: {e}")

        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login with phone number and password"""
    try:
        data = request.get_json()

        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not password:
            return jsonify({'error': 'Phone number and password required'}), 400

        # Find user
        user = User.query.filter_by(phone_number=phone_number).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401

        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401

        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Create JWT tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/upload-photo', methods=['POST'])
@jwt_required()
def upload_profile_photo():
    """Upload profile photo"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if 'photo' not in request.files:
            return jsonify({'error': 'No photo file provided'}), 400

        file = request.files['photo']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if file and allowed_file(file.filename):
            # Create uploads directory if it doesn't exist
            upload_dir = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            # Generate unique filename
            file_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
            file_path = os.path.join(upload_dir, filename)

            # Save file
            file.save(file_path)

            # Update user profile photo path
            user.profile_photo = f"/uploads/{filename}"
            user.updated_at = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'message': 'Profile photo uploaded successfully',
                'profile_photo': user.profile_photo
            }), 200

        return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-phone', methods=['POST'])
def verify_phone():
    """Send OTP for phone verification"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')

        if not phone_number:
            return jsonify({'error': 'Phone number required'}), 400

        # Generate 6-digit OTP
        import random
        otp = str(random.randint(100000, 999999))

        # Store OTP in Redis with 5-minute expiration
        if current_app.redis:
            current_app.redis.setex(f"otp:{phone_number}", 300, otp)

        # Send OTP via SMS
        message = f"आपका आरोग्य सहायक OTP: {otp}। यह 5 मिनट में समाप्त हो जाएगा।"
        if current_app.sms:
            current_app.sms.send_sms(phone_number, message)
        else:
            print(f"OTP for {phone_number}: {otp}")  # For development

        return jsonify({
            'message': 'OTP sent successfully',
            'expires_in': 300  # 5 minutes
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP for phone verification"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        otp = data.get('otp')

        if not phone_number or not otp:
            return jsonify({'error': 'Phone number and OTP required'}), 400

        # Get stored OTP from Redis
        stored_otp = None
        if current_app.redis:
            stored_otp = current_app.redis.get(f"otp:{phone_number}")

        if not stored_otp:
            return jsonify({'error': 'OTP expired or not found'}), 400

        if stored_otp != otp:
            return jsonify({'error': 'Invalid OTP'}), 400

        # Mark user as verified if they exist
        user = User.query.filter_by(phone_number=phone_number).first()
        if user:
            user.is_verified = True
            db.session.commit()

        # Delete used OTP
        if current_app.redis:
            current_app.redis.delete(f"otp:{phone_number}")

        return jsonify({
            'message': 'Phone number verified successfully'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
