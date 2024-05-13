from sqlalchemy import Boolean, Float, Numeric, ForeignKey, Integer, String, DECIMAL, DateTime, DATETIME
from sqlalchemy.orm import mapped_column, relationship
from db import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False)
    email = mapped_column(String(200), nullable=False, unique=True)
    password = mapped_column(String(200), nullable=False)
    items = relationship('Items', back_populates='user')

class Items(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False)
    image_url = mapped_column(String(200), nullable=False)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    user = relationship('User', back_populates='items')
    item_tags = relationship('Tags')
    outfit_items = relationship('OutfitItems')



class Categories(db.Model):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(200), nullable=False)
    tags = relationship('Tags')

class Tags(db.Model):
    id = mapped_column(Integer, primary_key=True)
    item_id = mapped_column(Integer, ForeignKey(Items.id), nullable=False)
    category_id = mapped_column(Integer, ForeignKey(Categories.id), nullable=False)
    item = relationship('Items', back_populates='item_tags')
    category = relationship('Categories')
class Outfit(db.Model):
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey(User.id), nullable=False)
    created = mapped_column(DateTime, nullable=True, default=None)
    rating = mapped_column(Integer, nullable=True)
    user = relationship('User')
    outfit_items = relationship('OutfitItems')
class OutfitItems(db.Model):
    id = mapped_column(Integer, primary_key=True)
    outfit_id = mapped_column(Integer, ForeignKey(Outfit.id), nullable=False)
    item_id = mapped_column(Integer, ForeignKey(Items.id), nullable=False)
    outfit = relationship('Outfit', back_populates='outfit_items')
    item = relationship('Items', back_populates='outfit_items')

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

