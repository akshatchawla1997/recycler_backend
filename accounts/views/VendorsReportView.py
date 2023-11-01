from django.conf import settings
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import UserModel 

class VendorReportView(APIView):
    def get(self, request):
        # Get all vendors
        vendors = UserModel.objects.filter(is_vendor=True)
        # Annotate the order count for each vendor
        annotated_vendors = vendors.annotate(order_count=Count('orders__vendor_id_id'))
        # Serialize the annotated vendors with order counts
        serialized_annotated_vendors = [
            {
                'vendor_id': vendor.id,
                'vendor_name': vendor.name,
                'vendor_email':vendor.email,
                'vendor_phone_number':vendor.phone_number,
                'vendor_area':vendor.pincode,
                'order_count': vendor.order_count
            }
            for vendor in annotated_vendors
        ]
        return Response({'success':True,
            'vendor_orders_count': serialized_annotated_vendors,
        }, status=status.HTTP_200_OK)

