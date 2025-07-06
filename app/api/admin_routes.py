from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.admin import Admin
from flask_jwt_extended import create_access_token, jwt_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_admins():
    admins = Admin.query.all()
    return jsonify([{
        'id': admin.id,
        'name': admin.name,
        'username': admin.username,
        'email': admin.email,
        'created_at': admin.created_at
    } for admin in admins]), 200

@admin_bp.route('/', methods=['POST'])
def create_admin():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([name, username, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    if Admin.query.filter((Admin.username == username) | (Admin.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    admin = Admin(name=name, username=username, email=email)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()

    access_token = create_access_token(identity=admin.id)
    return jsonify({
        'message': 'Admin created successfully',
        'admin_id': admin.id,
        'token': access_token,
        'user': {
            'id': admin.id,
            'username': admin.username,
            'fullname': admin.name,
            'email': admin.email,
            'role': 'admin'
        }
    }), 201
@admin_bp.route('/<int:admin_id>', methods=['GET'])
@jwt_required()
def get_admin(admin_id):
    admin = Admin.query.get(admin_id)
    if not admin:
        return jsonify({'error': 'Admin not found'}), 404

    return jsonify({
        'id': admin.id,
        'name': admin.name,
        'username': admin.username,
        'email': admin.email,
        'created_at': admin.created_at
    }), 200
