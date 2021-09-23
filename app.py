import flask
import os
from spotify import get_track_info
from genius import get_lyric

app = flask.Flask(__name__)

@app.route("/")  # Python decorator
def index():   
    data = get_track_info()
    lyrics_url = get_lyric(data['artists'])
   
    return flask.render_template(
            
            "index.html",     
            artists = data["artists"],
            name = data["name"],
            preview_url = data["preview_url"],
            image=data["image"],
           
            lyrics_url =lyrics_url,
            
            )

         

app.run(
    #host='0.0.0.0',
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", "8080"))
  
   
)