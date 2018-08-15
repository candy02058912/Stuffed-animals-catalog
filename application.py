#!/usr/bin/python python2.7
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User

app = Flask(__name__)

engine = create_engine('sqlite:///stuffedanimals.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# every page has categories
categories = session.query(Category).all()


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    animals = session.query(CategoryItem).order_by(CategoryItem.id.desc())
    return render_template(
        'catalog.html',
        categories=categories,
        animals=animals
    )


@app.route('/catalog/<string:animal_type>/items/')
def showCategoryItems(animal_type):
    category_id = session.query(Category).filter_by(name=animal_type).one().id
    animals = session.query(CategoryItem).filter_by(category_id=category_id)
    return render_template('category_items.html', categories=categories, animal_type=animal_type, animals=animals)


@app.route('/catalog/<string:animal_type>/<string:animal>/')
def showAnimal(animal_type, animal):
    animal = session.query(CategoryItem).filter_by(name=animal).one()
    return render_template('animal.html', categories=categories, animal=animal)


@app.route('/catalog/<string:animal>/edit/')
def editAnimal(animal):
    return render_template('edit_animal.html', categories=categories)


@app.route('/catalog/<string:animal>/delete/')
def deleteAnimal(animal):
    return render_template('delete_animal.html', categories=categories)


@app.route('/catalog/new/')
def addAnimal():
    return render_template('add_animal.html', categories=categories)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
