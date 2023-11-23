from typing import Optional
import graphene
from django.conf import settings
from django.db.models import QuerySet, Prefetch
from accounts.models import Inbox
from accounts.graphql.schema import InboxType, GetUserCoinTxHistoryReturnType, GetUserNFTTxHistoryReturnType, CoinTransactionHistoryType, NFTTransactionHistoryType, CheckUserAccountType
from blockchain.models import Network, CoinTransactionHistory, NFTTransactionHistory
from sns.models import SNS, SNSConnectionInfo
from backend.utils import errors


class AccountQuery(graphene.ObjectType):
    check_user_account = graphene.NonNull(
        CheckUserAccountType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
        network_name=graphene.String(required=True),
    )

    get_user_inbox_wallet = graphene.NonNull(
        InboxType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
        network_name=graphene.String(required=True),
    )

    get_user_coin_tx_history = graphene.NonNull(
        GetUserCoinTxHistoryReturnType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
    )

    get_user_nft_tx_history = graphene.NonNull(
        GetUserNFTTxHistoryReturnType,
        sns_name=graphene.String(required=True),
        discriminator=graphene.String(required=True),
    )

    def resolve_check_user_account(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")
        network_name = kwargs.get("network_name")

        sns = SNS.get_by_name(sns_name)

        if not SNSConnectionInfo.check_account(sns, discriminator):
            return CheckUserAccountType(social_account=False, inbox=False)
        
        network = Network.get_by_name(network_name)
        account = SNSConnectionInfo.get_account(sns, discriminator)

        if not Inbox.check_inbox(sns, account, network):
            return CheckUserAccountType(social_account=True, inbox=False)

        return CheckUserAccountType(social_account=True, inbox=True) 

    def resolve_get_user_inbox_wallet(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")
        network_name = kwargs.get("network_name")

        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)
        network = Network.get_by_name(network_name)
        
        inbox = Inbox.get_inbox(sns, social_account, network)

        return inbox

    def resolve_get_user_coin_tx_history(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")
        
        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)
        inbox_list = Inbox.objects.filter(account=social_account).prefetch_related('from_coin_tx', 'to_coin_tx')
        coin_tx_list = []

        for inbox in inbox_list:
            txs = inbox.from_coin_tx.all() | inbox.to_coin_tx.all()
            
            for tx in txs:
                is_sent = tx.from_inbox == inbox
                target_inbox = tx.to_inbox if is_sent else tx.from_inbox
                target_account = target_inbox.account
                target_sns_info = SNSConnectionInfo.get_by_sns_account(sns=target_inbox.sns, account=target_account)
                target_sns_nickname = target_sns_info.handle

                coin_tx_list.append(
                    CoinTransactionHistoryType(
                        coin=tx.coin,
                        is_sent=is_sent,
                        tx_hash=tx.tx_hash,
                        amount=tx.amount,
                        target_sns_nickname=target_sns_nickname,
                        target_social_nickname=target_account.nickname,
                        created_at=str(tx.created_at),
                    )
                )

        return GetUserCoinTxHistoryReturnType(coin_tx_list=coin_tx_list)

    def resolve_get_user_nft_tx_history(
        self, info: graphene.ResolveInfo, **kwargs
    ):
        sns_name = kwargs.get("sns_name")
        discriminator = kwargs.get("discriminator")
        
        sns = SNS.get_by_name(sns_name)
        social_account = SNSConnectionInfo.get_account(sns, discriminator)
        inbox_list = Inbox.objects.filter(account=social_account).prefetch_related('from_nft_tx', 'to_nft_tx')
        nft_tx_list = []

        for inbox in inbox_list:
            txs = inbox.from_nft_tx.all() | inbox.to_nft_tx.all()

            for tx in txs:
                is_sent = tx.from_inbox == inbox
                target_inbox = tx.to_inbox if is_sent else tx.from_inbox
                target_account = target_inbox.account

                target_sns_info = SNSConnectionInfo.get_by_sns_account(sns=target_inbox.sns, account=target_account)
                target_sns_nickname = target_sns_info.handle

                nft_tx_list.append(
                    NFTTransactionHistoryType(
                        NFT=tx.nft,
                        is_sent=is_sent,
                        tx_hash=tx.tx_hash,
                        target_sns_nickname=target_sns_nickname,
                        target_social_nickname=target_account.nickname,
                        created_at=str(tx.created_at),
                    )
                )

        return GetUserNFTTxHistoryReturnType(nft_tx_list=nft_tx_list)
