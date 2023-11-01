import datetime
import random
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.email import send_otp_via_email
from ..models import UserModel

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = UserModel.objects.get(email=email, is_active=1)
        except UserModel.DoesNotExist:
            return Response({'success':False,"message":"User does not exist.","status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        user.otp = otp
        user.otp_expiry = otp_expiry
        user.save()
        send_otp_via_email(email, otp)
        return Response({'success':True,"data":{"id": user.id,"message":"OTP sent to user."},"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
  