from graphene_django.views import GraphQLView as BaseGraphQLView


class GraphQLView(BaseGraphQLView):
    @staticmethod
    def format_error(error):
        formatted_error = super(GraphQLView, GraphQLView).format_error(error)

        try:
            formatted_error["context"] = error.original_error.context
        except AttributeError:
            pass

        return formatted_error


class GenieGraphQLException(Exception):
    message = None
    error_msg = None

    def __init__(
        self,
    ):
        self.context = {}

        if self.error_msg:
            self.context["error_msg"] = self.error_msg

        super().__init__(self.message)
