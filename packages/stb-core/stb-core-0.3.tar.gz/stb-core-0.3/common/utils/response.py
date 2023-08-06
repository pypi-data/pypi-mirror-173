from rest_framework import status


class CustomAPIResponse:
    """ Returns a custom response object for UI """

    def __init__(self, message:str, errors=None, code=status.HTTP_200_OK) -> None:
        """ Initialise a constructor """
        self.message = message
        self.errors  = errors
        self.code    = code


    def get_response_dict(self):
        """ Returns a dict of response """

        return {
            "message": self.message,
            "code"   : self.code,
            "errors" : self.errors
        }
