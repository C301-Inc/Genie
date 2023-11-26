import graphene
from accounts.models import SocialAccount, Inbox
from sns.models import SNS, SNSConnectionInfo, Server
from blockchain.models import Network, Coin, NFT, CoinTransactionHistory, NFTTransactionHistory
from backend.utils.api_calls import create_social_account_call, create_inbox_account_call, register_inbox_account_call, get_inbox_token_call, get_inbox_nft_call, send_token_call
from backend.utils import errors


class CreateSocialAccount(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    pub_key = graphene.NonNull(graphene.String)

    class Arguments:
        nickname = graphene.String(required=True)

    def mutate(self, info, nickname):
        nickname = nickname.strip()
        data, pub_key, sec_key, wallet_address = create_social_account_call()
        if not data['success']:
            return CreateSocialAccount(success=False)

        SocialAccount.objects.create(
            nickname=nickname,
            pub_key=pub_key,
            secret_key=sec_key,
            wallet_address=wallet_address,
        )

        return CreateSocialAccount(success=True, pub_key=pub_key)


class CreateInboxAccount(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    wallet_address = graphene.NonNull(graphene.String)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        data, pub_key, sec_key, wallet_address = create_inbox_account_call(sns_name.lower(), discriminator)
        if not data['success']:
            return CreateInboxAccount(success=False)

        register_inbox_account_call(account.secret_key, sec_key)

        Inbox.objects.create(
            pub_key=pub_key,
            secret_key=sec_key,
            wallet_address=wallet_address,
            account=account,
            network=network,
            sns=sns,
        )

        return CreateInboxAccount(success=True, wallet_address=wallet_address)


class GetUserTokens(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    token_ticker_list = graphene.List(graphene.String)
    token_address_list = graphene.List(graphene.String)
    token_value_list = graphene.List(graphene.Float)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        inbox_account = Inbox.get_inbox(sns=sns, account=account, network=network)
        token_ticker_list = []
        token_address_list = []
        token_value_list = []

        token_list = get_inbox_token_call(inbox_account.secret_key, sns_name.lower(), discriminator)
        for token in token_list:
            coin = Coin.get_or_create_by_mint(network, token['mint'], token['decimals'])
            token_ticker_list.append(coin.ticker)
            token_address_list.append(coin.mint_address)
            token_value_list.append(float(token['amount']) / (10 ** float(token['decimals'])))

        return GetUserTokens(
                success=True, 
                token_ticker_list=token_ticker_list, 
                token_address_list=token_address_list,
                token_value_list=token_value_list
        )


class GetUserNFTs(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    nft_name_list = graphene.List(graphene.String)
    nft_address_list = graphene.List(graphene.String)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        inbox_account = Inbox.get_inbox(sns=sns, account=account, network=network)
        nft_name_list = []
        nft_address_list = []

        nft_list = get_inbox_nft_call(inbox_account.secret_key, sns_name.lower(), discriminator)
        for nft in nft_list:
            NFT.register_nft(network=network, name=nft['name'], mint_address=nft['mint'])
            nft_name_list.append(nft['name'])
            nft_address_list.append(nft['mint'])

        return GetUserNFTs(
                success=True, 
                nft_name_list=nft_name_list,
                nft_address_list=nft_address_list,
        )


class SendToken(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        receiver = graphene.String(required=True)
        mint_address = graphene.String(required=True)
        amount = graphene.Float(required=True)
        server_id = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name, receiver, mint_address, amount, server_id):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        inbox = Inbox.get_inbox(sns=sns, account=account, network=network)
        coin = Coin.get_by_mint(network, mint_address)
        amount = amount * (10**coin.decimal)
        tx_hash = send_token_call(account.secret_key, inbox.secret_key, receiver, mint_address, amount)

        receiver_inbox = Inbox.get_by_address(receiver)
        
        if sns_name == "Discord":
            try:
                server = Server.get_by_server_id(server_id)
            except:
                server = None
        else:
            server = None
         
        CoinTransactionHistory.objects.create(
            from_inbox=inbox, to_inbox=receiver_inbox, tx_hash=tx_hash, server=server, coin=coin, amount=amount
        )

        return SendToken(success=True, tx_hash=tx_hash)


class SendNFT(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        receiver = graphene.String(required=True)
        mint_address = graphene.String(required=True)
        server_id = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name, receiver, mint_address, server_id):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        inbox = Inbox.get_inbox(sns=sns, account=account, network=network)
        tx_hash = send_token_call(account.secret_key, inbox.secret_key, receiver, mint_address, 1)

        nft = NFT.get_by_mint(network, mint_address)
        receiver_inbox = Inbox.get_by_address(receiver)

        if sns_name == "Discord":
            try:
                server = Server.get_by_server_id(server_id)
            except:
                server = None
        else:
            server = None

        NFTTransactionHistory.objects.create(
            from_inbox=inbox, to_inbox=receiver_inbox, tx_hash=tx_hash, server=server, nft=nft
        )

        return SendNFT(success=True, tx_hash=tx_hash)


class WithdrawToken(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        receiver = graphene.String(required=True)
        mint_address = graphene.String(required=True)
        amount = graphene.Float(required=True)

    def mutate(self, info, sns_name, discriminator, network_name, receiver, mint_address, amount):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        inbox = Inbox.get_inbox(sns=sns, account=account, network=network)
        coin = Coin.get_by_mint(network, mint_address)
        amount = amount * (10**coin.decimal)
        tx_hash = send_token_call(account.secret_key, inbox.secret_key, receiver, mint_address, amount)

        return WithdrawToken(success=True, tx_hash=tx_hash)


class WithdrawNFT(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)
        receiver = graphene.String(required=True)
        mint_address = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name, receiver, mint_address):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        inbox = Inbox.get_inbox(sns=sns, account=account, network=network)
        tx_hash = send_token_call(account.secret_key, inbox.secret_key, receiver, mint_address, 1)

        return WithdrawNFT(success=True, tx_hash=tx_hash)


class AccountMutation(graphene.ObjectType):
    create_social_account = CreateSocialAccount.Field()
    create_inbox_account = CreateInboxAccount.Field()
    send_token = SendToken.Field()
    send_nft = SendNFT.Field()
    get_user_tokens = GetUserTokens.Field()
    get_user_nfts = GetUserNFTs.Field()
    withdraw_token = WithdrawToken.Field()
    withdraw_nft = WithdrawNFT.Field()
