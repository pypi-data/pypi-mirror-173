from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException


class RestAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '400 Bad request'
    default_code = 'NOT FOUND'
    default_errors = []

    def __init__(self, detail, status_code=status.HTTP_400_BAD_REQUEST, code=0, errors=None):
        self.status_code = status_code

        if detail is not None:
            self.detail = {'message': force_text(detail)}
        else:
            self.detail = {'message': force_text(self.default_detail)}

        self.detail['code'] = status_code or self.status_code
        self.detail['errors'] = errors if errors else self.default_errors
