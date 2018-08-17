#!/usr/bin/python python2.7
import httplib2
import json
import os
import random
import requests
import string
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash, make_response)
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# Initialization
app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))
CLIENT_ID = json.loads(
    open(os.path.join(path, 'client_secrets.json'), 'r').read())['web']['client_id']
engine = create_engine(
    'sqlite:///stuffedanimals.db', connect_args={'check_same_thread': False}
)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Every page has categories
categories = session.query(Category).all()


@app.route('/')
@app.route('/catalog/')
def show_catalog():
    """Shows the whole catalog to the public"""
    animals = session.query(CategoryItem).order_by(CategoryItem.create_time.desc())
    return render_template(
        'catalog.html',
        categories=categories,
        animals=animals
    )


@app.route('/catalog/<string:animal_type>/items/')
def show_category_items(animal_type):
    """Shows item by category to the public"""
    category_id = session.query(Category).filter_by(name=animal_type).one_or_none().id
    animals = session.query(CategoryItem).filter_by(category_id=category_id)
    return render_template(
        'category_items.html',
        categories=categories,
        animal_type=animal_type,
        animals=animals
    )


@app.route('/catalog/<string:animal_type>/<string:animal_name>/')
def show_animal(animal_type, animal_name):
    """Show the individual animal"""
    animal = session.query(CategoryItem).filter_by(
        name=animal_name, category_id=animal_type).one_or_none()
    creator = get_user_info(animal.user_id)
    if 'username' not in login_session or \
            creator.id != login_session['user_id']:
        return render_template(
            'animal.html', categories=categories, animal=animal, public=True)
    return render_template('animal.html', categories=categories, animal=animal)


@app.route('/catalog/<string:animal_name>/edit/', methods=['GET', 'POST'])
def edit_animal(animal_name):
    """Edit a particular animal"""
    animal = session.query(CategoryItem).filter_by(name=animal_name).one_or_none()
    creator = get_user_info(animal.user_id)
    if 'username' not in login_session or\
            creator.id != login_session['user_id']:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            animal.name = request.form['name']
        if request.form['picture']:
            animal.picture = request.form['picture']
        if request.form['description']:
            animal.description = request.form['description']
        if request.form['category']:
            animal.category = session.query(Category).filter_by(
                name=request.form['category']).one_or_none()
        session.add(animal)
        session.commit()
        flash("Edited!")
        return redirect(url_for(
            'show_category_items', animal_type=request.form['category']
        ))
    return render_template(
        'edit_animal.html',
        categories=categories,
        animal=animal
    )


@app.route('/catalog/<string:animal_name>/delete/', methods=['GET', 'POST'])
def delete_animal(animal_name):
    """Delete a particular animal"""
    animal = session.query(CategoryItem).filter_by(name=animal_name).one_or_none()
    creator = get_user_info(animal.user_id)
    if 'username' not in login_session or\
            creator.id != login_session['user_id']:
        return redirect('/login')
    if request.method == 'POST':
        session.delete(animal)
        session.commit()
        flash("%s from %s has been deleted!" %
              (animal.name, animal.category.name))
        return redirect(
            url_for('show_category_items', animal_type=animal.category.name)
        )
    return render_template(
        'delete_animal.html',
        categories=categories,
        animal_name=animal_name
    )


@app.route('/catalog/new/', methods=['GET', 'POST'])
def add_animal():
    """Add an animal"""
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        animal = CategoryItem(
            name=request.form['name'],
            picture=request.form['picture'],
            description=request.form['description'],
            user_id=login_session['user_id'],
            category=session.query(Category).filter_by(
                name=request.form['category']).one_or_none()
        )
        session.add(animal)
        session.commit()
        flash("Added %s to %s!" %
              (request.form['name'], request.form['category']))
        return redirect(url_for('show_catalog'))
    return render_template('add_animal.html', categories=categories)


# User login
@app.route('/login')
def login():
    # State can help prevent CSRF by generating a different state on each login
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', categories=categories, state=state, client_id=CLIENT_ID)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code.
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object.
        oauth_flow = flow_from_clientsecrets(os.path.join(path, 'client_secrets.json'), scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # If user does not exist, create a new row in db.
    user_id = get_user_id(login_session['email'])
    if not user_id:
        user_id = create_user(login_session)
    login_session['user_id'] = user_id
    flash('Hello %s!' % (login_session['username']))
    return 'Logged In'


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % (
        login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Remove logged in info from login session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Logged out successfully!")
        return redirect('/')
    else:
        response = make_response(
            json.dumps("Failed to revoke token for given user.", 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/api/catalog/')
def catalog_api():
    """Returns the whole catalog in JSON format"""
    animals = session.query(CategoryItem).all()
    return jsonify(animals=[animal.serialize for animal in animals])


@app.route('/api/catalog/<string:animal_type>/')
def catalog_by_category_api(animal_type):
    """Returns the animals by category in JSON format"""
    category = session.query(Category).filter_by(name=animal_type).one_or_none()
    animals = session.query(CategoryItem).filter_by(category=category)
    return jsonify(animals=[animal.serialize for animal in animals])


@app.route('/api/catalog/<string:animal_type>/<string:animal_name>')
def animal_api(animal_type, animal_name):
    """Returns individual animal in JSON format"""
    animal = session.query(CategoryItem).filter_by(
        name=animal_name, category_name=animal_type).one_or_none()
    return jsonify(animal.serialize)


# Util functions
def create_user(login_session):
    """Create user and return user id from login session"""
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture']
    )
    session.add(new_user)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one_or_none()
    return user.id


def get_user_info(user_id):
    """Returns user by user id"""
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def get_user_id(email):
    """Returns user id by email"""
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except Exception:
        return None


if __name__ == '__main__':
    app.secret_key = os.environ['SECRET_KEY']
    app.run(host='0.0.0.0', port=8000, debug=True)
