from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_required, current_user
from .models import Donation
from .models import Request as ResourceRequest
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'donor':
        return render_template('dashboard/donor_dashboard.html')
    elif current_user.role == 'recipient':
        return render_template('dashboard/recipient_dashboard.html')
    else:
        return render_template('home.html')
    
@main.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if current_user.role != 'donor':
        flash("you are not a donor. cannnot donate")
        return redirect(url_for(main.dashboard))
    
    if request.method == 'POST':
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        location = request.form.get('location')

        new_donation = Donation(
            donor_id=current_user.id,
            item=item,
            quantity=quantity,
            description=description,
            location=location
        )
        db.session.add(new_donation)
        db.session.commit()
        flash("Donation submitted! Thanks for danating on downa")
        return redirect(url_for(main.dashboard))
    
    return render_template('donor/donate.html')
    
@main.route('/request-resource', methods=['GET', 'POST'])
@login_required
def request_resource():
    if current_user.role != 'recipient':
        flash("Access denied.")
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        item_needed = request.form.get('item_needed')
        quantity = request.form.get('quantity')
        reason = request.form.get('reason')
        location = request.form.get('location')

        new_request = ResourceRequest(
            recipient_id=current_user.id,
            item_needed=item_needed,
            quantity=quantity,
            reason=reason,
            location=location
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Request submitted!")
        return redirect(url_for('main.dashboard'))
    
    return render_template('recipient/request_form.html')

@main.route('/admin/matches')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    unmatched_donations = Donation.query.filter_by(matched=False).all()
    unfulfilled_requests = ResourceRequest.query.filter_by(fulfilled=False).all()

    return render_template('admin/match_dashboard.html', donations=unmatched_donations, requests=unfulfilled_requests)
