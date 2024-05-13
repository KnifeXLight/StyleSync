from app import app
from db import db
from models import User, Items,Tags,Categories, Outfit,OutfitItems

def create_tables():
    with app.app_context():
        db.create_all()

def drop_tables():
    with app.app_context():
        db.drop_all()

def seed():
    with app.app_context():
        user = db.session.query(User).filter_by(id=1).first()
        print(user)
        db.session.add(Items(name="shirt",image_url="/Assets/shirt.png",user =user))
        
        db.session.commit()
        item = db.session.query(Items).filter_by(id=1).first()
        print(item)
        print(item.user)
        db.session.add(Items(name="pants",image_url="/Assets/jeans.png",user = user))
        db.session.add(Items(name="shoes",image_url="/Assets/shoesghost.png",user = user))
        db.session.add(Items(name="hat",image_url="/Assets/hatghost.png",user = user))
        db.session.add(Items(name="gloves",image_url="/Assets/bracelet.png",user = user))
        db.session.add(Items(name="scarf",image_url="/Assets/watch.png",user = user))
        db.session.add(Categories(name="shirt"))
        db.session.add(Categories(name="pants"))
        db.session.add(Categories(name="shoes"))
        db.session.add(Categories(name="hat"))
        db.session.add(Categories(name="gloves"))
        db.session.add(Categories(name="scarf"))
        db.session.add(Categories(name="Summer"))
        db.session.add(Categories(name="Winter"))
        db.session.add(Categories(name="Spring"))
        db.session.add(Categories(name="Fall"))
        db.session.add(Categories(name="Casual"))
        db.session.add(Categories(name="Formal"))
        db.session.add(Categories(name="Work"))
        db.session.add(Categories(name="Party"))
        db.session.add(Categories(name="Sport"))
        db.session.add(Categories(name="Outdoor"))
        db.session.add(Categories(name="Indoor"))
        db.session.add(Categories(name="Rain"))
        db.session.add(Categories(name="Snow"))
        db.session.add(Categories(name="Sun"))
        db.session.add(Categories(name="Cloud"))
        db.session.add(Categories(name="Wind"))
        db.session.add(Categories(name="Hot"))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=1).first(),category = db.session.query(Categories).filter_by(id=1).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=2).first(),category = db.session.query(Categories).filter_by(id=2).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=3).first(),category = db.session.query(Categories).filter_by(id=3).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=4).first(),category = db.session.query(Categories).filter_by(id=4).first()))
        db.session.add(Tags(item= db.session.query(Items).filter_by(id=5).first(),category = db.session.query(Categories).filter_by(id=5).first()))
        db.session.add(Tags(item= db.session.query(Items).filter_by(id=6).first(),category = db.session.query(Categories).filter_by(id=6).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=1).first(),category = db.session.query(Categories).filter_by(id=7).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=2).first(),category = db.session.query(Categories).filter_by(id=8).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=3).first(),category = db.session.query(Categories).filter_by(id=9).first()))
        db.session.add(Tags(item = db.session.query(Items).filter_by(id=4).first(),category = db.session.query(Categories).filter_by(id=10).first()))
        db.session.commit()
        db.session.add(Outfit(user = user))
        db.session.commit()
        outfit = db.session.query(Outfit).filter_by(id=1).first()
        db.session.add(OutfitItems(outfit=outfit,item=db.session.query(Items).filter_by(id=1).first()))
        db.session.add(OutfitItems(outfit=outfit,item=db.session.query(Items).filter_by(id=2).first()))
        db.session.add(OutfitItems(outfit=outfit,item=db.session.query(Items).filter_by(id=3).first()))
        db.session.add(OutfitItems(outfit=outfit,item=db.session.query(Items).filter_by(id=4).first()))
        db.session.add(OutfitItems(outfit=outfit,item=db.session.query(Items).filter_by(id=5).first()))
        db.session.add(OutfitItems(outfit=outfit,item=db.session.query(Items).filter_by(id=6).first()))
        db.session.commit()



if __name__ == "__main__":
    # drop_tables()
    # create_tables()
    seed()
with app.app_context():
    print("Database seeded")