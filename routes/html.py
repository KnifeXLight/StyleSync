from flask import Flask, url_for, render_template, request, Blueprint, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,current_user
from db import db
from models import User, Outfit, Item,OutfitItem,Category,Filter,Tag
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
    # statement = db.session.query(Outfit).filter(Outfit.user_id == current_user.id).all()
    return render_template("/html/wardrobe.html", user = current_user)
@html_routes_bp.route("/item/<int:id>")
@login_required
def item(id):
    item = db.session.query(Item).filter(Item.id == id).first()
    return render_template("/html/item.html", item = item)
@html_routes_bp.route("/items/<int:id>")
@login_required
def delete_item(id):
    item = db.session.query(Item).filter(Item.id == id).first()
    if not item:
        return redirect(url_for("html.wardrobe")), 404
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("html.wardrobe"))