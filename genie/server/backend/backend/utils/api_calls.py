import os
import requests
import json
from solders.keypair import Keypair
from backend.utils import errors, cryptography

SERVERLESS_ENDPOINT = os.environ.get("SERVERLESS_ENDPOINT")

def create_social_account_call():
    keypair = Keypair()
    endpoint = SERVERLESS_ENDPOINT + 'api/profile/initialize'
    pub_key = str(keypair.pubkey())
    sec_key_bytes = str(Keypair.from_bytes(bytes(keypair)).to_bytes_array())
    password = bytes(os.environ.get("SECRET_PASSWORD"), 'utf-8')
    encrypted_sec_key = cryptography.encrypt_message(sec_key_bytes, password)
    response = requests.post(endpoint, json={"initialAuth": sec_key_bytes})
    data = json.loads(response.text)

    if not data['success']:
        raise errors.CreateSocialAccountFailure()

    return data, pub_key, encrypted_sec_key, data['key']

def create_inbox_account_call(platform, primary_key):
    keypair = Keypair()
    endpoint = SERVERLESS_ENDPOINT + 'api/inbox/initialize'
    pub_key = str(keypair.pubkey())
    sec_key_bytes = str(Keypair.from_bytes(bytes(keypair)).to_bytes_array())
    password = bytes(os.environ.get("SECRET_PASSWORD"), 'utf-8')
    encrypted_sec_key = cryptography.encrypt_message(sec_key_bytes, password)
    response = requests.post(endpoint, json={"initialAuth": sec_key_bytes, "platform": platform, "primaryKey": primary_key})
    data = json.loads(response.text)

    if not data['success']:
        raise errors.CreateInboxAccountFailure()

    return data, pub_key, encrypted_sec_key, data['key']

def register_inbox_account_call(social_account_sec_key, inbox_account_sec_key):
    password = bytes(os.environ.get("SECRET_PASSWORD"), 'utf-8')
    endpoint = SERVERLESS_ENDPOINT + 'api/inbox/registerOwner'
    social_account_sec_key = str(cryptography.decrypt_message(bytes(social_account_sec_key), password))
    inbox_account_sec_key = str(cryptography.decrypt_message(inbox_account_sec_key, password))
    response = requests.post(endpoint, json={"initialAuthProfile": social_account_sec_key, "initialAuthInbox": inbox_account_sec_key})
    data = json.loads(response.text)

    if not data['success']:
        raise errors.RegisterInboxAccountFailure

    return

def get_inbox_token_call(inbox_account_sec_key, platform, primary_key):
    password = bytes(os.environ.get("SECRET_PASSWORD"), 'utf-8')
    endpoint = SERVERLESS_ENDPOINT + 'api/inbox/getTokens'
    inbox_account_sec_key = str(cryptography.decrypt_message(inbox_account_sec_key, password))
    response = requests.post(endpoint, json={"initialAuth": inbox_account_sec_key, "platform": platform, "primaryKey": primary_key})
    data = json.loads(response.text)

    if not data['success']:
        raise errors.GetInboxTokenFailure

    token_list = data['list']

    return token_list

def get_inbox_nft_call(inbox_account_sec_key, platform, primary_key):
    password = bytes(os.environ.get("SECRET_PASSWORD"), 'utf-8')
    endpoint = SERVERLESS_ENDPOINT + 'api/inbox/getNfts'
    inbox_account_sec_key = str(cryptography.decrypt_message(inbox_account_sec_key, password))
    response = requests.post(endpoint, json={"initialAuth": inbox_account_sec_key, "platform": platform, "primaryKey": primary_key})
    data = json.loads(response.text)

    if not data['success']:
        raise errors.GetInboxTokenFailure

    nft_list = data['list']

    return nft_list


def send_token_call(social_account_sec_key, inbox_account_sec_key, receiver_address, mint_address, amount):
    password = bytes(os.environ.get("SECRET_PASSWORD"), 'utf-8')
    endpoint = SERVERLESS_ENDPOINT + 'api/inbox/sendToken'
    social_account_sec_key = str(cryptography.decrypt_message(social_account_sec_key, password))
    inbox_account_sec_key = str(cryptography.decrypt_message(inbox_account_sec_key, password))
    response = requests.post(
                    endpoint, 
                    json={
                        "initialAuthProfile": social_account_sec_key, 
                        "initialAuthInbox": inbox_account_sec_key, 
                        "receiver": receiver_address, 
                        "mint": mint_address,
                        "amount": amount
                    }
                )
    data = json.loads(response.text)

    if not data['success']:
        raise errors.SendTokenFailure

    return data['txId']
