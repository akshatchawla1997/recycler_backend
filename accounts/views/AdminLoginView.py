from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.backend import AdminPhoneBackend

class AdminLoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        user, token = AdminPhoneBackend().authenticate(request=request, phone_number=phone_number, password=password)
        if user:
            if user.is_authenticated:
                # Successful login
                return Response({'success':True,"message": "Admin successfully logged in", "token": token.key}, status=status.HTTP_200_OK)
            else:
                # User is not a superuser
                return Response({'success':False,"message": "You are not authorized to access this resource"}, status=status.HTTP_403_FORBIDDEN)
        else:
            # Invalid credentials
            return Response({'success':False,"message": "Invalid phone number or password"}, status=status.HTTP_400_BAD_REQUEST)
