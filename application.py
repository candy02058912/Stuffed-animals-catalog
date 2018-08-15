#!/usr/bin/python python2.7
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash

app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    return render_template('catalog.html')


@app.route('/catalog/<string:animal_type>/items/')
def showCategoryItems(animal_type):
    return render_template('category_items.html')


@app.route('/catalog/<string:animal_type>/<string:animal>/')
def showAnimal(animal_type, animal):
    return render_template('animal.html')

@app.route('/catalog/<string:animal>/edit/')
def editAnimal(animal):
    return render_template('edit_animal.html')


@app.route('/catalog/<string:animal>/delete/')
def deleteAnimal(animal):
    return render_template('delete_animal.html')


@app.route('/catalog/new/')
def addAnimal():
    return render_template('add_animal.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)