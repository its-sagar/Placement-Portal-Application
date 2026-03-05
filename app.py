from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
  


db = SQLAlchemy()
migrate = Migrate()



def create_app(config_classs='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_classs)

    db.init_app(app)
    migrate.init_app(app=app, db=db)


    @app.route("/")
    def hello():
        return "Hello, Flask!"

    return app





