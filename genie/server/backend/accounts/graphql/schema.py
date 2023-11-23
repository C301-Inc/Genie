import graphene
from accounts.models import SocialAccount, Inbox
from blockchain.models import Network, Coin, Collection, NFT, CoinTransactionHistory, NFTTransactionHistory
from graphene_django.types import DjangoObjectType


class CheckUserAccountType(graphene.ObjectType):
    social_account = graphene.NonNull(graphene.Boolean)
    inbox = graphene.NonNull(graphene.Boolean)


class InboxType(DjangoObjectType):
    class Meta:
        model = Inbox
        fields = ("wallet_address", "network")


class CoinType(DjangoObjectType):
    class Meta:
        model = Coin
        fields = ("network", "ticker", "mint_address")


class CollectionType(DjangoObjectType):
    class Meta:
        model = Collection
        fields = ("network", "name", "mint_address")


class NFTType(DjangoObjectType):
    class Meta:
        model = NFT
        fields = ("network", "name", "mint_address", "collection")


class CoinTransactionHistoryType(graphene.ObjectType):
    coin = graphene.NonNull(CoinType)
    is_sent = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)
    amount = graphene.NonNull(graphene.String)
    target_sns_nickname = graphene.NonNull(graphene.String)
    target_social_nickname = graphene.NonNull(graphene.String)
    created_at = graphene.NonNull(graphene.String)


class NFTTransactionHistoryType(graphene.ObjectType):
    NFT = graphene.NonNull(NFTType)
    is_sent = graphene.NonNull(graphene.Boolean)
    tx_hash = graphene.NonNull(graphene.String)
    target_sns_nickname = graphene.NonNull(graphene.String)
    target_social_nickname = graphene.NonNull(graphene.String)
    created_at = graphene.NonNull(graphene.String)


class GetUserCoinTxHistoryReturnType(graphene.ObjectType):
    coin_tx_list = graphene.List(graphene.NonNull(CoinTransactionHistoryType))


class GetUserNFTTxHistoryReturnType(graphene.ObjectType):
    nft_tx_list = graphene.List(graphene.NonNull(NFTTransactionHistoryType))
