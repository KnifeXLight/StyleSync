from app import app
from db import db
from models import User, Item,Category, Outfit,Filter,Tag,OutfitItem
from datetime import datetime
def create_tables():
    with app.app_context():
        db.create_all()

def drop_tables():
    with app.app_context():
        db.drop_all()


# Create all tables
# Add mock data
def add_mock_data():
    with app.app_context():
        
        # Create Users

# Query for users
        user1 = db.session.query(User).filter_by(id=1).first()
        user2 = db.session.query(User).filter_by(id=2).first()

        # Create Categories
        category1 = Category(name='Clothing')
        category2 = Category(name='Accessories')

        db.session.add_all([category1, category2])
        db.session.commit()

        # Create Filters
        filter1 = Filter(name='Color', category=category1)
        filter2 = Filter(name='Size', category=category1)

        db.session.add_all([filter1, filter2])
        db.session.commit()

        # Create Items
        item1 = Item(name='Red Shirt', image_url='/static/img/red_shirt.png', user=user1)
        item2 = Item(name='Blue Jeans', image_url='/static/img/blue_jeans.png', user=user1)
        item3 = Item(name='Green Hat', image_url='/static/img/green_hat.png', user=user2)

        db.session.add_all([item1, item2, item3])
        db.session.commit()

        # Create Tags
        tag1 = Tag(item=item1, category=category1, filter=filter1)
        tag2 = Tag(item=item2, category=category1, filter=filter2)
        tag3 = Tag(item=item3, category=category2, filter=filter1)  # Assuming filter1 is appropriate here

        db.session.add_all([tag1, tag2, tag3])
        db.session.commit()

        # Create Outfits
        outfit1 = Outfit(user=user1, created=datetime.now(), rating=5)
        outfit2 = Outfit(user=user2, created=datetime.now(), rating=4)

        db.session.add_all([outfit1, outfit2])
        db.session.commit()

        # Create OutfitItems
        outfit_item1 = OutfitItem(outfit=outfit1, item=item1)
        outfit_item2 = OutfitItem(outfit=outfit1, item=item2)
        outfit_item3 = OutfitItem(outfit=outfit2, item=item3)

        db.session.add_all([outfit_item1, outfit_item2, outfit_item3])
        db.session.commit()

if __name__ == '__main__':
    drop_tables()
    create_tables()
    # add_mock_data()
    print("Mock data added successfully")


# if __name__ == "__main__":
# #     seed()
# with app.app_context():
#     print(db.session.query(Items).filter_by(id=2).first().item_tags)
#     print(db.session.query(Items).filter_by(id=3).first().item_tags)
#     print(db.session.query(Items).filter_by(id=4).first().item_tags)
#     print(db.session.query(Items).filter_by(id=5).first().item_tags)
#     print(db.session.query(Items).filter_by(id=6).first().item_tags)
#     print(db.session.query(Tags).filter_by(id=1).first().item)
#     print(db.session.query(Tags).filter_by(id=1).first().category)
#     print(db.session.query(Outfit).filter_by(id=1).first().outfit_items)
#     print("Database seeded")