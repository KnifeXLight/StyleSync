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
    outfits = relationship("Outfit", back_populates="user", cascade="all, delete-orphan")
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
    user_id = db.Column(Integer, ForeignKey('user.id'), nullable=True)
    user = relationship("User", back_populates="items")
    item_tags = relationship("Tag", back_populates="item", cascade="all, delete-orphan")
    outfit_items = relationship(
        "OutfitItem", back_populates="item", cascade="all, delete-orphan"
    )

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
    outfit_items = relationship(
        "OutfitItem", back_populates="outfit", cascade="all, delete-orphan"
    )

# * OutfitItem Table (Junction Table between Outfit and Item)
class OutfitItem(db.Model):
    id = db.Column(Integer, primary_key=True)
    outfit_id = db.Column(Integer, ForeignKey('outfit.id'), nullable=False)
    item_id = db.Column(Integer, ForeignKey('item.id'), nullable=False)
    outfit = relationship("Outfit", back_populates="outfit_items")
    item = relationship("Item", back_populates="outfit_items")

# The other models (Image, Type, Weather, Colour, Feeling, Style, Wardrobe) and their respective relationships
# can be defined here similarly if needed, ensuring that cascade="all, delete-orphan" is used where necessary.
