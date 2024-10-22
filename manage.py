from app import create_app
from db import db
from models import User, Item,Category, Outfit,Filter,Tag,OutfitItem
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import sys

# Create all tables
def create_tables(app):
    with app.app_context():
        db.create_all()

# Drop all tables
def drop_tables(app):
    with app.app_context():
        db.drop_all()


# Add mock data
def add_mock_data(app):
    with app.app_context():
        
        name1 = "Test User 1"
        email1 = "test1@example.com"
        password1 = "testpassword"

        name2 = "Test User 2"
        email2 = "test2@example.com"
        password2 = "testpassword"
        # Create Users
        user1 = User(name=name1, email=email1, password=generate_password_hash(password1, method="scrypt"))
        user2 = User(name=name2, email=email2, password=generate_password_hash(password2, method="scrypt"))
        
        db.session.add_all([user1, user2])
        db.session.commit()

# Query for users
        user1 = db.session.query(User).filter_by(id=1).first()
        user2 = db.session.query(User).filter_by(id=2).first()

        # Create Categories
        category2 = Category(name='Weather')
        category3 = Category(name='Style')
        category4 = Category(name='Upper Wear')
        category5 = Category(name='Leg Wear')
        category6 = Category(name='Shoes')
        category7 = Category(name='Accessories')
        category8 = Category(name='Outer Wear')

        db.session.add_all([category2, category3, category4, category5, category6, category7, category8])
        db.session.commit()

        # Create Filters
        # Types
        filter3 = Filter(name='Shirt', category=category4)
        filter4 = Filter(name='Suit', category=category4)
        filter5 = Filter(name='Jacket', category=category8)
        filter6 = Filter(name='Dress', category=category4)
        filter18 = Filter(name='Hoodie', category=category8)
        filter19 = Filter(name='Sweater', category=category8)
        filter20 = Filter(name='T-shirt', category=category4)
        filter21 = Filter(name='Vest', category=category4)
        filter22 = Filter(name='Top', category=category4)
        filter23 = Filter(name='Coat', category=category8)

        filter24 = Filter(name='Shorts', category=category5)
        filter25 = Filter(name='Skirt', category=category5)
        filter26 = Filter(name='Jeans', category=category5)
        filter27 = Filter(name='Pants', category=category5)

        filter28 = Filter(name='Flip Flops', category=category6)
        filter29 = Filter(name='Boots', category=category6)
        filter30 = Filter(name='Sandals', category=category6)
        filter31 = Filter(name='Loafers', category=category6)
        filter32 = Filter(name='Heels', category=category6)
        filter33 = Filter(name='Dress Shoes', category=category6)

        filter34 = Filter(name='Scarf', category=category7)
        filter35 = Filter(name='Socks', category=category7)
        filter36 = Filter(name='Bracelet', category=category7)
        filter37 = Filter(name='Hat', category=category7)
        filter38 = Filter(name='Tote', category=category7)
        filter39 = Filter(name='Cap', category=category7)
        filter40 = Filter(name='Purse', category=category7)
        filter41 = Filter(name='Tie', category=category7)


        # Weather
        filter7 = Filter(name='Sunny', category=category2)
        filter8 = Filter(name='Windy', category=category2)
        filter9 = Filter(name='Snowy', category=category2)
        filter10 = Filter(name='Clear', category=category2)
        filter11 = Filter(name='Rainy', category=category2)

        # Style
        filter12 = Filter(name='Casual', category=category3)
        filter13 = Filter(name='Street', category=category3)
        filter14 = Filter(name='Formal', category=category3)
        filter15 = Filter(name='Sporty', category=category3)
        filter16 = Filter(name='Classic', category=category3)
        filter17 = Filter(name='Fancy', category=category3)

        db.session.add_all([filter3,filter4,filter5,filter6,filter7,filter8,filter9,filter10,filter11,filter12,filter13,
                            filter14,filter15,filter16,filter17, filter18, filter19, filter20, filter21, filter22, filter23,
                            filter24, filter25, filter26, filter27, filter28, filter29, filter30, filter31, filter32, filter33,
                            filter34, filter35, filter36, filter37, filter38, filter39, filter40, filter41])
        db.session.commit()

        # Create Items
        # User 1 items
        # User 1 accessories
        item2 = Item(name='beige tote', image_url='/items/Accessories/beige_tote.png', user=user1)
        item3 = Item(name='black purse', image_url='/items/Accessories/black_purse.png', user=user1)
        item4 = Item(name='ghostbracelet3', image_url='/items/Accessories/ghostbracelet3.png', user=user1)
        item5 = Item(name='ghosthat2', image_url='/items/Accessories/ghosthat2.png', user=user1)
        item6 = Item(name='olive green tote', image_url='/items/Accessories/olive_green_tote.png', user=user1)
        item7 = Item(name='white cap', image_url='/items/Accessories/white_cap.png', user=user1)
    
        # User 1 bottoms
        item8 = Item(name='black leather A-line skirt', image_url='/items/bottoms/black_leather_A-line_skirt.png', user=user1)
        item9 = Item(name='black leather H-line skirt', image_url='/items/bottoms/black_leather_H-line_skirt.png', user=user1)
        item10 = Item(name='dark washed denim bell jeans', image_url='/items/bottoms/dark_washed_denim_bell_jeans.png', user=user1)
        item11 = Item(name='light washed denim skirt', image_url='/items/bottoms/light_washed_denim_skirt.png', user=user1)
        item12 = Item(name='dark washed denim short', image_url='/items/bottoms/dark_washed_denim_short.png', user=user1)
        item13 = Item(name='dark washed jeans', image_url='/items/bottoms/dark_washed_jeans.png', user=user1)
        item14 = Item(name='light pink tennis skirt', image_url='/items/bottoms/light_pink_tennis_skirt.png', user=user1)

        # User 1 tops
        item15 = Item(name='black short sleeve dress', image_url='/items/overalls&dresses/black_short_sleeve_dress.png', user=user1)
        item16 = Item(name='black sleeveless dress', image_url='/items/overalls&dresses/black_sleeveless_dress.png', user=user1)
        item45 = Item(name='black crop top', image_url='/items/overalls&dresses/black_crop_top.png', user=user1)
        item46 = Item(name='black pink windbreaker', image_url='/items/overalls&dresses/blackpink_windbreaker.png', user=user1)
        item47 = Item(name='red jacket', image_url='/items/overalls&dresses/red_jacket.png', user=user1)
        item48 = Item(name='red raincoat', image_url='/items/overalls&dresses/red_raincoat.png', user=user1)

        # User 1 shoes
        item17 = Item(name='black knee high boots', image_url='/items/shoes/black_knee_high_boots.png', user=user1)
        item18 = Item(name='black leather loafers', image_url='/items/shoes/black_leather_loafers.png', user=user1)
        item19 = Item(name='black stilettos', image_url='/items/shoes/black_stilettos.png', user=user1)
        item20 = Item(name='brown flat sandals', image_url='/items/shoes/brown_flat_sandals.png', user=user1)
        item21 = Item(name='camel ankle boots', image_url='/items/shoes/camel_ankle_boots.png', user=user1)

        # User 2 items
        # User 2 accessories
        item22 = Item(name='black scarf', image_url='/items/Accessories/black_scarf.png', user=user2)
        item23 = Item(name='black socks', image_url='/items/Accessories/black_socks.png', user=user2)
        item24 = Item(name='ghostbracelet2', image_url='/items/Accessories/ghostbracelet2.png', user=user2)
        item25 = Item(name='ghosthat3', image_url='/items/Accessories/ghosthat3.png', user=user2)
        item26 = Item(name='ghosthat4', image_url='/items/Accessories/ghosthat4.png', user=user2)
        item27 = Item(name='grey scarf', image_url='/items/Accessories/grey_scarf.png', user=user2)
        item28 = Item(name='red tie', image_url='/items/Accessories/red_tie.png', user=user2)

        # User 2 bottoms
        item29 = Item(name='beige pants', image_url='/items/bottoms/beige_pants.png', user=user2)
        item41 = Item(name='brown shorts', image_url='/items/bottoms/brown_shorts.png', user=user2)

        # User 2 shoes
        item30 = Item(name='black flip flops', image_url='/items/shoes/black_flip_flops.png', user=user2)
        item31 = Item(name='black leather dress shoes', image_url='/items/shoes/black_leather_dress_shoes.png', user=user2)
        item42 = Item(name='rain boots', image_url='/items/shoes/rain_boots.png', user=user2)

        # User 2 tops
        item32 = Item(name='black dress shirt', image_url='/items/tops/black_dress_shirt.png', user=user2)
        item33 = Item(name='black hoodie', image_url='/items/tops/black_hoodie.png', user=user2)
        item34 = Item(name='black leather jacket', image_url='/items/tops/black_leather_jacket.png', user=user2)
        item35 = Item(name='black nike hoodie', image_url='/items/tops/black_nike_hoodie.png', user=user2)
        item36 = Item(name='black suit top and tie', image_url='/items/tops/black_suit_top_and_tie.png', user=user2)
        item37 = Item(name='black suit top', image_url='/items/tops/black_suit_top.png', user=user2)
        item38 = Item(name='blue sweater', image_url='/items/tops/blue_sweater.png', user=user2)
        item39 = Item(name='dusty blue sweater', image_url='/items/tops/dusty_blue_sweater.png', user=user2)
        item40 = Item(name='white dress shirt', image_url='/items/tops/white_dress_shirt.png', user=user2)
        item43 = Item(name='dry fit', image_url='/items/tops/dryfit_tshirt.png', user=user2)
        item44 = Item(name='grey tshirt', image_url='/items/tops/grey_tshirt.png', user=user2)

        db.session.add_all([item2,item3,item4,item5,item6,item7,item8,item9,
                            item10,item11,item12,item13,item14,item15,item16,item17,item18,item19,
                            item20,item21,item22,item23,item24,item25,item26,item27,item28,item29,
                            item30,item31,item32,item33,item34,item35,item36,item37,item38,item39,
                            item40, item41, item42, item43, item44, item45, item46, item47, item48])
        db.session.commit()

        # Create Tags
        # User 1 tags
        # User 1 accessories
        tag1 = Tag(item=item2, category=category7, filter=filter38)
        tag2 = Tag(item=item3, category=category7, filter=filter40)
        tag3 = Tag(item=item4, category=category7, filter=filter36)
        tag4 = Tag(item=item5, category=category7, filter=filter37)
        tag5 = Tag(item=item6, category=category7, filter=filter38)
        tag6 = Tag(item=item7, category=category7, filter=filter39)
        tag40 = Tag(item=item7, category=category2, filter=filter7)
        tag52 = Tag(item=item2, category=category3, filter=filter14)
        tag53 = Tag(item=item3, category=category3, filter=filter12)
        tag54 = Tag(item=item4, category=category3, filter=filter17)
        tag55 = Tag(item=item5, category=category3, filter=filter13)
        tag56 = Tag(item=item6, category=category3, filter=filter14)
        tag57 = Tag(item=item7, category=category3, filter=filter15)

        # User 1 bottoms
        tag7 = Tag(item=item8, category=category5, filter=filter25)
        tag8 = Tag(item=item9, category=category5, filter=filter25)
        tag9 = Tag(item=item10, category=category5, filter=filter26)
        tag10 = Tag(item=item11, category=category5, filter=filter25)
        tag11 = Tag(item=item12, category=category5, filter=filter24)
        tag12 = Tag(item=item13, category=category5, filter=filter26)
        tag13 = Tag(item=item14, category=category5, filter=filter25)
        tag41 = Tag(item=item14, category=category2, filter=filter7)
        tag58 = Tag(item=item8, category=category3, filter=filter13)
        tag59 = Tag(item=item9, category=category3, filter=filter14)
        tag60 = Tag(item=item10, category=category3, filter=filter12)
        tag61 = Tag(item=item11, category=category3, filter=filter12)
        tag62 = Tag(item=item12, category=category3, filter=filter12)
        tag63 = Tag(item=item13, category=category3, filter=filter12)
        tag64 = Tag(item=item14, category=category3, filter=filter15)

        # User 1 tops
        tag14 = Tag(item=item15, category=category4, filter=filter6)
        tag15 = Tag(item=item16, category=category4, filter=filter6)
        tag65 = Tag(item=item15, category=category3, filter=filter14)
        tag66 = Tag(item=item16, category=category3, filter=filter17)
        tag101 = Tag(item=item45, category=category4, filter=filter22)
        tag102 = Tag(item=item45, category=category3, filter=filter16)
        tag103 = Tag(item=item45, category=category2, filter=filter10)
        tag104 = Tag(item=item46, category=category8, filter=filter5)
        tag105 = Tag(item=item46, category=category3, filter=filter13)
        tag106 = Tag(item=item46, category=category2, filter=filter8)
        tag107 = Tag(item=item47, category=category8, filter=filter23)
        tag108 = Tag(item=item47, category=category3, filter=filter17)
        tag109 = Tag(item=item47, category=category2, filter=filter5)
        tag110 = Tag(item=item48, category=category8, filter=filter8)
        tag111 = Tag(item=item48, category=category2, filter=filter16)
        tag112 = Tag(item=item48, category=category2, filter=filter11)

        # User 1 shoes
        tag16 = Tag(item=item17, category=category6, filter=filter29)
        tag17 = Tag(item=item18, category=category6, filter=filter31)
        tag18 = Tag(item=item19, category=category6, filter=filter32)
        tag19 = Tag(item=item20, category=category6, filter=filter30)
        tag20 = Tag(item=item21, category=category6, filter=filter29)
        tag42 = Tag(item=item20, category=category2, filter=filter7)
        tag43 = Tag(item=item21, category=category2, filter=filter9)
        tag67 = Tag(item=item17, category=category3, filter=filter13)
        tag68 = Tag(item=item18, category=category3, filter=filter14)
        tag69 = Tag(item=item19, category=category3, filter=filter17)
        tag70 = Tag(item=item20, category=category3, filter=filter12)
        tag71 = Tag(item=item21, category=category3, filter=filter17)

        # User 2 tags
        # User 2 accessories
        tag21 = Tag(item=item22, category=category7, filter=filter34)
        tag22 = Tag(item=item23, category=category7, filter=filter35)
        tag23 = Tag(item=item24, category=category7, filter=filter36)
        tag24 = Tag(item=item25, category=category7, filter=filter37)
        tag25 = Tag(item=item26, category=category7, filter=filter37)
        tag26 = Tag(item=item27, category=category7, filter=filter34)
        tag27 = Tag(item=item28, category=category7, filter=filter41)
        tag44 = Tag(item=item22, category=category2, filter=filter8)
        tag45 = Tag(item=item27, category=category2, filter=filter9)
        tag72 = Tag(item=item22, category=category3, filter=filter12)
        tag73 = Tag(item=item23, category=category3, filter=filter14)
        tag74 = Tag(item=item24, category=category3, filter=filter13)
        tag75 = Tag(item=item25, category=category3, filter=filter13)
        tag76 = Tag(item=item26, category=category3, filter=filter13)
        tag77 = Tag(item=item27, category=category3, filter=filter12)
        tag78 = Tag(item=item28, category=category3, filter=filter14)

        # User 2 bottoms
        tag28 = Tag(item=item29, category=category5, filter=filter27)
        tag79 = Tag(item=item29, category=category3, filter=filter12)
        tag91 = Tag(item=item41, category=category5, filter=filter24)
        tag92 = Tag(item=item41, category=category3, filter=filter16)

        # User 2 shoes
        tag29 = Tag(item=item30, category=category6, filter=filter28)
        tag30 = Tag(item=item31, category=category6, filter=filter33)
        tag46 = Tag(item=item30, category=category2, filter=filter7)
        tag80 = Tag(item=item30, category=category3, filter=filter12)
        tag81 = Tag(item=item31, category=category3, filter=filter14)
        tag93 = Tag(item=item42, category=category6, filter=filter29)
        tag94 = Tag(item=item42, category=category2, filter=filter11)

        # User 2 tops
        tag31 = Tag(item=item32, category=category4, filter=filter3)
        tag32 = Tag(item=item33, category=category4, filter=filter18)
        tag33 = Tag(item=item34, category=category4, filter=filter5)
        tag34 = Tag(item=item35, category=category4, filter=filter18)
        tag35 = Tag(item=item36, category=category4, filter=filter4)
        tag36 = Tag(item=item37, category=category4, filter=filter4)
        tag37 = Tag(item=item38, category=category4, filter=filter19)
        tag38 = Tag(item=item39, category=category4, filter=filter19)
        tag39 = Tag(item=item40, category=category4, filter=filter3)
        tag47 = Tag(item=item33, category=category2, filter=filter8)
        tag48 = Tag(item=item34, category=category2, filter=filter9)
        tag49 = Tag(item=item35, category=category2, filter=filter8)
        tag50 = Tag(item=item38, category=category2, filter=filter9)
        tag51 = Tag(item=item39, category=category2, filter=filter8)
        tag82 = Tag(item=item32, category=category3, filter=filter14)
        tag83 = Tag(item=item33, category=category3, filter=filter12)
        tag84 = Tag(item=item34, category=category3, filter=filter13)
        tag85 = Tag(item=item35, category=category3, filter=filter12)
        tag86 = Tag(item=item36, category=category3, filter=filter14)
        tag87 = Tag(item=item37, category=category3, filter=filter17)
        tag88 = Tag(item=item38, category=category3, filter=filter12)
        tag89 = Tag(item=item39, category=category3, filter=filter12)
        tag90 = Tag(item=item40, category=category3, filter=filter16)
        tag99 = Tag(item=item43, category=category4, filter=filter20)
        tag95 = Tag(item=item43, category=category2, filter=filter7)
        tag96 = Tag(item=item43, category=category3, filter=filter15)
        tag100 = Tag(item=item44, category=category4, filter=filter20)
        tag97 = Tag(item=item44, category=category2, filter=filter10)
        tag98 = Tag(item=item44, category=category3, filter=filter12)

        db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6, tag7, tag8, tag9,
                            tag10, tag11, tag12, tag13, tag14, tag15, tag16, tag17, tag18, tag19,
                            tag20, tag21, tag22, tag23, tag24, tag25, tag26, tag27, tag28, tag29,
                            tag30, tag31, tag32, tag33, tag34, tag35, tag36, tag37, tag38, tag39,
                            tag40, tag41, tag42, tag43, tag44, tag45, tag46, tag47, tag48, tag49,
                            tag50, tag51, tag52, tag53, tag54, tag55, tag56, tag57, tag58, tag59,
                            tag60, tag61, tag62, tag63, tag64, tag65, tag66, tag67, tag68, tag69,
                            tag70, tag71, tag72, tag73, tag74, tag75, tag76, tag77, tag78, tag79,
                            tag80, tag81, tag82, tag83, tag84, tag85, tag86, tag87, tag88, tag89,
                            tag90, tag91, tag92, tag93, tag94, tag95, tag96, tag97, tag98, tag99,
                            tag100, tag101, tag102, tag103, tag104, tag105, tag106, tag107, tag108, tag109,
                            tag110, tag111, tag112])
        db.session.commit()

        # Create Outfits
        outfit1 = Outfit(user=user1, created=datetime.now(), rating=5)
        outfit2 = Outfit(user=user1, created=datetime.now(), rating=4)
        outfit5 = Outfit(user=user1, created=datetime.now(), rating=5)

        outfit3 = Outfit(user=user2, created=datetime.now(), rating=4)
        outfit4 = Outfit(user=user2, created=datetime.now(), rating=5)
        outfit6 = Outfit(user=user2, created=datetime.now(), rating=5)

        db.session.add_all([outfit1, outfit2, outfit3, outfit4, outfit5, outfit6])
        db.session.commit()

        # Create OutfitItems
        # User 1 Outfit 1
        outfit_item1 = OutfitItem(outfit=outfit1, item=item6)
        outfit_item2 = OutfitItem(outfit=outfit1, item=item9)
        outfit_item3 = OutfitItem(outfit=outfit1, item=item15)
        outfit_item4 = OutfitItem(outfit=outfit1, item=item19)

        # User 1 Outfit 2
        outfit_item5 = OutfitItem(outfit=outfit2, item=item7)
        outfit_item6 = OutfitItem(outfit=outfit2, item=item14)
        outfit_item7 = OutfitItem(outfit=outfit2, item=item16)
        outfit_item8 = OutfitItem(outfit=outfit2, item=item20)

        # User 1 Outfit 3
        outfit_item17 = OutfitItem(outfit=outfit5, item=item7)
        outfit_item18 = OutfitItem(outfit=outfit5, item=item14)
        outfit_item19 = OutfitItem(outfit=outfit5, item=item45)
        outfit_item20 = OutfitItem(outfit=outfit5, item=item20)

        # User 2 Outfit 1
        outfit_item9 = OutfitItem(outfit=outfit3, item=item27)
        outfit_item10 = OutfitItem(outfit=outfit3, item=item29)
        outfit_item11 = OutfitItem(outfit=outfit3, item=item30)
        outfit_item12 = OutfitItem(outfit=outfit3, item=item39)

        # User 2 Outfit 2
        outfit_item13 = OutfitItem(outfit=outfit4, item=item28)
        outfit_item14 = OutfitItem(outfit=outfit4, item=item29)
        outfit_item15 = OutfitItem(outfit=outfit4, item=item31)
        outfit_item16 = OutfitItem(outfit=outfit4, item=item36)

        # User 2 Outfit 3
        outfit_item21 = OutfitItem(outfit=outfit6, item=item24)
        outfit_item22 = OutfitItem(outfit=outfit6, item=item41)
        outfit_item23 = OutfitItem(outfit=outfit6, item=item42)
        outfit_item24 = OutfitItem(outfit=outfit6, item=item44)

        db.session.add_all([outfit_item1, outfit_item2, outfit_item3, outfit_item4, outfit_item5, outfit_item6, outfit_item7,
                            outfit_item8, outfit_item9, outfit_item10, outfit_item11, outfit_item12, outfit_item13,
                            outfit_item14, outfit_item15, outfit_item16, outfit_item17, outfit_item18, outfit_item19,
                            outfit_item20, outfit_item21, outfit_item22, outfit_item23, outfit_item24])
        db.session.commit()

def main():
    argv = sys.argv
    if len(argv) > 1 and argv[1] == 'drop':
        drop_tables(app=create_app())
        print("Tables dropped successfully")
        sys.exit()
    elif len(argv) > 1 and argv[1] == 'create':
        create_tables(app=create_app())
        print("Tables created successfully")
        sys.exit()
    elif len(argv) > 1 and argv[1] == 'seed':
        add_mock_data(app=create_app())
        print("Mock data added successfully")
        sys.exit()
    elif len(argv) > 1 and argv[1] == 'reset':
        drop_tables(app=create_app())
        create_tables(app=create_app())
        add_mock_data(app=create_app())
        print("Tables reset successfully")
        sys.exit()
    else:
        print("Invalid command. Please use 'create', 'drop', or 'seed' as arguments")
        sys.exit()

if __name__ == '__main__':
    main()
