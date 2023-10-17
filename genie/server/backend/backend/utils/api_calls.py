import os
import requests
import json
from solders.keypair import Keypair
from backend.utils import errors

SERVERLESS_ENDPOINT = os.environ.get("SERVERLESS_ENDPOINT")

def create_social_account_call():
    keypair = Keypair()
    #endpoint = SERVERLESS_ENDPOINT + 'profile'
    sec_key = str(Keypair.from_bytes(bytes(keypair)).to_bytes_array()) 
    #response = requests.post(endpoint, json={"sec_key": sec_key})
    #data = json.loads(response.text)
    
    if not data['success']:
        raise errors.CreateSocialAccountFailure()

    return data, sec_key

def create_inbox_account_call(platform, primary_key):
    keypair = Keypair()
    #endpoint = SERVERLESS_ENDPOINT + 'inbox'
    sec_key = str(Keypair.from_bytes(bytes(keypair)).to_bytes_array()) 
    #response = requests.post(endpoint, json={"sec_key": sec_key, "platform": platform, "primary_key": primary_key})
    #data = json.loads(response.text)

    if not data['success']:
        raise errors.CreateInboxAccountFailure()

    return data, sec_key
