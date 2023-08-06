# from django.core.mail import send_mail
import random
import uuid

import environ
import requests
from django.utils import timezone

# from storely_backend.settings import EMAIL_HOST_USER
# from storely.models import *
# from storely_backend.responses import error_response, success_response

ENV = environ.Env()
sms_key = ENV("SMS_CLIENT_KEY")


def send_sms(mobile, text):
    """
        Sent the OTP to users
    """
    try:
        url = f'https://2factor.in/API/V1/{sms_key}/SMS/+91{mobile}/{text}'
        response = requests.get(url)
        if response.json()["Status"] == "Success":
            return {"status": "Success"}
        else:
            return {"session_token": "", "status": "Fail"}
    except Exception as e:
        print('otp could not be send due to ', e)
        return {"session_token": "", "status": "Fail", "reason": str(e)}