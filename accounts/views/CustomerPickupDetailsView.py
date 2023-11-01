from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import UserModel
  
class CustomerPickupDetails(APIView):
    def get(self, request, userid):
        try:
            queryset = UserModel.objects.filter(id=userid).select_related(
           'pickuprequest', 'pickuprequest__pickuprequestitem__item_id__itemrate'
).values(
    'name',
    'pickuprequest__pickuprequestitem__weight',
    'pickuprequest__pickuprequestitem__item_id_id',
    'pickuprequest__status',
    'pickuprequest__pickup_date',
    'pickuprequest__pickup_time',
    'pickuprequest__status',
    'pickuprequest__pickuprequestitem__item_id__item_name',
    'pickuprequest__pickuprequestitem__item_id__rate'

    )
            result= queryset.all()
            return Response({'success':True,"data":result})
        except Exception as e:
            return Response({'success':False,'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
