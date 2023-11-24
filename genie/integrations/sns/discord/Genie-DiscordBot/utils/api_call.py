import os
import json
import requests
from utils.constants import BACKEND_ENDPOINT

def check_user_account(discriminator):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        query {open_bracket}
            checkUserAccount (
                snsName: "Discord"
                discriminator: {discriminator}
                networkName: "Solana"
            ) {open_bracket}
                socialAcccount
                inbox
            {close_bracket}
        {close_bracket}
        """
    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        social_account = data['data']['checkUserAccount']['socialAcccount']
        inbox = data['data']['checkUserAccount']['inbox']
    except:
        return None

    return social_account, inbox

def create_social_account(nickname):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            createSocialAccount (
                nickname: "{nickname}"
            ) {open_bracket}
                success
                pubKey
            {close_bracket}
        {close_bracket}
        """
    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        data = data['data']['createSocialAccount']['pubKey']
    except:
        return None

    return data

def create_inbox_account(discord_id, network_name):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            createInboxAccount (
                discriminator: "{discord_id}"
                snsName: "Discord"
                networkName: "{network_name}"
            ) {open_bracket}
                success
                walletAddress
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        data = data['data']['createInboxAccount']['walletAddress']
    except:
        return None

    return data

def check_user_account(discriminator):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        query {open_bracket}
            checkUserAccount (
                snsName: "Discord"
                discriminator: "{discriminator}"
                networkName: "Solana"
            ) {open_bracket}
                socialAccountPubKey
                inbox
            {close_bracket}
        {close_bracket}
        """
    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        social_account_pub_key = data['data']['checkUserAccount']['socialAccountPubKey']
        inbox = data['data']['checkUserAccount']['inbox']
    except:
        return None

    return social_account_pub_key, inbox

def create_social_account(nickname):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            createSocialAccount (
                nickname: "{nickname}"
            ) {open_bracket}
                success
                pubKey
            {close_bracket}
        {close_bracket}
        """
    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
     
    try:
        data = data['data']['createSocialAccount']['pubKey']
    except:
        return None

    return data

def create_inbox_account(discord_id, network_name):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            createInboxAccount (
                discriminator: "{discord_id}"
                snsName: "Discord"
                networkName: "{network_name}"
            ) {open_bracket}
                success
                walletAddress
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)

    try:
        data = data['data']['createInboxAccount']['walletAddress']
    except:
        return None

    return data

def get_user_inbox_account(discord_id):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        query {open_bracket}
            getUserInboxWallet (
                discriminator: "{discord_id}"
                snsName: "Discord"
                networkName: "Solana"
            ) {open_bracket}
                walletAddress
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        data = data['data']['getUserInboxWallet']['walletAddress']
    except:
        return None

    return data

def register_sns(network_name, pub_key, discord_id, nickname):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            registerSns (
                discriminator: "{discord_id}"
                pubKey: "{pub_key}"
                snsName: "Discord"
                networkName: "{network_name}"
                handle: "{nickname}"
            ) {open_bracket}
                success
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)

    try:
        data = data['data']['registerSns']['success']
    except:
        return None

    return
>>>>>>> c7925a8 (Add: api calls for register command)
