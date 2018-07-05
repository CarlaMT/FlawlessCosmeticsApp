from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
app.secret_key = 'some secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = False


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///makeupcatalog.db', echo=True)


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

db = SQLAlchemy(app)

# ==========================
# Login & Anti-forgery state token
# ==========================

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)

# ========================
# User Helper Functions
# ========================

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(
        email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# ========================
# GConnect
# ========================


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps(
            'Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(
            'client_secrets.json', scope='')
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
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;\
    border-radius: 150px;-webkit-border-radius: 150px;\
    -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
    session.close()

# ========================
# GDisConnect
# ========================

@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s'\
        % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps(
            'Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# ===================
# Flask Routing
# ===================

@app.route('/')
def index():
    return render_template('index.html')

# Show all categories
@app.route('/categories/')
def showCategories():
    """Shows all categories"""
    if 'username' not in login_session:
        return redirect('/login')
    flash("you are now logged in as %s" % login_session['username'])
    session.close()
    category = session.query(Category).all()
    return render_template('categories.html', category=category)



# Show catalog item for specific category
@app.route('/categoryitems/<int:category_id>/')
def showCategoryItems(category_id):
    """Show all catalog items for a specific category"""
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).all()
    items = session.query(CategoryItem).filter_by(
        category_id=category_id).all()
    return render_template('showCategoryItems.html',
                           category=category,
                           items=items,
                           category_id=category_id)


# Show catalog item for specific item
@app.route('/categoryitem/<int:category_id>/')
@app.route('/categoryitem/<int:category_id>/item')
def showCategoryItem(category_id):
    """Show all catalog items for a specific item"""
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).all()
    title = session.query(Category).filter_by(id=category_id).all()
    oneItem = session.query(CategoryItem).filter_by(
        id=category_id).first()
    return render_template('showCategoryItem.html',
                           category=category,
                           oneItem=oneItem,
                           category_id=category_id,
                           title=title)

# Edit a catalog item
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategoryItem(category_id):
    """Edit an existing category"""
    if 'username' not in login_session:
        return redirect('/login')
    editedCategory = session.query(
        CategoryItem).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
        if request.form['description']:
            editedCategory.description = request.form['description']
        if request.form['price']:
            editedCategory.price = request.form['price']
        session.add(editedCategory)
        session.commit()
        flash('Category Item Successfully Edited!')
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('editCategoryItem.html',
                               category=editedCategory,
                               category_id=category_id)


# New catalog item
@app.route('/categoryitem/<int:category_id>/items/new/',
           methods=['GET', 'POST'])
def addCategoryItem(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    """Create a new catalog item for a specific category"""
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newCategoryItem = CategoryItem(name=request.form['name'],
                                       description=request.form['description'],
                                       price=request.form['price'],
                                       category=category)
        session.add(newCategoryItem)
        flash('New Category Item %s Successfully Created' %
              (newCategoryItem.name))
        session.commit()
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('addCategoryItem.html',
                               category_id=category_id)


@app.route('/categories/<int:category_id>/items/delete/',
           methods=['GET', 'POST'])
def deleteCategoryItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    itemToDelete = session.query(
        CategoryItem).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('Category Item %s Successfully Deleted!' %
              (itemToDelete.name))
        session.commit()
        return redirect(url_for('showCategoryItems', category_id=category_id))
    else:
        return render_template('deletecategoryitem.html',
                               items=itemToDelete,
                               category_id=category_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000, threaded = False)