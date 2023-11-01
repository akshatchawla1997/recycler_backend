# from .models import UserModel
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from .models import UserModel

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, username=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
            token, created = Token.objects.get_or_create(user=user)
            return user, token
        except User.DoesNotExist:
            return None
        
class AdminPhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, username=None, password=None):
        User = get_user_model()
        try:

            if phone_number and password:

                user = User.objects.get(phone_number=phone_number)
                if check_password(password, user.password):
                    token, created = Token.objects.get_or_create(user=user)
                    return user, token       
            return None
        except User.DoesNotExist:
            pass
        
class VendorPhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        User = get_user_model()
        try:
            if phone_number and password:
                user = User.objects.get(phone_number=phone_number, is_vendor=True)
                if check_password(password, user.password):
                    token, _ = Token.objects.get_or_create(user=user)
                    return user, token
        except User.DoesNotExist:
            pass  

        return None, None  

