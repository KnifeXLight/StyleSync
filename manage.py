from app import app
from db import db
from models import User, Item,Category, Outfit,Filter,Tag,OutfitItem
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys

# Create all tables
def create_tables():
    with app.app_context():
        db.create_all()

# Drop all tables
def drop_tables():
    with app.app_context():
        db.drop_all()


# Add mock data
def add_mock_data():
    with app.app_context():
        
        name1 = "Test User 1"
        email1 = "test1@example.com"
        password1 = "testpassword"

        name2 = "Test User 2"
        email2 = "test2@example.com"
        password2 = "testpassword"
        # Create Users
        user1 = User(name=name1, email=email1,password=generate_password_hash(password1, method="scrypt")) # type: ignore
        user2 = User(name=name2, email=email2, password=generate_password_hash(password2, method="scrypt")) # type: ignore
        
        db.session.add_all([user1, user2])
        db.session.commit()

# Query for users
        user1 = db.session.query(User).filter_by(id=1).first()
        user2 = db.session.query(User).filter_by(id=2).first()

        # Create Categories
        category1 = Category(name='Clothing') # type: ignore
        category2 = Category(name='Accessories') # type: ignore

        db.session.add_all([category1, category2])
        db.session.commit()

        # Create Filters
        filter1 = Filter(name='Color', category=category1) # type: ignore
        filter2 = Filter(name='Size', category=category1) # type: ignore

        db.session.add_all([filter1, filter2])
        db.session.commit()

        # Create Items
        item1 = Item(name='Red Shirt', image_url='/static/img/red_shirt.png', user=user1) # type: ignore
        item2 = Item(name='Blue Jeans', image_url='/static/img/blue_jeans.png', user=user1) # type: ignore
        item3 = Item(name='Green Hat', image_url='/static/img/green_hat.png', user=user2) # type: ignore

        db.session.add_all([item1, item2, item3])
        db.session.commit()

        # Create Tags
        tag1 = Tag(item=item1, category=category1, filter=filter1) # type: ignore
        tag2 = Tag(item=item2, category=category1, filter=filter2) # type: ignore
        tag3 = Tag(item=item3, category=category2, filter=filter1) # type: ignore
        # Assuming filter1 is appropriate here

        db.session.add_all([tag1, tag2, tag3])
        db.session.commit()

        # Create Outfits
        outfit1 = Outfit(user=user1, created=datetime.now(), rating=5) # type: ignore
        outfit2 = Outfit(user=user2, created=datetime.now(), rating=4) # type: ignore

        db.session.add_all([outfit1, outfit2])
        db.session.commit()

        # Create OutfitItems
        outfit_item1 = OutfitItem(outfit=outfit1, item=item1) # type: ignore
        outfit_item2 = OutfitItem(outfit=outfit1, item=item2) # type: ignore
        outfit_item3 = OutfitItem(outfit=outfit2, item=item3) # type: ignore

        db.session.add_all([outfit_item1, outfit_item2, outfit_item3])
        db.session.commit()

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) > 1 and argv[1] == 'drop':
        drop_tables()
        print("Tables dropped successfully")
        sys.exit()
    elif len(argv) > 1 and argv[1] == 'create':
        create_tables()
        print("Tables created successfully")
        sys.exit()
    elif len(argv) > 1 and argv[1] == 'seed':
        add_mock_data()
        print("Mock data added successfully")
        sys.exit()
    elif len(argv) > 1 and argv[1] == 'reset':
        drop_tables()
        create_tables()
        add_mock_data()
        print("Tables reset successfully")
        sys.exit()
    else:
        print("Invalid command. Please use 'create', 'drop', or 'seed' as arguments")
        sys.exit()
