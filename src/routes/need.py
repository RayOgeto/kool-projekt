from flask import *
from flask_login import login_required, current_user
from src.models.user import db
from src.models.need import Need
from src.models.donation import Donation

need_bp = Blueprint('need', __name__)

@need_bp.route('/needs', methods=['GET'])
def get_needs():
    """Get all active needs with optional filtering"""
    category = request.args.get('category')
    urgency = request.args.get('urgency')
    status = request.args.get('status', 'active')
    
    query = Need.query
    
    if category:
        query = query.filter(Need.category == category)
    if urgency:
        query = query.filter(Need.urgency_level == urgency)
    if status:
        query = query.filter(Need.status == status)
    
    needs = query.order_by(Need.created_at.desc()).all()
    return jsonify([need.to_dict() for need in needs])

@need_bp.route('/needs', methods=['POST'])
@login_required
def create_need():
    """Create a new need (only recipients can create needs)"""
    if current_user.user_type != 'recipient':
        return jsonify({'error': 'Only recipients can create needs'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'description', 'category']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate category
    valid_categories = ['food', 'clothing', 'shelter', 'medical', 'education', 'transport', 'other']
    if data['category'] not in valid_categories:
        return jsonify({'error': 'Invalid category'}), 400
    
    # Validate urgency level
    valid_urgency = ['low', 'medium', 'high', 'critical']
    urgency = data.get('urgency_level', 'medium')
    if urgency not in valid_urgency:
        return jsonify({'error': 'Invalid urgency level'}), 400
    
    need = Need(
        title=data['title'].strip(),
        description=data['description'].strip(),
        category=data['category'],
        urgency_level=urgency,
        amount_needed=data.get('amount_needed'),
        unit=data.get('unit'),
        location=data.get('location'),
        recipient_id=current_user.id
    )
    
    db.session.add(need)
    db.session.commit()
    
    return jsonify(need.to_dict()), 201

@need_bp.route('/needs/<int:need_id>', methods=['GET'])
def get_need(need_id):
    """Get a specific need"""
    need = Need.query.get_or_404(need_id)
    return jsonify(need.to_dict())

@need_bp.route('/needs/<int:need_id>', methods=['PUT'])
@login_required
def update_need(need_id):
    """Update a need (only the creator or admin can update)"""
    need = Need.query.get_or_404(need_id)
    
    if current_user.id != need.recipient_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'title' in data:
        need.title = data['title'].strip()
    if 'description' in data:
        need.description = data['description'].strip()
    if 'category' in data:
        valid_categories = ['food', 'clothing', 'shelter', 'medical', 'education', 'transport', 'other']
        if data['category'] in valid_categories:
            need.category = data['category']
    if 'urgency_level' in data:
        valid_urgency = ['low', 'medium', 'high', 'critical']
        if data['urgency_level'] in valid_urgency:
            need.urgency_level = data['urgency_level']
    if 'status' in data:
        valid_status = ['active', 'fulfilled', 'cancelled']
        if data['status'] in valid_status:
            need.status = data['status']
    if 'amount_needed' in data:
        need.amount_needed = data['amount_needed']
    if 'unit' in data:
        need.unit = data['unit']
    if 'location' in data:
        need.location = data['location']
    
    db.session.commit()
    return jsonify(need.to_dict())

@need_bp.route('/needs/<int:need_id>', methods=['DELETE'])
@login_required
def delete_need(need_id):
    """Delete a need (only the creator or admin can delete)"""
    need = Need.query.get_or_404(need_id)
    
    if current_user.id != need.recipient_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(need)
    db.session.commit()
    return '', 204

@need_bp.route('/my-needs', methods=['GET'])
@login_required
def get_my_needs():
    """Get current user's needs"""
    needs = Need.query.filter_by(recipient_id=current_user.id).order_by(Need.created_at.desc()).all()
    return jsonify([need.to_dict() for need in needs]) 