from allauth.socialaccount.models import SocialAccount, SocialApp
from django.conf import settings
from django.contrib.sites.models import Site
from rest_framework import response

from common.models import *


# create a super users
def create_seed_super_user():
    try:
        # TODO can create super user in for loop for all admin email present in settings
        user = CustomUser.objects.create(email="strivebit.tech@gmail.com",is_staff=True,is_superuser=True)
        user.set_password('Password1a')
        user.save()
        print('Superuser created successfully')
        response = {"process":"Creating superuser","status":True}
        return response
    except Exception as e:
        # TODO add logger here
        print('Error while creating superuser',str(e))
        response = {"process":"Creating superuser","status":False,"reason":f'Super user creation Failed'+str(e)}
        return response


# create a super users
def create_shop_related_data():
    try:
        category = Category.objects.create(name="cloth",slug="cloths")
        address = Address.objects.create(houseFlatNumber="kr tower",street="gali no 3",area="chalera",city="noida",country="india",pin=123456,primary=True)
        plan = ShopPlan.objects.create(name='basic',duration=6,amount=100)
        template = Template.objects.create(name='basic',theme=[{"color":"red"}])
        Shop.objects.create(name='storely',description='storely description',slug='storely',category=category,address=address,plan=plan,template=template)
        response = {"process":"Creating shop seed data","status":True}
        print('Shop data created successfully')
        return response
    except Exception as e:
        # TODO add logger here
        print('Error while creating shop data',str(e))
        response = {"process":"Creating shop seed data","status":False,"reason":f'Shop data creation Failed'+str(e)}
        return response


def set_google_client_id():
    try:
        # update site 
        site_obj = Site.objects.get(id=1)
        site_obj.domain = settings.ENV('HOST_URL')
        site_obj.name = settings.ENV('HOST_URL')
        site_obj.save()
        # fetch secrets from env
        client_id = settings.ENV('GOOGLE_API_CLIENT_ID')
        client_secret = settings.ENV('GOOGLE_API_SECRET')
        # create a social application entry for google
        if SocialApp.objects.all():
            response = {"process":"Entering google client secrets","status":False,"reason":'Application entry already exist'}
            return response
        sapp = SocialApp(provider='google', name='Google', 
            client_id=client_id,
            secret=client_secret)

        sapp.save()
        sapp.sites.add(1)
        response = {"process":"Entering google client secrets","status":True}
        print('Google client data created successfully')
        return response
    except Exception as e:
        print('Error while creating google credential data',str(e))
        response = {"process":"Entering google client secrets","status":False,"reason":f'Super user creation Failed'+str(e)}
        return response



def create_seed_data_func():
    superuser_creation = create_seed_super_user()
    client_id_set = set_google_client_id()
    shop_data = create_shop_related_data()
    if superuser_creation.get('status') and shop_data.get('status') and client_id_set.get('status'):
        response = {"status":True,"responses":[superuser_creation,client_id_set,shop_data]}
    else:
        response = {"status":False,"responses":[superuser_creation,client_id_set,shop_data]}
    return response
    