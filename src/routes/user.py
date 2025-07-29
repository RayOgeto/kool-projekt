from flask import *
from flask_login import login_required, current_user
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@login_required
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name', 'user_type']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        email=data['email'].lower().strip(),
        first_name=data['first_name'].strip(),
        last_name=data['last_name'].strip(),
        phone_number=data.get('phone_number', '').strip(),
        user_type=data['user_type']
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # Only allow users to update their own profile or admin to update any
    if current_user.id != user_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Update fields
    if 'first_name' in data:
        user.first_name = data['first_name'].strip()
    if 'last_name' in data:
        user.last_name = data['last_name'].strip()
    if 'phone_number' in data:
        user.phone_number = data['phone_number'].strip()
    if 'user_type' in data and current_user.user_type == 'admin':
        user.user_type = data['user_type']
    
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Only allow users to delete their own account or admin to delete any
    if current_user.id != user_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(user)
    db.session.commit()
    return '', 204

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify(current_user.to_dict())