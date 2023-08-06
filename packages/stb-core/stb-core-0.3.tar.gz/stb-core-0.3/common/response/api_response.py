"""
This module consists of a function that returns the response to the UI
"""
from rest_framework import status
from rest_framework.response import Response


def api_response(msg="", data={}, status_code=status.HTTP_200_OK):
    return Response({"code": status_code, "message": msg, "data": data})
