from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import PlacementDrive, Application
from routes._decorators import role_required
from datetime import datetime

company_bp = Blueprint('company', __name__)

@company_bp.route('/dashboard')
@login_required
@role_required('company')
def dashboard():
    drives = PlacementDrive.query.filter_by(company_id=current_user.id).all()
    # application count per drive can be handled in template by drive.applications|length
    return render_template('company/dashboard.html', drives=drives)

@company_bp.route('/drive/create', methods=['GET', 'POST'])
@login_required
@role_required('company')
def create_drive():
    if not current_user.is_approved:
        flash('You must be approved by the admin to create placement drives.', 'warning')
        return redirect(url_for('company.dashboard'))
        
    if request.method == 'POST':
        job_title = request.form.get('job_title')
        job_description = request.form.get('job_description')
        eligibility_criteria = request.form.get('eligibility_criteria')
        application_deadline_str = request.form.get('application_deadline')
        
        try:
            deadline = datetime.strptime(application_deadline_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            try:
                deadline = datetime.strptime(application_deadline_str, '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format.', 'danger')
                return redirect(url_for('company.create_drive'))
                
        drive = PlacementDrive(
            company_id=current_user.id,
            job_title=job_title,
            job_description=job_description,
            eligibility_criteria=eligibility_criteria,
            application_deadline=deadline,
            status='Pending' # Default to pending admin approval
        )
        db.session.add(drive)
        db.session.commit()
        flash('Placement drive created and is pending admin approval.', 'success')
        return redirect(url_for('company.dashboard'))
        
    return render_template('company/create_drive.html')

@company_bp.route('/drive/<int:drive_id>/edit', methods=['GET', 'POST'])
@login_required
@role_required('company')
def edit_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('company.dashboard'))
        
    if request.method == 'POST':
        drive.job_title = request.form.get('job_title')
        drive.job_description = request.form.get('job_description')
        drive.eligibility_criteria = request.form.get('eligibility_criteria')
        
        deadline_str = request.form.get('application_deadline')
        try:
            drive.application_deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            try:
                drive.application_deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
            except ValueError:
                pass
                
        db.session.commit()
        flash('Placement drive updated.', 'success')
        return redirect(url_for('company.dashboard'))
        
    return render_template('company/edit_drive.html', drive=drive)

@company_bp.route('/drive/<int:drive_id>/close', methods=['POST'])
@login_required
@role_required('company')
def close_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id == current_user.id:
        drive.status = 'Closed'
        db.session.commit()
        flash('Drive closed successfully.', 'success')
    return redirect(url_for('company.dashboard'))
    
@company_bp.route('/drive/<int:drive_id>/applications')
@login_required
@role_required('company')
def view_applications(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('company.dashboard'))
        
    applications = Application.query.filter_by(drive_id=drive_id).all()
    return render_template('company/applications.html', drive=drive, applications=applications)

@company_bp.route('/application/<int:app_id>/status', methods=['POST'])
@login_required
@role_required('company')
def update_application_status(app_id):
    application = Application.query.get_or_404(app_id)
    # verify ownership
    if application.drive.company_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('company.dashboard'))
        
    new_status = request.form.get('status')
    valid_statuses = ['Applied', 'Shortlisted', 'Selected', 'Rejected']
    if new_status in valid_statuses:
        application.status = new_status
        db.session.commit()
        flash(f'Application status updated to {new_status}.', 'success')
        
    return redirect(url_for('company.view_applications', drive_id=application.drive_id))
