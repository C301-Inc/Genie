import graphene

from accounts.graphql.user_query import AccountQuery


class Query(
    AccountQuery,
    graphene.ObjectType
):
    pass


#class Mutation(
#    graphene.ObjectType
#):
#    pass


schema = graphene.Schema(
    query=Query,
#    mutation=Mutation,
        )
