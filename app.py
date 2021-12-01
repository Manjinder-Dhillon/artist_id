import flask
import os
from flask_sqlalchemy import SQLAlchemy
from spotify import get_track_info
from genius import get_lyric
from dotenv import find_dotenv, load_dotenv
from datetime import timedelta
from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_login import login_user, current_user, logout_user, login_required
import flask
from flask_login import login_user, current_user, LoginManager
from flask_login.utils import login_required
from flask import Flask, flash, redirect, render_template, \
     request, url_for
from datetime import timedelta
from authlib.integrations.flask_client import OAuth
from flask_login import UserMixin


load_dotenv(find_dotenv())

app = flask.Flask(__name__)

global client_id
global client_secret

client_Id = os.getenv("client_Id")
client_Secret = os.getenv("client_Secret")
# secret key
secret_key = os.getenv("secret_key")
app.config["SECRET_KEY"] = secret_key

# database url
url = os.getenv("DATABASE_URL")
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = url

# secret key
secret_key = os.getenv("secret_key")
app.config["SECRET_KEY"] = secret_key

app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)




# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=client_Id,
    client_secret=client_Secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


db = SQLAlchemy(app)

# define some Models!
class Todo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))


class Todo_artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(120))

class Todo_A(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String(120))    


db.create_all()

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_name):
    return Todo.query.get(user_name)
# signup page
@app.route('/sign')
def sign():
    return render_template('signup.html')

@app.route('/sign', methods=['POST'])
def sign_post():
    username = flask.request.form.get('username')
   

    user = Todo.query.filter_by(username=username).first()

    if user:
        flash('Username  already exists.')
        return redirect(url_for('login'))

    new_user = Todo( username=username)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('login'))

# login page
@app.route('/login')
def googleLogin():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)
      


@app.route("/")
def login():
    return flask.render_template("login.html")


@app.route("/login_flask", methods=["POST"])
def login_post():
    
    username = flask.request.form.get("username")
    user = Todo.query.filter_by(username=username).first()
    if user:
        login_user(user)
        return flask.redirect("/artist")

    else:
        flash(u'Invalid login provided. Click on Signup now to create', 'error')
        return redirect(url_for('login'))

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/artist')
# artist page
@app.route("/artist", methods=["GET", "POST"])  # Python decorator
def get_artist_id():
    todos_id = Todo_artist.query.all()
    artist_ids = []
    for todo_id in todos_id:
        artist_ids.append(todo_id.artist_id)
    if flask.request.method == "POST":
        artist_id = flask.request.form.get("artist_id")
        todo_id = Todo_artist(artist_id=artist_id)
        db.session.add(todo_id)
        db.session.commit()
        artist_ids.append(artist_id)
    return flask.render_template(
        "artist.html",
        artist_ids=artist_ids,
    )


# index page and saving to database
@app.route("/index", methods=["GET", "POST"])  # Python decorator
def index():
    save_artist = Todo_artist.query.all()
    artist_id = []

    for i in save_artist:
        artist_id.append(i.artist_id)
    if flask.request.method == "POST":
        artist_id = flask.request.form.get("artist_id")
        for i in artist_id:
            if artist_id == i:
                flask.flash("ID saved in database")
                return flask.redirect("/index")
    i = Todo_artist(artist_id=artist_id)
    db.session.add(i)
    db.session.commit()

    data = get_track_info(artist_id)
    lyrics_url = get_lyric(data["artists"])

    return flask.render_template(
        "index.html",
        artists=data["artists"],
        name=data["name"],
        preview_url=data["preview_url"],
        image=data["image"],
        lyrics_url=lyrics_url,
    )


app.run(
    # debug=True
    host='0.0.0.0',
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", "8080")),
)
