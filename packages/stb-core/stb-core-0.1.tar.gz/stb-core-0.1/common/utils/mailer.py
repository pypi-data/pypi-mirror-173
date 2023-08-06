import threading

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from apps.custom_auth.encode import encode_auth_token


def send_mail_asyn(subject, message, receiver, sender=settings.EMAIL_HOST_USER, html_message=None):
    """ Send mail to receiver in thread """

    threading.Thread(target=mail, args=(subject, sender, receiver, html_message, message)).start()
    return


def mail(subject, from_email, recipient_list, html_message, message):
    """ Sends a mail to email using inbuilt send_mail method """
    send_mail(
        subject = subject,
        message = message,
        from_email = from_email,
        recipient_list = recipient_list,
        html_message = html_message
    )


def send_reset_password_mail(user, subject, template_name=None):
    """ Sends an email to the user along with their token """

    # generate a token from payload of expiry same as of login token
    payload = {"email" : user.email}
    token = encode_auth_token(payload, "login")

    # check if the encoded token is instance of str or bytes
    if isinstance(token, str):
        frontend_endpoint = settings.ENV('FRONTEND_RESET_PASSWORD_ROUTE') + '?' + token
    elif isinstance(token, bytes):
        frontend_endpoint = settings.ENV('FRONTEND_RESET_PASSWORD_ROUTE') + '?' + token.decode('UTF-8')

    # convert the html template with context data into string
    html_message = render_to_string(template_name, {'first_name': user.first_name, 'url': frontend_endpoint})
    # send the mail to the user with the html message
    send_mail_asyn(subject, "Sent from Django", [user.email], html_message=html_message)


def order_email_to_user( template_name='order_success_user.html'):
    """ Sends an email to the user along with their token """

    # generate a token from payload of expiry same as of login token

    # convert the html template with context data into string
    html_message = render_to_string(template_name, {'first_name': 'Kartik'})
    # send the mail to the user with the html message
    print('mail send for order successful')
    send_mail_asyn('Order Successful', "Order Successful", ['kartik123choudhary@gmail.com'], html_message=html_message)


def order_email_to_admin(user, subject, template_name=None):
    """ Sends an email to the user along with their token """


    # convert the html template with context data into string
    html_message = render_to_string(template_name, {'first_name': user.first_name})
    # send the mail to the user with the html message
    send_mail_asyn(subject, "Sent from Django", [user.email], html_message=html_message)
