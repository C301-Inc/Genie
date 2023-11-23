import graphene

from accounts.graphql.user_query import AccountQuery
from accounts.graphql.user_mutation import AccountMutation


class Query(
    AccountQuery,
    graphene.ObjectType
):
    pass


class Mutation(
    AccountMutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
        )
