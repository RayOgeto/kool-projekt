from flask import Blueprint, render_template, request, redirect, flash, url_for, current_app
from flask_login import login_required, current_user
from .models import Donation
from .models import Request as ResourceRequest
from .models import Match, DonationMedia, DonationReport, User
from . import db
import os
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'donor':
        donor_donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.id.desc()).all()
        total_donations = len(donor_donations)
        matched_donations = len([d for d in donor_donations if d.matched])
        unmatched_donations = total_donations - matched_donations
        lives_impacted = matched_donations
        success_rate = int((matched_donations / total_donations) * 100) if total_donations else 0
        recent_donations = donor_donations[:5]
        return render_template(
            'dashboard/donor_dashboard.html',
            total_donations=total_donations,
            matched_donations=matched_donations,
            unmatched_donations=unmatched_donations,
            lives_impacted=lives_impacted,
            success_rate=success_rate,
            recent_donations=recent_donations,
        )
    elif current_user.role == 'recipient':
        return render_template('dashboard/recipient_dashboard.html')
    elif current_user.role == 'admin':
        return render_template('admin/match_dashboard.html')


    else:
        return render_template('home.html')
    
@main.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if current_user.role != 'donor':
        flash("you are not a donor. cannnot donate")
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        location = request.form.get('location')
        image_file = request.files.get('donation_image')

        new_donation = Donation(
            donor_id=current_user.id,
            item=item,
            quantity=quantity,
            description=description,
            location=location
        )
        db.session.add(new_donation)
        db.session.commit()

        # Handle safe image upload
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            if not image_file.mimetype.startswith('image/'):
                flash('Only image uploads are allowed.')
                return redirect(url_for('main.donate'))
            image_file.seek(0, os.SEEK_END)
            size_bytes = image_file.tell()
            image_file.seek(0)
            if size_bytes > 5 * 1024 * 1024:
                flash('Image must be <= 5MB.')
                return redirect(url_for('main.donate'))

            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            save_path = os.path.join(upload_dir, filename)
            image_file.save(save_path)

            media = DonationMedia(donation_id=new_donation.id, file_path=f"/static/uploads/{filename}")
            db.session.add(media)
            db.session.commit()
        flash("Donation submitted! Thanks for danating on UjamaaFlow")
        return redirect(url_for('main.dashboard'))
    
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
    total_users = db.session.query(db.func.count('*')).select_from(db.Model.metadata.tables['user']).scalar() if 'user' in db.Model.metadata.tables else 0
    total_donations = Donation.query.count()
    total_requests = ResourceRequest.query.count()
    total_reports = DonationReport.query.count()

    return render_template(
        'admin/match_dashboard.html',
        donations=unmatched_donations,
        requests=unfulfilled_requests,
        total_users=total_users,
        total_donations=total_donations,
        total_requests=total_requests,
        total_reports=total_reports,
    )

@main.route('/admin/match', methods=['POST'])
@login_required
def create_match():
    if current_user.role != 'admin':
        flash("Admins only.")
        return redirect(url_for('main.dashboard'))

    donation_id = request.form.get('donation_id')
    request_id = request.form.get('request_id')
    donation = Donation.query.get(donation_id)
    req = ResourceRequest.query.get(request_id)
    if not donation or not req:
        flash('Invalid donation or request.')
        return redirect(url_for('main.admin_dashboard'))

    match = Match(donation_id=donation.id, request_id=req.id, status='matched')
    donation.matched = True
    req.fulfilled = True
    db.session.add(match)
    db.session.commit()
    flash('Match created successfully!')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/browse')
@login_required
def browse():
    if current_user.role != 'recipient':
        flash('Only recipients can browse available donations.')
        return redirect(url_for('main.dashboard'))

    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    location = request.args.get('location', '').strip()

    donations_query = Donation.query.filter_by(matched=False)
    if query:
        donations_query = donations_query.filter(
            (Donation.item.ilike(f"%{query}%")) | (Donation.description.ilike(f"%{query}%"))
        )
    if location:
        donations_query = donations_query.filter(Donation.location.ilike(f"%{location}%"))

    donations = donations_query.order_by(Donation.id.desc()).all()
    return render_template('recipient/browse.html', donations=donations, q=query, category=category, location=location)

@main.route('/admin/donations')
@login_required
def admin_donations():
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    items = Donation.query.order_by(Donation.id.desc()).all()
    return render_template('admin/donations.html', donations=items)

@main.route('/admin/requests')
@login_required
def admin_requests():
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    items = ResourceRequest.query.order_by(ResourceRequest.id.desc()).all()
    return render_template('admin/requests.html', requests=items)

@main.route('/admin/reports')
@login_required
def admin_reports():
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    reports = DonationReport.query.order_by(DonationReport.id.desc()).all()
    return render_template('admin/reports.html', reports=reports)

@main.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    users = User.query.order_by(User.id.desc()).all()
    return render_template('admin/users.html', users=users)

@main.route('/admin/donation/<int:donation_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_donation(donation_id):
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    d = Donation.query.get_or_404(donation_id)
    d.matched = not d.matched
    db.session.commit()
    flash('Donation status updated.')
    return redirect(request.referrer or url_for('main.admin_donations'))

@main.route('/admin/request/<int:request_id>/toggle', methods=['POST'])
@login_required
def admin_toggle_request(request_id):
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    r = ResourceRequest.query.get_or_404(request_id)
    r.fulfilled = not r.fulfilled
    db.session.commit()
    flash('Request status updated.')
    return redirect(request.referrer or url_for('main.admin_requests'))

@main.route('/admin/report/<int:report_id>/resolve', methods=['POST'])
@login_required
def admin_resolve_report(report_id):
    if current_user.role != 'admin':
        flash('Admins only.')
        return redirect(url_for('main.dashboard'))
    rep = DonationReport.query.get_or_404(report_id)
    db.session.delete(rep)
    db.session.commit()
    flash('Report resolved.')
    return redirect(request.referrer or url_for('main.admin_reports'))

@main.route('/donation/<int:donation_id>/report', methods=['POST'])
@login_required
def report_donation(donation_id):
    reason = request.form.get('reason', '').strip()
    donation = Donation.query.get_or_404(donation_id)
    report = DonationReport(donation_id=donation.id, reporter_id=current_user.id, reason=reason)
    donation.flagged = True
    db.session.add(report)
    db.session.commit()
    flash('Thank you for your report. Our team will review this listing.')
    return redirect(url_for('main.browse'))

@main.route('/contact')
def contact():
    return render_template('contact/contact.html')
# @main.route('/admin')
# def contact():
#     return render_template('admin/match_dashboard.html')
@main.route('/resource')
def resource():
    return render_template('resources/resource.html')
@main.route('/recipient')
def recipient_dashboard():
    return render_template('dashboard/recipient_dashboard.html')

@main.route('/donations')
@login_required
def my_donations():
    if current_user.role != 'donor':
        flash('Only donors can view their donations.')
        return redirect(url_for('main.dashboard'))
    donor_donations = Donation.query.filter_by(donor_id=current_user.id).order_by(Donation.id.desc()).all()
    return render_template('donor/my_donations.html', donations=donor_donations)