from sqlalchemy import (
    Boolean,
    Float,
    Numeric,
    ForeignKey,
    Integer,
    String,
    DECIMAL,
    DateTime,
    DATETIME,
)
from sqlalchemy.orm import mapped_column, relationship
from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
# from time import time

# from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
# * User Table (Users in the database for login)


class User(UserMixin, db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    email = db.Column(String(200), nullable=False, unique=True)
    password = db.Column(String(200), nullable=False)
    items = relationship("Item", back_populates="user")
    outfits = relationship("Outfit", back_populates="user")
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiration = db.Column(db.DateTime, nullable=True)

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(
                token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=1800)
        except:
            return None
        return User.query.filter_by(email=email).first()

    def set_password(self, password):
        self.password = generate_password_hash(password, method="scrypt")
# * Item Table (Items in the wardrobe)


class Item(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    image_url = db.Column(String(200), nullable=False)
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="items")
    item_tags = relationship("Tag", back_populates="item",
                             cascade="all, delete-orphan")
    outfit_items = relationship(
        "OutfitItem", back_populates="item", cascade="all, delete-orphan")

# * Category Table (Categories for the items, e.g. Tops, Bottoms, Shoes, etc.)


class Category(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    tags = relationship("Tag", back_populates="category")
    filters = relationship("Filter", back_populates="category")

# * Filter Table (Filters for the items)


class Filter(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    category_id = db.Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship("Category", back_populates="filters")
    tags = relationship("Tag", back_populates="filter")

# * Tag Table (Tags for the items)


class Tag(db.Model):
    id = db.Column(Integer, primary_key=True)
    item_id = db.Column(Integer, ForeignKey('item.id'), nullable=False)
    category_id = db.Column(Integer, ForeignKey('category.id'), nullable=False)
    filter_id = db.Column(Integer, ForeignKey('filter.id'), nullable=False)
    item = relationship("Item", back_populates="item_tags")
    category = relationship("Category", back_populates="tags")
    filter = relationship("Filter", back_populates="tags")

# * Outfit Table (Outfits created by the user)


class Outfit(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=False)
    name = db.Column(String(200), nullable=False, default="Untitled Outfit")
    created = db.Column(DateTime, nullable=True, default=None)
    rating = db.Column(Integer, nullable=True)
    user = relationship("User", back_populates="outfits")
    outfit_items = relationship("OutfitItem", back_populates="outfit")

# * OutfitItem Table (Junction Table between Outfit and Item)


class OutfitItem(db.Model):
    id = db.Column(Integer, primary_key=True)
    outfit_id = db.Column(Integer, ForeignKey('outfit.id'), nullable=False)
    item_id = db.Column(Integer, ForeignKey('item.id'), nullable=False)
    outfit = relationship("Outfit", back_populates="outfit_items")
    item = relationship("Item", back_populates="outfit_items")


# class Image(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=True)
#     image_url = mapped_column(String(500), nullable=True)
#     wardrobe = relationship('Wardrobe')

# class Type(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=False)
#     wardrobe = relationship('Wardrobe')

# class Weather(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=False)
#     wardrobe_weather = relationship('Wardrobe_Weather')

# class Colour(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=False)
#     wardrobe_colour = relationship('Wardrobe_Colour')

# class Feeling(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=False)
#     wardrobe_feeling = relationship('Wardrobe_Feeling')

# class Style(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=False)
#     wardrobe_style = relationship('Wardrobe_Style')

# class Wardrobe(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(500), nullable=False)
#     created = mapped_column(DateTime, nullable=False, default=None)

#     image_id = mapped_column(Integer, ForeignKey(Image.id), nullable=True)
#     user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False)
#     type_id = mapped_column(Integer, ForeignKey(Type.id), nullable=True)

#     user = relationship("User", back_populates='wardrobe')
#     image = relationship("Image", back_populates='wardrobe')
#     type = relationship("Type", back_populates='wardrobe')
#     wardrobe_weather = relationship('Wardrobe_Weather')
#     wardrobe_colour = relationship('Wardrobe_Colour')
#     wardrobe_feeling = relationship('Wardrobe_Feeling')
#     wardrobe_style = relationship('Wardrobe_Style')


# # # * Relations:
# # # 1. User has many Wardrobe Items, Wardrobe Items belong to a User
# # # 2. Wardrobe has one type, and one type has one wardrobe item
# # # 3. Wardrobe has many weather, style, colour, feeling
# # # 4. Weather, style, colour, feeling has many wardrobe items

# # Junction Tables:
# # 1. Wardrobe_Weather

# class Wardrobe_Weather(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     wardrobe_id = mapped_column(Integer, ForeignKey(Wardrobe.id), nullable=False)
#     weather_id = mapped_column(Integer, ForeignKey(Weather.id), nullable=False)
#     wardrobe = relationship('Wardrobe', back_populates='wardrobe_weather')
#     weather = relationship('Weather', back_populates='wardrobe_weather')


# # # 2. Wardrobe_Style

# class Wardrobe_Style(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     wardrobe_id = mapped_column(Integer, ForeignKey(Wardrobe.id), nullable=False)
#     style_id = mapped_column(Integer, ForeignKey(Style.id), nullable=False)
#     wardrobe = relationship('Wardrobe', back_populates='wardrobe_style')
#     style = relationship('Style', back_populates='wardrobe_style')


# # 3. Wardrobe_Colour

# class Wardrobe_Colour(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     wardrobe_id = mapped_column(Integer, ForeignKey(Wardrobe.id), nullable=False)
#     colour_id = mapped_column(Integer, ForeignKey(Colour.id), nullable=False)
#     wardrobe = relationship('Wardrobe', back_populates='wardrobe_colour')
#     colour = relationship('Colour', back_populates='wardrobe_colour')


# 4. Wardrobe_Feeling

# class Wardrobe_Feeling(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     wardrobe_id = mapped_column(Integer, ForeignKey(Wardrobe.id), nullable=False)
#     feeling_id = mapped_column(Integer, ForeignKey(Feeling.id), nullable=False)
#     wardrobe = relationship('Wardrobe', back_populates='wardrobe_feeling')
#     feeling = relationship('Feeling', back_populates='wardrobe_feeling')

# # ! Outfit Tables needed for the Outfit database

# # Outfit Table
# class Outfit(db.Model):
#     id = mapped_column(Integer, primary_key=True)
#     user_id = mapped_column(Integer, ForeignKey('User.id'), nullable=False)
#     created = mapped_column(DateTime, nullable=True, default=None)
#     rating = mapped_column(Integer, nullable=True)

# After creating the below categories for db, we need to add the foreign keys into Outfit Table
