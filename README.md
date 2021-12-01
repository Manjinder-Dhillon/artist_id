# Flask app

## Requirements
1. `npm install`
2. `pip install -r requirements.txt`


<h5>Technologies</h5>
VSCode, Git, GitHub, and Heroku
<h5>Frameworks</h5>
Flask, dotenv ,sqlalchemy, SQLAlchemy
<h5>Libraries</h5>
Requests, os, random, json


1. Require .env file and requires the following  
   clientId=""
   clientSecret= ""
   genius_access_token = "" 

## Run Application
1. Run command in terminal (in your project directory): `python3 app.py`
2. Preview web page in browser 'localhost:8080/' (or whichever port you're using)

## Deploy to Heroku
1. Create a Heroku app: `heroku create --buildpack heroku/python`
2. Add nodejs buildpack: `heroku buildpacks:add --index 1 heroku/nodejs`
3. Push to Heroku: `git push heroku main`
