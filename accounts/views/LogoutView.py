from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

class LogoutAPIView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if token:
            try:
                token_obj = Token.objects.get(key=token)                
                token_obj.delete()
                return Response({'success':True,'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':False,'detail': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)
    