import flask
import os
from flask_sqlalchemy import SQLAlchemy
from spotify import get_track_info
from genius import get_lyric
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = flask.Flask(__name__)

#database url
url = os.getenv("DATABASE_URL")
if url and url.startswith("postgres://"):
    url = url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = url

#secret key
secret_key = os.getenv("secret_key")
app.config['SECRET_KEY'] = secret_key  


db = SQLAlchemy(app)

# define some Models!
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
class Todo_artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.String(120))
db.create_all()

#signup page
@app.route('/', methods=["GET", "POST"])
@app.route('/signup', methods=["GET", "POST"])
def signup(): 
    todos = Todo.query.all()
    username = []
    for todo in todos:
        username.append(todo.username)   
    if flask.request.method == "POST":
        username_check = flask.request.form.get('username')      
        #checking existing user or not
        for i in username:       
            if username_check == i:
                flask.flash("id exists. login")
                return flask.redirect("/login")
        todo = Todo(username=username_check)    
        db.session.add(todo)
        db.session.commit()
       
    return flask.render_template(
        "signup.html",     
        username=username,
      
    )


#login page
@app.route('/login', methods=["GET", "POST"])
def login():
    todos = Todo.query.all()
    username = []
    for todo in todos:
        username.append(todo.username)   
    if flask.request.method == "POST":
        username_check = flask.request.form.get('username')      
        #checking existing user or not
        for i in username:  
            if username_check == i:
                flask.flash("id  exists.  artist")
                return flask.redirect("/artist")     
            if username_check != i:
                flask.flash("id doesnot exists. SIGN UP!")
                return flask.redirect("/signup")


        todo = Todo(username=username_check)    
        db.session.add(todo)
        db.session.commit()
       
    return flask.render_template(
        "login.html",     
        username=username,
     )

#artist page
@app.route("/artist",methods=["GET", "POST"])  # Python decorator
def get_artist_id():  
    todos_id = Todo_artist.query.all()
    artist_ids = []
    for todo_id in todos_id:
        artist_ids.append(todo_id.artist_id)    
    if flask.request.method == "POST":
        artist_id = flask.request.form.get('artist_id')      
        todo_id = Todo_artist(artist_id=artist_id)
        db.session.add(todo_id)
        db.session.commit()
        artist_ids.append(artist_id)
    return flask.render_template(
        "artist.html",
        artist_ids=artist_ids,
      
    )

#index page and saving to database
@app.route("/index",methods=["GET", "POST"])  # Python decorator
def index(): 
    save_artist = Todo_artist.query.all()
    artist_id = []

    for i in save_artist:
        artist_id.append(i.artist_id)
    if flask.request.method == "POST":   
     artist_id = flask.request.form.get("artist_id")
     for i in artist_id:
         if artist_id ==i:
            flask.flash("ID saved in database")
            return flask.redirect("/index")
    i = Todo_artist(artist_id=artist_id)    
    db.session.add(i)
    db.session.commit()      

    data = get_track_info(artist_id)
    lyrics_url = get_lyric(data['artists'])
   
    return flask.render_template(  
            "index.html",     
            artists = data["artists"],
            name = data["name"],
            preview_url = data["preview_url"],
            image=data["image"],
           
            lyrics_url =lyrics_url,       
            )

           

app.run(debug=True)