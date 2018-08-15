from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///stuffedanimals.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Ian Lin", email="ian_lin@example.com",
             picture="https://i.imgur.com/ZOcCoH1.png")
session.add(User1)
session.commit()

# Bear Stuffed Animals
category1 = Category(name="Bear")

session.add(category1)
session.commit()

animal1 = CategoryItem(user_id=1, name="Winnie the Pooh", description="A bear with a very little brain.",
                     picture="https://i.imgur.com/8y1Ugtn.jpg", category=category1)

session.add(animal1)
session.commit()

# Pig Stuffed Animals
category2 = Category(name="Pig")

session.add(category2)
session.commit()

animal1 = CategoryItem(user_id=1, name="Piglet", description="Winnie the Pooh's best friend.",
                     picture="https://i.imgur.com/QPz4qOm.jpg", category=category2)

session.add(animal1)
session.commit()

# Pig Stuffed Animals
category3 = Category(name="Mouse")

session.add(category3)
session.commit()

animal1 = CategoryItem(user_id=1, name="Pikachu", description="A friendly electric mouse from Pokemon.",
                     picture="https://i.imgur.com/acdAGy4.jpg", category=category3)

session.add(animal1)
session.commit()

print "added initial stuffed animals"