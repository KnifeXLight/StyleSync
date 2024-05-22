from flask import Flask, url_for, render_template, request, Blueprint, redirect, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required,current_user
from db import db
from models import User, Outfit, Item,OutfitItem,Category,Filter,Tag
from rembg import remove
from PIL import Image
import os
import webbrowser
from io import BytesIO
from werkzeug.utils import secure_filename
html_routes_bp = Blueprint("html", __name__)

@html_routes_bp.route("/home")
@login_required
def home():
    print(current_user)
    print(request.endpoint)
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
    statement = db.session.query(Item).filter(Item.user_id == current_user.id).all()
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    return render_template("/html/wardrobe.html", user = current_user, categories = categories, filters = filters, items = statement)
@html_routes_bp.route("/item/<int:id>")
@login_required
def item(id):
    item = db.session.query(Item).filter(Item.id == id).first()
    return render_template("/html/item.html", item = item)
@html_routes_bp.route("/items/<int:id>")
@login_required
def delete_item(id):
    item = db.session.query(Item).filter(Item.id == id).first()
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted",category= "success")
    return redirect(url_for("html.wardrobe"))
@html_routes_bp.route("/wardrobe/filter")
@login_required
def filter():
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    items = db.session.query(Item).filter(Item.user_id == current_user.id).all()
    print(items)
    return render_template("/html/wardrobe.html", user = current_user, categories = categories, filters = filters, items = items)
@html_routes_bp.route("/wardrobe/filter" , methods=["POST"])
@login_required
def filter_post():
    request_data = request.form.to_dict()
    print(request_data)
    print(current_user.id)
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    item = []
    for key,value in request_data.items():
        statement = db.session.query(Tag).filter(Tag.filter_id == value, Item.user_id == current_user.id).all()
        print(statement)
        for tag in statement:
            if tag.item.user_id == current_user.id and tag.item not in item:
                item.append(tag.item)
    print(item)

    return render_template("/html/wardrobe.html", user = current_user, categories = categories, filters = filters, items = item)
@html_routes_bp.route("/new_item")
@login_required
def new_item():
    return render_template("/html/new.html")
ALLOWED_EXTENSIONS = {'png'}
#limits file size to 16 MB
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
@html_routes_bp.route("/new_item", methods=["POST"])
@login_required

def upload_image():
    # Check if the post request has the file part
    # defines only allowed extension as png

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'})
    
    #message if file is too large
    if file.content_length > MAX_CONTENT_LENGTH:
        return jsonify({'error': 'File size exceeds limit'})
    
    filename = secure_filename(file.filename)
    filename_final = secure_filename(file.filename)
    filename_without_extension = filename.rsplit('.', 1)[0]
    print(filename)
    if file:
        # Save the uploaded image to the upload folder
        filename = os.path.join("static/items", file.filename)
        file.save(filename)
        
        try:
            # Open the input image
            input_image = Image.open(filename)
            
            # Remove the background
            output_image = remove(input_image)
            
            # Save the processed image
            output_filename = os.path.join("static/items", 'processed_' + file.filename)
            output_image.save(output_filename)
            db.session.add(Item(user_id = current_user.id, image_url = f"items/processed_{filename_final}", name = filename_without_extension))
            db.session.commit()
            # Remove the uploaded image

            os.remove(filename)
            flash("Item added",category= "success")
            return jsonify({'filename': 'processed_' + file.filename})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Unknown error'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS