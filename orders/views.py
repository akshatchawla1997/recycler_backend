from rest_framework import viewsets
from .models import ItemRate, PickupRequest,Orders,OrderItems, PickupRequestItem,UserTransactionDetails, MyCartItems
from .serializers import ItemRateSerializer, PickupRequestSerializer, OrdersPickupSerializer, MyCartSerializer, UserTransactionDetailsSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserModel
from django.db.models import F
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.db.models import F
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework import generics

class ItemRateViewSet(viewsets.ModelViewSet):
    queryset = ItemRate.objects.all()
    serializer_class = ItemRateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "success": True,  # Customize this based on your logic
            "data": serializer.data,
            "message": "Scrap rate found successfully",  # Customize the message as needed
        }
        return JsonResponse(response_data)
        
class AddToCartView(viewsets.ModelViewSet):
    queryset = MyCartItems.objects.all()
    serializer_class = MyCartSerializer

    def create(self, request, *args, **kwargs):
        user = request.data.get('user_id', None)
        cart_items = request.data.get('cart_items', [])

        if user is None:
            return Response({"success": False, 'user_id': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)

        if not cart_items:
            return Response({"success": False, 'cart_items': 'No items provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # List to store added cart items
        added_items = []

        # Add cart items
        for cart_item_data in cart_items:
            item_id = cart_item_data.get('item_id')
            weight = cart_item_data.get('weight')

            # You can perform additional validation here as needed

            # Create a new cart item
            added_item = MyCartItems.objects.create(user_id=user, item_id_id=item_id, weight=weight)
            added_items.append(added_item)

        # Serialize the added items
        serializer = MyCartSerializer(added_items, many=True)

        return Response({"success": True, "data": serializer.data, 'message': 'Items added to the cart successfully.'}, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        try:
            cart_items = MyCartItems.objects.filter(user_id=user_id)
            serializer = MyCartSerializer(cart_items, many=True)
            if cart_items.count()==0:
                return Response({"success": False, "data": serializer.data}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        except MyCartItems.DoesNotExist:
            return Response({"success": False, "data": None}, status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        # Your update logic here
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Customize the response format
        updated_items = MyCartItems.objects.filter(user_id=instance.user_id)
        updated_serializer = MyCartSerializer(updated_items, many=True)

        return Response({
            "success": True,
            "data": updated_serializer.data,
            "message": "Items updated to the cart successfully."
        }, status=status.HTTP_200_OK)

class CreateAndUpdateCartView(APIView):
    def post(self, request, *args, **kwargs):
        body_data = request.data
        user_id = body_data.get('user')
        cart_items = body_data.get('cart_items')
        item_id = cart_items.get('item_id')
        weight = cart_items.get('weight')

        try:
            # Check if an entry with the same user and item_id exists
            cart_item = MyCartItems.objects.get(user=user_id, item_id=item_id)
            cart_item.weight = weight
            cart_item.save()
        except MyCartItems.DoesNotExist:
            # If the entry does not exist, create a new one
            MyCartItems.objects.create(user_id=user_id, item_id_id=item_id, weight=weight)
            
        
        # Check if weight is 0 and delete the entry if it exists
        if weight == 0:
            try:
                cart_item = MyCartItems.objects.get(user=user_id, item_id=item_id)
                cart_item.delete()
            except MyCartItems.DoesNotExist:
                pass  # Entry doesn't exist, nothing to delete
        
        return JsonResponse({"success":True, "message":"cart updated successfully"},status=status.HTTP_200_OK)

class PickupRequestViewSet(viewsets.ModelViewSet):
    queryset = PickupRequest.objects.all()
    serializer_class = PickupRequestSerializer
 
    def create(self, request, *args, **kwargs):
            user_id = request.data.get('user')  # Retrieve the user_id from request.data
            serializer = self.get_serializer(data=request.data)
            items_data = request.data.pop('pickup_request_items', [])
            serializer.is_valid(raise_exception=True)
            
            serializer.save(user_id=user_id)  # Pass user_id as an argument to the save method
            for item_data in items_data:
                item_id = item_data.get('item_id')
                weight = item_data.get('weight')
                
                # Create PickupRequestItem and associate it with the PickupRequest
                pickup_request = serializer.instance
                # print(pickup_request)
                PickupRequestItem.objects.create(
                    pickup_request=pickup_request,
                    item_id_id=item_id,
                    weight=weight
                )
            headers = self.get_success_headers(serializer.data) 
            return JsonResponse({"success":True, "message":"Pickup request generated successfully"}, status=201)
        
    def get_queryset(self):
        user_id = self.kwargs.get('user')  
        pickup_data = PickupRequest.objects.filter(user=user_id)

        modified_pickup_data = []

        for pickup in pickup_data:
            # Check if the PickupRequest status is "completed"
            if pickup.status == "completed":
                # Get related orders with status "completed"
                completed_orders = Orders.objects.filter(pickup_id=pickup)
                
                # print(completed_orders)
                # Extract the order_status values from completed orders
                order_statuses = [order.order_status for order in completed_orders]
                # print(order_statuses)
                # Add the extracted order_status values to the pickup object
                pickup.status = order_statuses[0]

            modified_pickup_data.append(pickup)

        return modified_pickup_data

class VerifyPickupOTPView(APIView):
    def get_pickup_otp_for_order(self, order_id):
        try:
            order = Orders.objects.select_related('pickup_id__user').get(id=order_id)
            pickup_otp = order.pickup_id.user.pickup_otp
            return pickup_otp
        except Orders.DoesNotExist:
            return None

    def patch(self, request, order_id):
        pickup_otp = self.get_pickup_otp_for_order(order_id)
        
        otp = request.data.get('otp') 

        if otp == pickup_otp:
            return Response({'success':True,'detail': 'OTP verification successful'}, status=200)
        else:
            return JsonResponse({'success':False,'detail': 'Invalid OTP'}, status=400)
  
class PickupRequestItemView(APIView):
    def merge_order_data(self, pickup_data, order_data):
        merged_data = []

        # Create a dictionary to store order data for easier lookup
        order_lookup = {order["pickup_id_id"]: order for order in order_data}

        for pickup in pickup_data:
            pickup_id = pickup["id"]
            order = order_lookup.get(pickup_id)

            # If there is no matching order data for this pickup, set default values
            if not order:
                pickup["orderitems__quantity"] = None
                pickup["orderitems__item_id__item_name"] = None
                pickup["order_status"] = None
                pickup["total_amount"] = None
                pickup["order_created_at"] = None
            else:
                pickup["orderitems__quantity"] = order.get("orderitems__quantity")
                pickup["orderitems__item_id__item_name"] = order.get("orderitems__item_id__item_name")
                pickup["order_status"] = order.get("order_status")
                pickup["total_amount"] = order.get("total_amount")
                pickup["order_created_at"] = order.get("created_at")
                pickup["order_id"] = order.get("order_id")
            merged_data.append(pickup)

        return merged_data


    def get(self, request):
        try:

            pickup_data = PickupRequest.objects.select_related(
    'user',
    'pickuprequestitem__item_id'
).values(
    'id',
    'user_id',
    'user__name',
    'user__upiId',
    'pickup_date',
    'pickup_time',
    'status',
    'created_at',
    'pickuprequestitem__weight',
    'pickuprequestitem__item_id__item_name',
)
            pickup_instance = pickup_data.all()
            pickup_ids = [item['id'] for item in pickup_data]

            # query 2 data
            order_data = Orders.objects.select_related(
            'orderitems',
            'orderitems__item_id'
        ).annotate(order_id=F('id')).values(
            'order_id',
            'order_status',
            'pickup_id_id',
            'total_amount',
            'orderitems__quantity',
            'orderitems__item_id__item_name',
            'created_at'
        ).filter(pickup_id_id__in=pickup_ids)
            order_instance = order_data.all()
            merged_data = self.merge_order_data(pickup_instance, order_instance)
            return Response({'success':True,"data":merged_data})
        except Exception as e:
            return Response({'success':False,'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderRequestItemView(APIView):
    def get(self, request, vendor_id):
        
        query = Orders.objects.filter(vendor_id_id=vendor_id).values(
            'pickup_id__id',
            'pickup_id__pickup_date', 'pickup_id__pickup_time', 'pickup_id__flat_number',
            'pickup_id__area', 'pickup_id__landmark', 'pickup_id__city', 'pickup_id__state',
            'pickup_id__pincode', 'pickup_id__status', 'pickup_id__user_id', 'pickup_id__user__name',
            'pickup_id__user__phone_number', 'pickup_id__user__email', 'order_status',
            'vendor_id_id', 'id', 'pickup_id__pickuprequestitem__item_id__item_name','pickup_id__pickuprequestitem__weight',
            'pickup_id__pickuprequestitem__item_id__rate', 'pickup_id__pickuprequestitem__item_id_id'
        )

        results = query.all()  # Execute the query and fetch the results

        return  Response({'success':True,"data":results})

class OrderRequestViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersPickupSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({'success':True,"data":serializer.data}, status=status.HTTP_201_CREATED, headers=headers)

class UserPickupViewSet(APIView):
    def get(self, request):
        try:
             queryset = Orders.objects.select_related('pickup_id', 'pickup_id__user').values(
        'pickup_id__user__id',
        'pickup_id__user__name',
        'pickup_id__user__phone_number',
        'pickup_id__user__email',
        'pickup_id__user__upiId',
        'pickup_id__pickup_date',
        'pickup_id__status',
        'pickup_id__area',
        'pickup_id__city',
        'pickup_id__state',
        'pickup_id__pincode',
        'total_amount'
    )
             results = queryset.all()
             return Response({'success':True,"data":results})
             
        except Exception as e:
            return Response({'success':False,'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserTransactionDetailsView(viewsets.ModelViewSet):
     queryset = UserTransactionDetails.objects.all()
     serializer_class = UserTransactionDetailsSerializer

     def create(self, request, *args, **kwargs): 
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'success':True,"data":serializer.data}, status=status.HTTP_201_CREATED)

        
class AppPickupHistoryData(generics.ListAPIView):
    serializer_class = OrderSerializer  # You can use the OrderSerializer or PickupRequestSerializer as needed

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        
        if user_id:
            # Retrieve Orders and PickupRequest instances for the specified user_id
            queryset = Orders.objects.filter(pickup_id__user=user_id)
            return queryset
        else:
            return Orders.objects.none()  # Return an empty queryset if no user_id is provided

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)