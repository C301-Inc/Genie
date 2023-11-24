import graphene

from accounts.graphql.user_query import AccountQuery
from accounts.graphql.user_mutation import AccountMutation
from sns.graphql.sns_mutation import SNSMutation


class Query(
    AccountQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    AccountMutation,
    SNSMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
        )
