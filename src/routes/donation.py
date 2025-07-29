from flask import *
from flask_login import login_required, current_user
from src.models.user import db
from src.models.need import Need
from src.models.donation import Donation

donation_bp = Blueprint('donation', __name__)

@donation_bp.route('/donations', methods=['GET'])
@login_required
def get_donations():
    """Get all donations (filtered by user role)"""
    if current_user.user_type == 'admin':
        # Admin can see all donations
        donations = Donation.query.order_by(Donation.created_at.desc()).all()
    else:
        # Users can only see their own donations
        donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.created_at.desc()).all()
    
    return jsonify([donation.to_dict() for donation in donations])

@donation_bp.route('/donations', methods=['POST'])
@login_required
def create_donation():
    """Create a new donation (only donors can create donations)"""
    if current_user.user_type != 'donor':
        return jsonify({'error': 'Only donors can create donations'}), 403
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['amount', 'donation_type', 'need_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate donation type
    valid_types = ['monetary', 'goods', 'services']
    if data['donation_type'] not in valid_types:
        return jsonify({'error': 'Invalid donation type'}), 400
    
    # Check if need exists and is active
    need = Need.query.get(data['need_id'])
    if not need:
        return jsonify({'error': 'Need not found'}), 404
    if need.status != 'active':
        return jsonify({'error': 'Need is not active'}), 400
    
    donation = Donation(
        amount=data['amount'],
        unit=data.get('unit'),
        description=data.get('description'),
        donation_type=data['donation_type'],
        need_id=data['need_id'],
        donor_id=current_user.id,
        delivery_address=data.get('delivery_address'),
        delivery_instructions=data.get('delivery_instructions')
    )
    
    db.session.add(donation)
    db.session.commit()
    
    return jsonify(donation.to_dict()), 201

@donation_bp.route('/donations/<int:donation_id>', methods=['GET'])
@login_required
def get_donation(donation_id):
    """Get a specific donation"""
    donation = Donation.query.get_or_404(donation_id)
    
    # Check if user can view this donation
    if current_user.id != donation.donor_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(donation.to_dict())

@donation_bp.route('/donations/<int:donation_id>', methods=['PUT'])
@login_required
def update_donation(donation_id):
    """Update a donation (only the donor or admin can update)"""
    donation = Donation.query.get_or_404(donation_id)
    
    if current_user.id != donation.donor_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Update fields
    if 'amount' in data:
        donation.amount = data['amount']
    if 'unit' in data:
        donation.unit = data['unit']
    if 'description' in data:
        donation.description = data['description']
    if 'status' in data:
        valid_status = ['pending', 'accepted', 'delivered', 'cancelled']
        if data['status'] in valid_status:
            donation.status = data['status']
    if 'delivery_address' in data:
        donation.delivery_address = data['delivery_address']
    if 'delivery_instructions' in data:
        donation.delivery_instructions = data['delivery_instructions']
    if 'delivery_date' in data:
        from datetime import datetime
        try:
            donation.delivery_date = datetime.fromisoformat(data['delivery_date'])
        except ValueError:
            return jsonify({'error': 'Invalid delivery date format'}), 400
    
    db.session.commit()
    return jsonify(donation.to_dict())

@donation_bp.route('/donations/<int:donation_id>', methods=['DELETE'])
@login_required
def delete_donation(donation_id):
    """Delete a donation (only the donor or admin can delete)"""
    donation = Donation.query.get_or_404(donation_id)
    
    if current_user.id != donation.donor_id and current_user.user_type != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(donation)
    db.session.commit()
    return '', 204

@donation_bp.route('/needs/<int:need_id>/donations', methods=['GET'])
def get_need_donations(need_id):
    """Get all donations for a specific need"""
    need = Need.query.get_or_404(need_id)
    donations = Donation.query.filter_by(need_id=need_id).order_by(Donation.created_at.desc()).all()
    return jsonify([donation.to_dict() for donation in donations])

@donation_bp.route('/my-donations', methods=['GET'])
@login_required
def get_my_donations():
    """Get current user's donations"""
    donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.created_at.desc()).all()
    return jsonify([donation.to_dict() for donation in donations]) 