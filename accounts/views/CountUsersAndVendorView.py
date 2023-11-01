from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import UserModel
from orders.models import Orders

class CountUsersAndVendor(APIView):
    def get(self, request):
        try:
            vendor_count = UserModel.objects.filter(is_vendor=True).count()
            users_count = UserModel.objects.filter(is_vendor=False).count()
            orders_count = Orders.objects.all().count()
            pickup_count = Orders.objects.filter(order_status='picked').count()
            return Response({'success':True,'pickup_count':pickup_count, 'vendor_count': vendor_count, 'customer_count': users_count, 'orders_count':orders_count},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':False,"error": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
