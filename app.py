from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

import click
from flask.cli import with_appcontext


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
bcrypt = Bcrypt()



def create_app(config_classs='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_classs)

    db.init_app(app)
    migrate.init_app(app=app, db=db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.company import company_bp
    from routes.student import student_bp

    from models import User

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(company_bp, url_prefix='/company')
    app.register_blueprint(student_bp, url_prefix='/student')

    @app.cli.command("createsuperuser")
    @with_appcontext
    def createsuperuser():
        """Create a user with admin privilages"""
        username=click.prompt("Username: ")
        email=click.prompt("Email: ")
        password=click.prompt("Password: ", hide_input=True, confirmation_prompt=True)

        if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
            click.echo(f"Error: User or eamil already exists.")
            return
        
        hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')

        user=User(
            username=username,
            email=email,
            password=hashed_password,
            role='admin',
            is_approved=True
        )

        db.session.add(user)
        db.session.commit()

        click.echo(f"Superuser '{username}' created successfully.")

    @app.route("/health")
    def health_check():
        return "OK", 200

    return app





