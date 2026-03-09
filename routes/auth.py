from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from models import User, CompanyProfile, StudentProfile

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'company':
            return redirect(url_for('company.dashboard'))
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # Check if active
            if not user.is_active:
                flash('Your account has been deactivated. Contact admin.', 'danger')
                return redirect(url_for('auth.login'))
                
            # Check if company approved to login
            if user.role == 'company' and not user.is_approved:
                flash('Your registration is pending admin approval.', 'warning')
                return redirect(url_for('auth.login'))
                
            login_user(user, remember=request.form.get('remember'))
            
            # Redirect to role-based dashboard
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'company':
                return redirect(url_for('company.dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login.html')


@auth_bp.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name')
        hr_contact = request.form.get('hr_contact')
        website = request.form.get('website')
        
        # Validation checks could go here, omitting for brevity and to just flash
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Email or Username already exists.', 'danger')
            return redirect(url_for('auth.register_company'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password, role='company', is_approved=False)
        db.session.add(user)
        db.session.commit()
        
        profile = CompanyProfile(user_id=user.id, company_name=company_name, hr_contact=hr_contact, website=website)
        db.session.add(profile)
        db.session.commit()
        
        flash('Registration successful! Please wait for admin approval before logging in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_company.html')

@auth_bp.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        enrollment_no = request.form.get('enrollment_no')
        phone = request.form.get('phone')
        
        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            flash('Email or Username already exists.', 'danger')
            return redirect(url_for('auth.register_student'))
            
        if StudentProfile.query.filter_by(enrollment_no=enrollment_no).first():
            flash('Enrollment Number already exists.', 'danger')
            return redirect(url_for('auth.register_student'))
            
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Students don't need admin approval by default
        user = User(username=username, email=email, password=hashed_password, role='student', is_approved=True)
        db.session.add(user)
        db.session.commit()
        
        profile = StudentProfile(user_id=user.id, full_name=full_name, enrollment_no=enrollment_no, phone=phone)
        db.session.add(profile)
        db.session.commit()
        
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register_student.html')


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
