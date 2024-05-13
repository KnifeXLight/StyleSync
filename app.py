from flask import Flask
from db import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.instance_path = Path("./data").resolve()

# Initialize the database
db.init_app(app)
app.register_blueprint(auth_routes_bp, url_prefix="/")
app.register_blueprint(html_routes_bp, url_prefix="/views")
login_manager = LoginManager()
login_manager.login_view = 'authorization.home'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
