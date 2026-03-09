from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app import db
from models import User, CompanyProfile, StudentProfile, PlacementDrive, Application

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