from flask import url_for, render_template, request, Blueprint, redirect, session, flash
from db import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user


auth_routes_bp = Blueprint("authorization", __name__)


@auth_routes_bp.route("/")
def home():
    return render_template("/auth/login.html")


@auth_routes_bp.route("/auth/register")
def register():
    return render_template("/auth/signup.html")


@auth_routes_bp.route("/auth/register", methods=["POST"])
def signup():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    print(email)
    print(name)
    print(password)
    if not email or not name or not password:
        return redirect(url_for("authorization.register"))
    # if len(passwords) < 8:
    #     return redirect(url_for("authorization.register"))
    if email == "" or name == "" or password == "":
        return redirect(url_for("authorization.register"))
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(
        name=name,
        email=email,
        password=generate_password_hash(password, method="scrypt"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("authorization.home"))


# @auth_routes_bp.route("/login", methods=["POST"])
# def login():
#     email = request.form.get("email")
#     password = request.form.get("password")
#     print(email)
#     print(password)
#     statement = db.select(User).where(User.email == email)
#     user = db.session.execute(statement).scalar()
#     if not user:
#         print ("User not found")
#         return redirect(url_for("authorization.register"))
#     if not check_password_hash(user.password, password):
#         print("Password is incorrect")
#         return redirect(url_for("authorization.register"))
#     return redirect(url_for("html.homepage", id=user.id))
@auth_routes_bp.route("/auth/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    statement = db.select(User).where(User.email == email)
    user = db.session.execute(statement).scalar()
    if not user or not check_password_hash(user.password, password):
        flash('Email or Password is incorrect')
        return redirect(url_for("authorization.home"))
    login_user(user, remember=remember)
    return redirect(url_for("html.home"))
@auth_routes_bp.route("/auth/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("authorization.home"))