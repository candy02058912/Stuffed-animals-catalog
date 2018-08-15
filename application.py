#!/usr/bin/python python2.7
from flask import Flask, render_template, request, redirect,jsonify, url_for, flash

app = Flask(__name__)


@app.route('/')
@app.route('/catalog/')
def showCatalog():
    return 'Catalog'


@app.route('/catalog/<string:animal_type>/items/')
def showCategoryItems(animal_type):
    return 'Show category items'


@app.route('/catalog/<string:animal_type>/<string:animal>/')
def showAnimal(animal_type, animal):
    print animal_type, animal
    return 'pooh'

@app.route('/catalog/<string:animal>/edit/')
def editAnimal(animal):
    return 'edit pooh'


@app.route('/catalog/<string:animal>/delete/')
def deleteAnimal(animal):
    return 'delete pooh'


@app.route('/catalog/new/')
def addAnimal():
    return 'add animal'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)