from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models import UserModel 
from ..serializers import VendorSerializer
  
class VendorSignupView(viewsets.ModelViewSet):
    queryset = UserModel.objects.filter(is_vendor=True)
    serializer_class = VendorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vendor = self.perform_create(serializer)
        
        return Response({'message': 'Vendor signed up successfully'}, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        password = make_password(serializer.validated_data.get('password'))
        return serializer.save(password=password)
 