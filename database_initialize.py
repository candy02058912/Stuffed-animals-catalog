#!/usr/bin/python python2.7
import json
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

# Create initial data
data = json.loads(open('data.json', 'r').read())
for category in data:
    new_category = Category(name=category)
    session.add(new_category)
    session.commit()
    for item in data[category]:
        new_item = CategoryItem(
            user_id=item['user_id'],
            name=item['name'],
            description=item['description'],
            picture=item['picture'],
            category=new_category
        )
        session.add(new_item)
        session.commit()

print "added initial stuffed animals"
