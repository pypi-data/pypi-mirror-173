from django.http import JsonResponse
from rest_framework import status
from apps.common.utils.exceptions import RestAPIException
from rest_framework.authentication import get_authorization_header
from apps.custom_auth.decode import decode_auth_token
import json


def custom_user_authenticate(*args, **kwargs):
    ''' Authenticate customer user '''

    def inner(request, *inner_args, **inner_kwargs):
        try:
            # user_id = json.loads(verify_token_format(request))
            user_id = verify_token_format(request)
            # setattr(request, 'email', user["email"])
            setattr(request, 'customer_id', user_id)
        except RestAPIException as e:
            # Convert the RestAPIException response to JSON response
            return JsonResponse(e.__dict__['detail'], status=status.HTTP_401_UNAUTHORIZED)
        # Proceed with the url call
        return args[0](request, *inner_args, **inner_kwargs)
    return inner



def verify_token_format(request):
    """ Check Token from Header """
    # auth = get_authorization_header(request).split()
    auth = get_authorization_header(request).split()

    # if not auth or auth[0].lower() != b'bearer':
    #     msg = 'Invalid token header. No credentials provided.'
    #     # Status code for un-authorized token should be 401 (Un-Authorized)
    #     raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)

    # if len(auth) == 1:
    #     msg = 'Invalid token header. No token credentials provided.'
    #     raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)
    # elif len(auth) > 2:
    #     msg = 'Invalid token header'
    #     raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)
    if not auth:
        msg = 'Invalid token header. No credentials provided.'
        # Status code for un-authorized token should be 401 (Un-Authorized)
        raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)

    try:
        token = auth[0]
        if not token or token == "null":
            msg = 'Null token not allowed'
            raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)
    except UnicodeError:
        msg = 'Invalid token header. Token string should not contain invalid characters.'
        raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        msg = str(e)
        raise RestAPIException(msg, status_code=status.HTTP_401_UNAUTHORIZED)
    
    
    if isinstance(token, bytes):
        token = token.decode('UTF-8')
    # return decode_auth_token(token)
    return token

