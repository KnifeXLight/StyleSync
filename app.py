from flask import Flask
from db import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User


def create_app(testing=False):
    # Initialize the Flask app
    app = Flask(__name__)
    app.secret_key = "supersecret"
    if testing:
        # In-memory database for testing
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        # Main database URI
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
        app.instance_path = Path("./data").resolve()

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the database
    db.init_app(app)

    # Register the blueprints
    app.register_blueprint(auth_routes_bp, url_prefix="/")
    app.register_blueprint(html_routes_bp, url_prefix="/views")

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'authorization.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8888)
