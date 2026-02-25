from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



def create_app(config_classs='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_classs)

    db.init_app(app)

    @app.route("/")
    def hello():
        return "Hello, Flask!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)



