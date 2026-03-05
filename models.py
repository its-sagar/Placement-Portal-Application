from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_approved = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"
    

class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    hr_contact = db.Column(db.String(20), nullable=False)
    website = db.Column(db.String(100), nullable=True)

    user = db.relationship('User', backref=db.backref('company_profile'), uselist=False)

    def __repr__(self):
        return f"companyProfile('{self.company_name}')"
    
class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    enrollment_no = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    resume_path = db.Column(db.String(200), nullable=True)

    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def __repr__(self):
        return f"StudentProfile('{self.full_name}', '{self.enrollment_no}')"
    

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.Foreignkey('user.id'), nunallable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    eligibility_criteria = db.Column(db.Text, nullable=False)
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    company = db.relationship('User', backref=db.backref('drives', lazy=True))
    applications = db.relationship('Application', backref='drive', lazy=True)

    def __repr__(self):
        return f"PlacementDrive('{self.job_title}', '{self.status}')"
    

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id', nullable=False))
    application_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Applied')

    def __repr__(self):
        return f"Application('{self.student_id}', '{self.status}')"


    
    