from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models import PlacementDrive, Application, StudentProfile
from routes._decorators import role_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
@role_required('student')
def dashboard():
    # Show active/approved drives
    approved_drives = PlacementDrive.query.filter_by(status='Approved').order_by(PlacementDrive.created_at.desc()).all()
    # Get all application ids for current student to hide apply buttons
    student_profile = current_user.student_profile
    applied_drive_ids = [app.drive_id for app in student_profile.applications]
    
    return render_template('student/dashboard.html', drives=approved_drives, applied_drive_ids=applied_drive_ids)

@student_bp.route('/apply/<int:drive_id>', methods=['POST'])
@login_required
@role_required('student')
def apply(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    student_profile = current_user.student_profile
    
    if drive.status != 'Approved':
        flash('This drive is not open for applications.', 'danger')
        return redirect(url_for('student.dashboard'))
        
    # Prevent duplicate applications
    existing_application = Application.query.filter_by(student_id=student_profile.id, drive_id=drive_id).first()
    if existing_application:
        flash('You have already applied for this drive.', 'warning')
        return redirect(url_for('student.dashboard'))
        
    application = Application(student_id=student_profile.id, drive_id=drive_id, status='Applied')
    db.session.add(application)
    db.session.commit()
    flash('Successfully applied to the placement drive.', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/history')
@login_required
@role_required('student')
def history():
    student_profile = current_user.student_profile
    applications = Application.query.filter_by(student_id=student_profile.id).order_by(Application.application_date.desc()).all()
    return render_template('student/history.html', applications=applications)

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('student')
def profile():
    student_profile = current_user.student_profile
    if request.method == 'POST':
        student_profile.phone = request.form.get('phone')
        
        # Resume handling (saving to disk, simplified here to just the URL or basic logic)
        resume_file = request.files.get('resume')
        if resume_file and resume_file.filename != '':
            import os
            from werkzeug.utils import secure_filename
            from flask import current_app
            filename = secure_filename(f"{current_user.id}_{resume_file.filename}")
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            resume_file.save(filepath)
            student_profile.resume_path = filename
            
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('student.profile'))
        
    return render_template('student/profile.html', student=student_profile)
