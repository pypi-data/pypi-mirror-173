import random
import uuid

import environ
import requests
from django.utils import timezone

from apps.common.models.otp import OtpData

from .mailer import send_mail_asyn,order_email_to_user
from .sms import send_sms

ENV = environ.Env()
sms_key = ENV("SMS_CLIENT_KEY")


def generate_otp():
    # order_email_to_user()
    otp = random.randint(100000, 999999)
    return otp


def is_otp_expired(created_time):
    current_time = timezone.now()
    time_difference = (current_time - created_time).seconds
    if time_difference > int(ENV('OTP_EXPIRY_TIME')):
        # if token expired
        return True
    else:
        return False


def send_otp(reciever, send_type='email', otp=generate_otp(), resend=False, session_token=None):
    """
        Sent the OTP to users
    """
    try:
        if send_type == 'mobile':
            try:
                response = send_sms(reciever, otp)
                if not response.get("status") == "Success":
                    return {"session_token": "", "status": "Fail"}
            except Exception as e:
                print('otp could not be send due to ', e)
                return {"session_token": "", "status": "Fail", "reason": str(e)}
        elif send_type == 'email':
            send_mail_asyn("OTP", f"{otp} is your otp for verification", [reciever])
        else:
            data = {"status":False,"reason":"send type is not valid"}
            return data

        if not resend:
            session_token = uuid.uuid4()
            OtpData.objects.create(session_token=session_token, otp_no=otp,
                            to=reciever, time=timezone.now(), otp_count_today=1)
        return {"session_token": session_token, "status":True}
    except Exception as e:
        data = {"status":False,"reason":str(e)}
        return data


def resend_otp(reciever, session_token, send_type='email'):
    """
        Resend OTP to users 
    """

    # fetch otp from database with mobile no and session token and sent again
    try:
        otp_obj = OtpData.objects.get(session_token=session_token)
        # check if token is expired
        if is_otp_expired(otp_obj.time):
            # if token expired
            response = send_otp(reciever, send_type)
        else:
            response = send_otp(reciever, send_type, otp_obj.otp_no,
                                resend=True, session_token=session_token)

    except Exception as e:
        return {"session_token": "", "status": "Fail", "reason": str(e)}
    return response


def verify_otp_func(session_token, otp):
    """
        Verify the OTP entered by users
    """

    try:
        otp_obj = OtpData.objects.get(session_token=session_token,otp_no=otp)
        if is_otp_expired(otp_obj.time):
            print('otp Expired')
            data = {"status":False,"reason":"OTP expired"}
            return data
        else:
            print("otp_match")
            data = {"status":True,"reason":"OTP matched"}
            return data
        
    except Exception as e:
        print('OTP fetch fail due to ', e)
        data = {"status":False,"message":"OTP verification Failed","reason":str(e)}
        return data
