from flask import Flask, url_for, render_template, request, Blueprint, redirect, session, jsonify, flash
from db import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User
from flask_mail import Mail, Message

def create_app(testing=False):
    # Initialize the Flask app
    app = Flask(__name__)
    app.secret_key = "supersecret"
    UPLOAD_FOLDER = 'items'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    if testing:
        # In-memory database for testing
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        # Main database URI
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
        app.instance_path = Path("./data").resolve()

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'tanishbansal07787@gmail.com'
    app.config['MAIL_PASSWORD'] = 'elgggkpszgvqypkj'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    def test_mail():
        with app.app_context():
            msg = Message('Hello', sender = app.config['MAIL_USERNAME'], recipients = ['tanish.bansal0007@gmail.com'])
            msg.body = "Hello Flask message sent from Flask-Mailhhhh"
            mail.send(msg)
            return "Sent"
    test_mail()

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

# defines only allowed extension as png
ALLOWED_EXTENSIONS = {'png'}

#limits file size to 16 MB
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# checks that a period is in filename (signifies extentsion), splits the filename into the part before the period and after, selects the second item which is the extension, makes it lower case, then checks to see if its in allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8888)
