from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_classs='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_classs)

    db.init_app(app=app, )


