import os
import json
import requests
from utils.constants import BACKEND_ENDPOINT


def get_track_counts(discord_id):
    open_bracket = "{"
    close_bracket = "}"
    body = f"""
        query {open_bracket}
            getTrackCounts (
                discriminator: "{discord_id}"
            ) {open_bracket}
                track {open_bracket}
                    title    
                {close_bracket}
                streamingCount
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})

    data = json.loads(response.text)

    if "errors" in data:
        return []

    return data["data"]["getTrackCounts"]

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


def get_user_tokens(discord_id, network_name):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            getUserTokens (
                discriminator: "{discord_id}"
                networkName: "{network_name}"
                snsName: "Discord"
            ) {open_bracket}
                success
                tokenValueList
                tokenTickerList
                tokenAddressList
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        token_value_list = data['data']['getUserTokens']['tokenValueList']
        token_ticker_list = data['data']['getUserTokens']['tokenTickerList']
        token_address_list = data['data']['getUserTokens']['tokenAddressList']
    except:
        return None

    return token_value_list, token_ticker_list, token_address_list

def get_user_nfts(discord_id, network_name):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            getUserNfts (
                discriminator: "{discord_id}"
                networkName: "{network_name}"
                snsName: "Discord"
            ) {open_bracket}
                success
                nftNameList
                nftAddressList
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        nft_name_list = data['data']['getUserNfts']['nftNameList']
        nft_address_list = data['data']['getUserNfts']['nftAddressList']
    except:
        return None

    return nft_name_list, nft_address_list

def send_token(discord_id, network_name, mint_address, amount, to_address, server_id):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            sendToken (
                discriminator: "{discord_id}"
                networkName: "{network_name}"
                mintAddress: "{mint_address}"
                receiver: "{to_address}"
                snsName: "Discord"
                amount: {amount}
                serverId: "{server_id}"
            ) {open_bracket}
                success
                txHash
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        tx_hash = data['data']['sendToken']['txHash']
    except:
        return None

    return tx_hash

def send_nft(discord_id, network_name, mint_address, to_address, server_id):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            sendNft (
                discriminator: "{discord_id}"
                networkName: "{network_name}"
                mintAddress: "{mint_address}"
                receiver: "{to_address}"
                snsName: "Discord"
                serverId: "{server_id}"
            ) {open_bracket}
                success
                txHash
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        tx_hash = data['data']['sendNft']['txHash']
    except:
        return None

    return tx_hash

def get_user_coin_tx_history(discord_id):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        query {open_bracket}
            getUserCoinTxHistory (
                discriminator: "{discord_id}"
                snsName: "Discord"
            ) {open_bracket}
                coinTxList {open_bracket}
                    isSent
                    coin {open_bracket}
                        ticker
                    {close_bracket}
                    amount
                    txHash
                    targetSnsDiscriminator
                {close_bracket}
            {close_bracket}
        {close_bracket}
        """
  
    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        coin_tx = data['data']['getUserCoinTxHistory']['coinTxList']
    except:
        return None

    return coin_tx

def get_user_nft_tx_history(discord_id):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        query {open_bracket}
            getUserNftTxHistory (
                discriminator: "{discord_id}"
                snsName: "Discord"
            ) {open_bracket}
                nftTxList {open_bracket}
                    isSent
                    NFT {open_bracket}
                        name
                        mintAddress
                    {close_bracket}
                    txHash
                    targetSnsDiscriminator
                {close_bracket}
            {close_bracket}
        {close_bracket}
        """
    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        nft_tx = data['data']['getUserNftTxHistory']['nftTxList']
    except:
        return None

    return nft_tx

def withdraw_token(discord_id, network_name, mint_address, amount, to_address):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            withdrawToken (
                discriminator: "{discord_id}"
                networkName: "{network_name}"
                mintAddress: "{mint_address}"
                receiver: "{to_address}"
                snsName: "Discord"
                amount: {amount}
            ) {open_bracket}
                success
                txHash
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        tx_hash = data['data']['withdrawToken']['txHash']
    except:
        return None

    return tx_hash

def withdraw_nft(discord_id, network_name, mint_address, to_address):
    open_bracket = '{'
    close_bracket = '}'
    body = f"""
        mutation {open_bracket}
            withdrawNft (
                discriminator: "{discord_id}"
                networkName: "{network_name}"
                mintAddress: "{mint_address}"
                receiver: "{to_address}"
                snsName: "Discord"
            ) {open_bracket}
                success
                txHash
            {close_bracket}
        {close_bracket}
        """

    response = requests.post(url=os.environ['BACKEND_ENDPOINT'], json={"query": body})
    data = json.loads(response.text)
    
    try:
        tx_hash = data['data']['withdrawNft']['txHash']
    except:
        return None

    return tx_hash


