# pylint: disable=inconsistent-return-statements
#search for song
import requests
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_lyric(artists):
    client_access_token = os.getenv("genius_access_token")
    base_url = 'https://api.genius.com'

    path = 'search/'
    request_uri = '/'.join([base_url, path])
    token = 'Bearer {}'.format(client_access_token)
    headers = {'Authorization': token}

    params = {'q': artists,
              'access-token':token,
               }

    response = requests.get(request_uri, params=params, headers=headers)
    response_json = response.json()
    #print (json.dumps(response_json, indent=4))
    
    try:
     return response_json['response']['hits'][0]['result']['url']
    except KeyError:
     print("could not find lyrics")  
##




    
   
 

    
   
 