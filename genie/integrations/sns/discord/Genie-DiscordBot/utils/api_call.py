import os
import requests
import json


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

def get_user_inbox_account(discord_id):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        query {open_bracket}
            getUserInboxAccount (
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
        data = data['data']['getUserInboxAccount']['walletAddress']
    except:
        return None

    return data
