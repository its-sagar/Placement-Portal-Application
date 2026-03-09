from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import User, CompanyProfile, StudentProfile, PlacementDrive, Application
from routes._decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/deshboard')
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()

    pending_companies = User.query.filter_by(role="company", is_approved=False).all()
    pending_drives = PlacementDrive.query.filter_by(status='Pending').all()

    return render_template('admin/dashboard.html',
                            total_students=total_students,
                            total_companies=total_companies,
                            total_drives=total_drives,
                            total_applications=total_applications,
                            pending_companies=pending_companies,
                            pending_drives=pending_drives)

@admin_bp.route('/companies', methods=['GET'])
@login_required
@role_required('admin')
def companies():
    search_query = request.args.get('search', '')
    if search_query:
        # Search by company name
        companies = User.query.join(CompanyProfile).filter(
            User.role == 'company',
            CompanyProfile.company_name.ilike(f'%{search_query}%')
        ).all()
    else:
        companies = User.query.filter_by(role='company').all()
    return render_template('admin/companies.html', companies=companies, search_query=search_query)

@admin_bp.route('/students', methods=['GET'])
@login_required
@role_required('admin')
def students():
    search_query = request.args.get('search', '')
    if search_query:
        # Search by name or enrollment number or email
        students = User.query.join(StudentProfile).filter(
            User.role == 'student',
            (StudentProfile.full_name.ilike(f'%{search_query}%')) |
            (StudentProfile.enrollment_no.ilike(f'%{search_query}%')) |
            (User.email.ilike(f'%{search_query}%'))
        ).all()
    else:
        students = User.query.filter_by(role='student').all()
    return render_template('admin/students.html', students=students, search_query=search_query)

@admin_bp.route('/approve_company/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def approve_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        user.is_approved = True
        db.session.commit()
        flash(f'Company {user.company_profile.company_name} approved successfully.', 'success')
    return redirect(request.referrer or url_for('admin.companies'))

@admin_bp.route('/reject_company/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def reject_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        # Rejecting might mean deleting or just leaving unapproved
        db.session.delete(user.company_profile)
        db.session.delete(user)
        db.session.commit()
        flash('Company registration rejected and deleted.', 'success')
    return redirect(request.referrer or url_for('admin.companies'))

@admin_bp.route('/toggle_status/<int:user_id>', methods=['POST'])
@login_required
@role_required('admin')
def toggle_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role in ['company', 'student']:
        user.is_active = not user.is_active
        db.session.commit()
        status = "Activated" if user.is_active else "Deactivated/Blacklisted"
        flash(f'User {user.username} {status}.', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))

@admin_bp.route('/drives', methods=['GET'])
@login_required
@role_required('admin')
def drives():
    drives = PlacementDrive.query.all()
    return render_template('admin/drives.html', drives=drives)

@admin_bp.route('/approve_drive/<int:drive_id>', methods=['POST'])
@login_required
@role_required('admin')
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Approved'
    db.session.commit()
    flash('Placement drive approved.', 'success')
    return redirect(request.referrer or url_for('admin.drives'))

@admin_bp.route('/reject_drive/<int:drive_id>', methods=['POST'])
@login_required
@role_required('admin')
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    flash('Placement drive rejected and deleted.', 'success')
    return redirect(request.referrer or url_for('admin.drives'))
