from flask import Blueprint, request, jsonify
from app.services.auth_utils import authenticate_admin
from app.models.admin import Admin
from app.extensions import db
from app.services.mail_service import generate_reset_token, send_reset_email
from flask_jwt_extended import create_access_token
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/reset-request', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({'error': 'No account associated with this email'}), 404

    url = generate_reset_token(admin)
    send_reset_email(admin.email, url)
    return jsonify({'message': 'Password reset email sent'}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({'error': 'Password is required'}), 400

    admin = Admin.query.filter_by(reset_token=token).first()
    if not admin or admin.token_time < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired token'}), 400

    admin.set_password(new_password)
    admin.reset_token = None
    admin.token_time = None
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username') or data.get('email')
    password = data.get('password')

    if not username_or_email or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    admin = authenticate_admin(username_or_email, password)
    if admin:
        access_token = create_access_token(identity=admin.id)
        return jsonify({
            'token': access_token,
            'user': {
                'id': admin.id,
                'username': admin.username,
                'fullName': admin.name,
                'email': admin.email,
                'role': 'admin',
                'last_login': admin.last_login,
                'login_count': admin.login_count
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid username/email or password'}), 401
