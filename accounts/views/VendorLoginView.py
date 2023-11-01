from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.backend import VendorPhoneBackend
from django.contrib.auth import login
from rest_framework.authtoken.models import Token

class VendorLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        backend = VendorPhoneBackend()
        user, token = backend.authenticate(request, phone_number=phone_number, password=password)

        if user is not None:
            login(request, user, backend='accounts.backend.VendorPhoneBackend')
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                    {'success':True,'token': token.key, 'message': "User logged in",'vendor_id': user.id},
                    status=status.HTTP_200_OK)      
        else:
            return Response(
                {'success':False,"message":"Please enter the correct OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )
      