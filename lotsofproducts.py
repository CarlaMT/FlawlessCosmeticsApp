from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String
from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///makeupcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='http://placeimg.com/400/400/any')
session.add(user1)
session.commit()


# Category 1: Face
category1 = Category(name="Face", id="1",
                     description="Smooth paraben free products, \
                     no animal testing. Oil-controlling formulas \
                     that offers a matte finish with medium to full \
                     coverage.")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(name="Fountain of Youth Foundation", id="1",
                             description="Natural, chemical free makeup \
                             made for your skintone, from Flawless Cosmetics",
                             price="$10.00", category=category1)
session.add(categoryItem1)
session.commit()


categoryItem2 = CategoryItem(name="Powder Puff Magic", id="2",
                             description="Custom made full coverage foundation,\
                             giving you a finished look,great\
                             for mature skin.",
                             price="$45.00", category=category1)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Blushing Bride", id="3",
                             description="Custom blended beautiful melon\
                             colored blush, perfect for summer. ",
                             price="$30.00", category=category1)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Blush Brush", id="4",
                             description="Flexible bristles and gently \
                             tapered edges makes this brush perfect \
                             for applying blush.",
                             price="$40.00", category=category1)
session.add(categoryItem4)
session.commit()


# Category 2: Lips
category2 = Category(name="Lips", id="2",
                     description="Paraben free lip products.\
                     Special shades, matte finish for all skin types.\
                     Special Packaging is available.")
session.add(category2)
session.commit()

categoryItem1 = CategoryItem(name="Luscious Lips", id="5",
                             description="Sultry shimmery lipgloss,\
                             perfect for every occasion. ",
                             price="$10.00", category=category2)
session.add(categoryItem1)
session.commit()


categoryItem2 = CategoryItem(name="Ruby Red", id="6",
                             description="Paraben free ruby red \
                             lipstick with a matte finish, .",
                             price="$45.00", category=category2)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Get It Straight Lipliner", id="7",
                             description="Precision tip lip \
                             to outline lips. ",
                             price="$15.00", category=category2)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Sticky Lips Lip Balm", id="8",
                             description="Chemical free lip balm to \
                             moisten dry chapped lips.",
                             price="$40.00", category=category2)
session.add(categoryItem4)
session.commit()


# Category 3: Eyes
category3 = Category(name="Eyes", id="3",
                     description="Eye products in all shades!\
                     Great pigmentation, blend beautifully in\
                     rich shades special packaging available.")

session.add(category3)
session.commit()

categoryItem1 = CategoryItem(name="Black Eyeliner Pencil", id="9",
                             description="Perfect pencil to define the\
                             eyes to create a variety of\
                             aesthetic effects .",
                             price="$10.00", category=category3)
session.add(categoryItem1)
session.commit()


categoryItem2 = CategoryItem(name="Brown Eyeliner Pencil", id="10",
                             description="Perfect pencil to define\
                             the eyes to create a variety of \
                             effects .",
                             price="$45.00", category=category3)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Purple Eyeliner Pencil", id="11",
                             description="Perfect pencil to define the\
                             eyes to create a variety of aesthetic effects .",
                             price="$15.00", category=category3)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Blue Eyeliner Pencil", id="12",
                             description="Perfect pencil to define\
                             the eyes to create a variety \
                             of aesthetic effects .",
                             price="$40.00", category=category3)
session.add(categoryItem4)
session.commit()


# Category 4: Nails
category4 = Category(name="Nails", id="4",
                     description="Discover our latest \
                      of nail polish and nail care \
                      products. Get inspiration for your next manicure!")

session.add(category4)
session.commit()

categoryItem1 = CategoryItem(name="Summer Glow Nails", id="13",
                             description="Orangy bright nail \
                             great summer color!",
                             price="$20.00", category=category4)
session.add(categoryItem1)
session.commit()


categoryItem2 = CategoryItem(name="Mirror Nails", id="14",
                             description="Chrome powder\
                             transform your nails! .",
                             price="$45.00", category=category4)
session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Black Widow", id="15",
                             description="Dark nail polish,\
                             perfect color for Halloween. ",
                             price="$15.00", category=category4)
session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Winter Wonderland", id="16",
                             description="White frosted nail polish,\
                             with a shimmery shine.",
                             price="$40.00", category=category4)
session.add(categoryItem4)
session.commit()


print("added menu items!")
