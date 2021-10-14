#pylint: disable=bad-indentation
import requests
import os
from dotenv import find_dotenv, load_dotenv
import random

load_dotenv(find_dotenv())

# Step 1 - Authorization 
authUrl = "https://accounts.spotify.com/api/token"
headers = {}
data = {}

clientId = os.getenv("clientId")
clientSecret = os.getenv("clientSecret")

# POST
auth_response = requests.post(authUrl, {
    'grant_type': 'client_credentials',
    'client_id': clientId,
    'client_secret': clientSecret,   
})

# convert the response to JSON
auth_response_data = auth_response.json()
# save the access token
access_token = auth_response_data['access_token']
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


artists = []
def get_track_info(artist_id):
    params = {
       
        'q': artist_id,
        'api-key': access_token,
    }

    # id_arijit='4YRxDV8wJFPHPTeXepOstw'
    # id_diljit='2FKWNmZWDBZR4dE5KX4plR'
    # id_billie='6qqNVTkY8uBg9cP3Jd7DAH'
    # id_bpraak='56SjZARoEvag3RoKWIb16j'
    # id_dua='6M2wZ9GZgrQXHCFfjv46we'

    # ids = [id_arijit, id_diljit, id_billie, id_bpraak, id_dua]
    # id_1 = ids[random.randint(0,4)]
    # print(id_1)

    BASE_URL = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"

    response = requests.get(BASE_URL, params=params, headers=headers)
    response_json = response.json()


     #print(json.dumps(response_json))

        #print (json.dumps(response_json, indent=4))
    try:
        track = response_json['tracks']  
        artists = []
        name = []
        preview_url = []
        image =[]
       
        for i in track:
                
                artists.append(i['album']['artists'][0]['name'])   
                name.append(i['name'])
                preview_url.append(i['preview_url'])
                image.append(i['album']['images'][0]['url'])
    except KeyError:
        print("could not find")   

    return{       
                  
                "artists":artists,
                "name":name,
                "preview_url":preview_url,
                "image":image,
              
               
               
            }

# get_track_info(artist_id)
# print(artists)

