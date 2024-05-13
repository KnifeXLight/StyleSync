from flask import Flask, url_for, render_template, request, Blueprint, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,current_user

html_routes_bp = Blueprint("html", __name__)

@html_routes_bp.route("/home")
@login_required
def home():
    print(current_user)
    return render_template("/html/wardrobe.html", user=current_user)

@html_routes_bp.route("/homepage")
@login_required
def homepage():
    return render_template("/html/home.html", user  = current_user)

@html_routes_bp.route("/newoutfit")
@login_required
def newoutfit():
    return render_template("/html/newoutfit.html")

@html_routes_bp.route("/wardrobe")
@login_required
def wardrobe():

    return render_template("/html/wardrobe.html", user = current_user)