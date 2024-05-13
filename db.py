from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Create a SQLAlchemy base class
class Base(DeclarativeBase):
    pass

# Create a SQLAlchemy object
db = SQLAlchemy(model_class=Base)
#hello world