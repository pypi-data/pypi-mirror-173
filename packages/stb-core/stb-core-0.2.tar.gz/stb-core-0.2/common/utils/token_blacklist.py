from rest_framework import status

from apps.common.models import TokenBlacklist
from apps.common.utils.exceptions import RestAPIException


def is_token_blacklisted(token):
    # check if the token is blacklisted
    blacklisted_token = TokenBlacklist.objects.filter(token=token).first()
    if blacklisted_token:
        return True
    
    return False
