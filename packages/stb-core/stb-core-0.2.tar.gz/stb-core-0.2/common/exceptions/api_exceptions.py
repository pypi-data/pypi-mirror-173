"""
This module consists of a class that contains generic methods for API exceptions
"""
from rest_framework import status
from rest_framework.serializers import Serializer

from apps.common.utils.exceptions import RestAPIException


class APIExceptionMixin:
    """ Class that contains generic methods for API exceptions """

    def is_valid_request_params(self, serializer_obj, msg="Invalid request params", status_code=status.HTTP_400_BAD_REQUEST):
        """ Raises a rest API exception for invalid request params """

        if not isinstance(serializer_obj, Serializer):
            raise RestAPIException("Please provide a valid serializer instance")

        if not serializer_obj.is_valid():
            raise RestAPIException(msg, errors=serializer_obj.errors, status_code=status_code)
