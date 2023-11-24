import requests
import graphene
from sns.models import SNS, SNSConnectionInfo, Server
from blockchain.models import Network
from accounts.models import SocialAccount
from backend.utils import errors


class RegisterSNS(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        network_name = graphene.String(required=True)
        pub_key = graphene.String(required=True)
        sns_name = graphene.String(required=True)
        discriminator = graphene.String(required=True)
        handle = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        network_name: str,
        pub_key: str,
        sns_name: str,
        discriminator: str,
        handle: str,
    ) -> graphene.Mutation:
        _network_name: str = network_name.strip()
        _pub_key: str = pub_key.strip()
        _sns_name: str = sns_name.strip()
        _discriminator: str = discriminator.strip()
        _handle: str = handle.strip()
            
        network: "Network" = Network.get_by_name(_network_name)
        sns: "SNS" = SNS.get_by_name(_sns_name)
        account: "SocialAccount" = SocialAccount.get_by_pub_key(_pub_key)

        try:
            SNSConnectionInfo.objects.create(
                account=account, sns=sns, discriminator=_discriminator, handle=_handle
            )
        except Exception:
            raise errors.RegisterSNSFailure from Exception

        return RegisterSNS(success=True)


class RegisterServer(graphene.Mutation):
    success: bool = graphene.NonNull(graphene.Boolean)

    class Arguments:
        sns_name = graphene.String(required=True)
        server_id = graphene.String(required=True)
        name = graphene.String(required=True)

    def mutate(
        self,
        info: graphene.ResolveInfo,
        sns_name: str,
        server_id: str,
        name: str,
    ) -> graphene.Mutation:
        sns: "SNS" = SNS.get_by_name(sns_name)

        try:
            Server.objects.create(
            sns=sns, server_id=server_id, name=name
        )
        except Exception:
            raise errors.RegisterServerFailure

        return RegisterServer(success=True)


class SNSMutation(graphene.ObjectType):
    register_sns = RegisterSNS.Field()
