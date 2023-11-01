from django.conf import settings
from rest_framework import status, viewsets
from django.utils import timezone
from ..models import UserModel 
from ..email import send_otp_via_email
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from ..serializers import UserSerializer
from rest_framework.decorators import action
from accounts.backend import PhoneBackend
from django.contrib.auth import login
import datetime
from django.http import JsonResponse
import random

class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    queryset = UserModel.objects.filter(is_vendor=False)
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()
        if (instance.otp == request.data.get("otp")
            and (instance.otp_expiry is not None 
            and timezone.now() < instance.otp_expiry)
                ):
                instance.is_active = True
                instance.otp_expiry = None
                instance.max_otp_try = settings.MAX_OTP_TRY
                instance.otp_max_out = None
                instance.save()
                user, token = PhoneBackend().authenticate(request=request, phone_number=instance.phone_number)
                if user is not None:
                    login(request, user, backend='accounts.backend.PhoneBackend')
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse(
                    { 'success':True, 'token': token.key, 'message': "User logged in"},
                    status=status.HTTP_200_OK
                )
        elif not instance.is_active and instance.otp == request.data.get("otp") and timezone.now() < instance.otp_expiry:
                instance.is_active = True
                instance.otp_expiry = None
                instance.max_otp_try = settings.MAX_OTP_TRY
                instance.otp_max_out = None
                instance.save()
                user, token = PhoneBackend().authenticate(request=request, phone_number=instance.phone_number)
                if user is not None:
                    login(request, user, backend='accounts.backend.PhoneBackend')
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {'success':True,'token': token.key, 'message': "User logged in"},
                    status=status.HTTP_200_OK
                )
        return Response(
             
                {'success':False,"message":"Please enter the correct OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        """
        Regenerate OTP for the given user and send it to the user.
        """
        instance = self.get_object()
        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response(
                {'success':False,"message":"Max OTP try reached, try after an hour"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1
        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try
        if max_otp_try == 0:
            otp_max_out = timezone.now() + datetime.timedelta(hours=1)
            instance.otp_max_out = otp_max_out
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_otp_via_email(instance.email, otp)
        return Response({'success':True,"message":"Successfully generate new OTP."}, status=status.HTTP_200_OK)
