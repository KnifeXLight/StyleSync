from flask import Flask, url_for, render_template, request, Blueprint, redirect, session, jsonify, flash
from db import db
from pathlib import Path
from routes import auth_routes_bp, html_routes_bp
from flask_login import LoginManager
from models import User
from flask_mail import Mail, Message
import os
from werkzeug.security import generate_password_hash, check_password_hash
# Initialize the Flask app
app = Flask(__name__)
app.secret_key = "supersecret"
app.config['SECURITY_PASSWORD_SALT'] = 'your_password_salt'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.instance_path = Path("./data").resolve()
UPLOAD_FOLDER = 'items'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "tanish.bansal87077@gmail.com"
app.config['MAIL_PASSWORD'] = "tanishbansal"
mail = Mail(app)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_reset_token()
            send_reset_email(user, token)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            flash('No account found with that email.', 'warning')
        return redirect(url_for('login'))
    return render_template('reset_request.html')

def send_reset_email(user, token):
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    if request.method == 'POST':
        password = request.form['password']
        user.set_password(password)  # Assuming you have a method to hash and set the password
        user.reset_token = None
        user.reset_token_expiration = None
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html')
# defines only allowed extension as png
ALLOWED_EXTENSIONS = {'png'}

#limits file size to 16 MB
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# checks that a period is in filename (signifies extentsion), splits the filename into the part before the period and after, selects the second item which is the extension, makes it lower case, then checks to see if its in allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
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
