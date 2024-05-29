from flask import Flask, url_for, render_template, request, Blueprint, redirect, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from db import db
from models import User, Outfit, Item, OutfitItem, Category, Filter, Tag
from rembg import remove
from PIL import Image
import os
from sqlalchemy import func
# import webbrowser
# from io import BytesIO
from werkzeug.utils import secure_filename
html_routes_bp = Blueprint("html", __name__)


@html_routes_bp.route("/home")
@login_required
def home():
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    items = db.session.query(Item).filter(
        Item.user_id == current_user.id).all()
    outfit = db.session.query(Outfit).filter(
        Outfit.user_id == current_user.id).order_by(func.random()).first()
    alloutfits = db.session.query(Outfit).filter(
        Outfit.user_id == current_user.id).all()
    if not outfit:
        return redirect(url_for("html.home"))
    outfit_items = db.session.query(OutfitItem).filter(
        OutfitItem.outfit_id == outfit.id).all()
    item_dict = {}
    # print(outfit_items)
    for item in outfit_items:
        # print(item.item.item_tags)
        for tag in item.item.item_tags:
            if tag.category.name not in item_dict:
                item_dict[tag.category.name] = []
                item_dict[tag.category.name].append(tag.item)
            else:
                item_dict[tag.category.name].append(tag.item)
        # print(item_dict)
    all_items = {}
    for item in items:
        for tag in item.item_tags:
            if tag.category.name not in all_items:
                all_items[tag.category.name] = []
                all_items[tag.category.name].append(tag.item)
            else:
                all_items[tag.category.name].append(tag.item)
    # print(all_items)
    # print(items)
    item48 = db.session.query(Item).filter(Item.id == 45).first()
    print(item48.item_tags)
    for tag in item48.item_tags:
        print(tag.category.name)
    print(all_items)
    return render_template("/html/homepage.html", user=current_user, categories=categories, filters=filters, items=all_items, outfit=outfit, item_dict=item_dict, item_list=items, alloutfits=alloutfits)


@html_routes_bp.route("/newoutfit")
@login_required
def newoutfit():
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    items = db.session.query(Item).filter(
        Item.user_id == current_user.id).all()
    outfit = db.session.query(Outfit).filter(
        Outfit.user_id == current_user.id).first()
    outfit_items = db.session.query(OutfitItem).filter(
        OutfitItem.outfit_id == outfit.id).all()

    all_items = {}
    for item in items:
        for tag in item.item_tags:
            if tag.category.name not in all_items:
                all_items[tag.category.name] = []
                all_items[tag.category.name].append(tag.item)
            else:
                all_items[tag.category.name].append(tag.item)
    print(all_items)
    return render_template("/html/newoutfit.html", user=current_user, categories=categories, filters=filters, items=all_items, outfit=outfit)


@html_routes_bp.route("/outfit/<int:id>", methods=["GET"])
@login_required
def outfit(id):
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    items = db.session.query(Item).filter(
        Item.user_id == current_user.id).all()
    outfit = db.session.query(Outfit).filter(
        Outfit.id == id, Outfit.user_id == current_user.id).first()
    if not outfit:
        return redirect(url_for("html.home"))
    outfit_items = db.session.query(OutfitItem).filter(
        OutfitItem.outfit_id == outfit.id).all()
    item_dict = {}
    # print(outfit_items)
    for item in outfit_items:
        # print(item.item.item_tags)
        for tag in item.item.item_tags:
            if tag.category.name not in item_dict:
                item_dict[tag.category.name] = []
                item_dict[tag.category.name].append(tag.item)
            else:
                item_dict[tag.category.name].append(tag.item)
        # print(item_dict)
    all_items = {}
    for item in items:
        for tag in item.item_tags:
            if tag.category.name not in all_items:
                all_items[tag.category.name] = []
                all_items[tag.category.name].append(tag.item)
            else:
                all_items[tag.category.name].append(tag.item)
    # print(all_items)
    # print(items)
    item48 = db.session.query(Item).filter(Item.id == 45).first()
    print(item48.item_tags)
    for tag in item48.item_tags:
        print(tag.category.name)
    print(all_items)
    return render_template("/html/outfit.html", user=current_user, categories=categories, filters=filters, items=all_items, outfit=outfit, item_dict=item_dict, item_list=items)


@html_routes_bp.route("/wardrobe")
@login_required
def wardrobe():
    statement = db.session.query(Item).filter(
        Item.user_id == current_user.id).all()
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()

    return render_template("/html/wardrobe.html", user=current_user, categories=categories, filters=filters, items=statement)


@html_routes_bp.route("/item/<int:id>")
@login_required
def item(id):
    item = db.session.query(Item).filter(Item.id == id).first()
    return render_template("/html/item.html", item=item)


@html_routes_bp.route("/item/<int:id>", methods=["POST"])
@login_required
def oitem(id):
    request_data = request.form.to_dict()
    print(request_data)
    item = db.session.query(Item).filter(Item.id == id).first()
    return render_template("/html/item.html", item=item)


@html_routes_bp.route("/items/<int:id>")
@login_required
def delete_item(id):
    item = db.session.query(Item).filter(Item.id == id).first()
    if not item:
        return redirect(url_for("html.wardrobe")), 404
    db.session.delete(item)
    db.session.commit()
    flash("Item deleted", category="success")
    return redirect(url_for("html.wardrobe"))


@html_routes_bp.route("/wardrobe/filter")
@login_required
def filter():
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    items = db.session.query(Item).filter(
        Item.user_id == current_user.id).all()
    print(items)
    return render_template("/html/wardrobe.html", user=current_user, categories=categories, filters=filters, items=items)


# @html_routes_bp.route("/wardrobe/filter", methods=["POST"])
# @login_required
# def filter_post():
#     request_data = request.form.to_dict()
#     print(request_data)
#     print(current_user.id)
#     categories = db.session.query(Category).all()
#     filters = db.session.query(Filter).all()
#     item = []
#     for key, value in request_data.items():
#         statement = db.session.query(Tag).filter(
#             Tag.filter_id == value, Item.user_id == current_user.id).all()
#         print(statement)
#         for tag in statement:
#             if tag.item.user_id == current_user.id and tag.item not in item:
#                 item.append(tag.item)
#     print(item)

#     return render_template("/html/wardrobe.html", user=current_user, categories=categories, filters=filters, items=item)

@html_routes_bp.route("/wardrobe/filter", methods=["POST"])
@login_required
def filter_post():
    request_data = request.form.to_dict()
    print(request_data)
    print(current_user.id)
    categories = db.session.query(Category).all()
    filters = db.session.query(Filter).all()
    items = []

    for key, value in request_data.items():
        statement = db.session.query(Item).join(Tag).filter(
            Tag.filter_id == value, Tag.item_id == Item.id, Item.user_id == current_user.id).all()
        print(statement)
        for item in statement:
            if item not in items:
                items.append(item)
    print(items)

    return render_template("/html/wardrobe.html", user=current_user, categories=categories, filters=filters, items=items)


@html_routes_bp.route("/new_item")
@login_required
def new_item():
    return render_template("/html/new.html")


ALLOWED_EXTENSIONS = {'png'}
# limits file size to 16 MB
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

    # message if file is too large
    if file.content_length > MAX_CONTENT_LENGTH:
        return jsonify({'error': 'File size exceeds limit'})

    filename = secure_filename(file.filename)
    # filename_final = secure_filename(file.filename)
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
            output_filename = os.path.join(
                "static/items", 'processed_' + file.filename)
            output_image.save(output_filename)
            db.session.add(Item(user_id=current_user.id,
                           image_url=f"items/processed_{file.filename}", name=filename_without_extension))
            db.session.commit()
            # Remove the uploaded image

            os.remove(filename)
            flash("Item added", category="success")
            return jsonify({'filename': 'processed_' + file.filename})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'error': 'Unknown error'})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    # return redirect(url_for("html.wardrobe"))


@html_routes_bp.route("/profile", methods=["GET"])
@login_required
def profile():
    return render_template("/html/profile.html", user=current_user)


@html_routes_bp.route("/profile", methods=["POST"])
@login_required
def change_name_profile():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        print(name)
        print(email)
        user = db.session.get(User, current_user.id)
        if user:
            # Update the user's name and/or email if provided
            if name:
                current_user.name = name
            if email:
                current_user.email = email
            if password:  # If new password is provided
                # Hash the new password before storing it
                hashed_password = generate_password_hash(password)
                current_user.password = hashed_password
            db.session.commit()

            flash(
                f"User information updated - Name: {user.name}, Email: {user.email}", category="success")
            return redirect(url_for("html.profile"))

    return "", 204


@html_routes_bp.route("/oufit/<int:id>", methods=["POST"])
@login_required
def replace_item(id):
    request_data = request.form.to_dict()
    print(request_data)
    outfit = db.session.query(Outfit).filter(Outfit.id == id).first()
    outfit_items = db.session.query(OutfitItem).filter(
        OutfitItem.outfit_id == id).all()
    item = db.session.query(Item).filter(
        Item.id == request_data["item_to_be_replaced_id"]).first()
    item_to_replace = db.session.query(Item).filter(
        Item.id == request_data["item_to_replace_id"]).first()
    for outfit_item in outfit_items:
        if outfit_item.item_id == item.id:
            db.session.delete(outfit_item)
            db.session.commit()
    db.session.add(OutfitItem(outfit=outfit, item=item_to_replace))
    db.session.commit()
    return redirect(url_for("html.outfit", id=outfit.id))


@html_routes_bp.route("/add_outfit/<int:id>", methods=["POST"])
@login_required
def add_item(id):
    request_data = request.form.to_dict()
    print(request_data)
    outfit = db.session.query(Outfit).filter(Outfit.id == id).first()
    item = db.session.query(Item).filter(
        Item.id == request_data["item_id"]).first()
    db.session.add(OutfitItem(outfit=outfit, item=item))
    db.session.commit()
    return redirect(url_for("html.outfit", id=outfit.id))


@html_routes_bp.route("/newoutfit", methods=["POST"])
@login_required
def create_new_outfit():
    request_data = request.form.to_dict()
    print(request_data)
    outfit = Outfit(user_id=current_user.id)
    db.session.add(outfit)
    db.session.commit()
    item = db.session.query(Item).filter(
        Item.id == request_data["item_id"]).first()
    db.session.add(OutfitItem(outfit=outfit, item=item))
    db.session.commit()

    return redirect(url_for("html.outfit", id=outfit.id))


@html_routes_bp.route("/about")
@login_required
def about():
    return render_template("/html/about.html", user=current_user)

@html_routes_bp.route("/change_outfit_name/<int:id>", methods=["POST"])
@login_required
def change_outfit_name(id):
    request_data = request.form.to_dict()
    print(request_data)
    outfit = db.session.query(Outfit).filter(Outfit.id == id).first()
    print(outfit)
    print(outfit.name)
    outfit.name = request_data["name"]
    db.session.commit()
    return redirect(url_for("html.outfit", id=outfit.id))