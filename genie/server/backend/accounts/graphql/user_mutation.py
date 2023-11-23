import graphene
from accounts.models import SocialAccount, Inbox
from sns.models import SNS, SNSConnectionInfo
from blockchain.models import Network, Coin, NFT
from backend.utils.api_calls import create_social_account_call, create_inbox_account_call, register_inbox_account_call, get_inbox_token_call, get_inbox_nft_call
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
    token_list = graphene.List(graphene.String)
    value_list = graphene.List(graphene.Float)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        inbox_accounts = Inbox.objects.filter(account=account)
        network = Network.get_by_name(network_name)
        token_dict = {}

        for inbox_account in inbox_accounts:
            token_list = get_inbox_token_call(inbox_account.secret_key, sns_name.lower(), discriminator)
            for token in token_list:
                ticker = Coin.get_by_mint(network, token['mint'])

                if ticker not in token_dict.keys():
                    token_dict[ticker] = float(token['amount']) / (10 ** float(token['decimals']))
                else:
                    token_dict[ticker] += float(token['amount']) / (10 ** float(token['decimals']))

        return GetUserTokens(
                success=True, 
                token_list=token_dict.keys(), 
                value_list=token_dict.values(),
                )


class GetUserNFTs(graphene.Mutation):
    success = graphene.NonNull(graphene.Boolean)
    nft_list = graphene.List(graphene.String)
    nft_value_list = graphene.List(graphene.Int)

    class Arguments:
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        network_name = graphene.String(required=True)

    def mutate(self, info, sns_name, discriminator, network_name):
        sns = SNS.get_by_name(sns_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)
        inbox_accounts = Inbox.objects.filter(account=account)
        network = Network.get_by_name(network_name)
        nft_dict = {}

        for inbox_account in inbox_accounts:
            nft_list = get_inbox_nft_call(inbox_account.secret_key, sns_name.lower(), discriminator)
            for nft in nft_list:
                NFT.register_nft(network=network, name=nft['name'], mint_address=nft['mint'])
                
                if nft['name'] not in nft_dict.keys():
                    nft_dict[nft['name']] = 1
                else:
                    nft_dict[nft['name']] += 1


        return GetUserNFTs(
                success=True, 
                nft_list=nft_dict.keys(),
                nft_value_list=nft_dict.values(),
                )


class AccountMutation(graphene.ObjectType):
    create_social_account = CreateSocialAccount.Field()
    create_inbox_account = CreateInboxAccount.Field()
    get_user_tokens = GetUserTokens.Field()
    get_user_nfts = GetUserNFTs.Field()
