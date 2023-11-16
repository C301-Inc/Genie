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


class AccountNotFound(GenieGraphQLException):
    error_code = "A00001"
    message = "Does Not Exist!!!"
    error_msg = "Account does not exist. Please check again."


class SNSNotFound(GenieGraphQLException):
    error_code = "A00002"
    message = "Does Not Exist!!!"
    error_msg = "SNS does not exist. Please check again."


class NetworkNotFound(GenieGraphQLException):
    error_code = "A00003"
    message = "Does Not Exist!!!"
    error_msg = "Network does not exist. Please check again."


class SNSConnectionNotFound(GenieGraphQLException):
    error_code = "A00004"
    message = "Does Not Exist!!!"
    error_msg = "SNSConnectionInfo does not exist. Please check again."


class CreateSocialAccountFailure(GenieGraphQLException):
    error_code = "A00005"
    message = "Serverless Call Failure!!!"
    error_msg = "Failed to call CreateSocialAccount"


class CreateInboxAccountFailure(GenieGraphQLException):
    error_code = "A00006"
    message = "Serverless Call Failure!!!"
    error_msg = "Failed to call CreateInboxAccount"


class RegisterInboxAccountFailure(GenieGraphQLException):
    error_code = "A00007"
    message = "Serverless Call Failure!!!"
    error_msg = "Failed to call RegisterInboxAccount"


class DecryptFailure(GenieGraphQLException):
    error_code = "A00008"
    message = "Decrypt Failure!!!"
    error_msg = "Failed to decrypt encrypted message"
