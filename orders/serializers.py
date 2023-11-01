from rest_framework import serializers
from .models import ItemRate, PickupRequestItem
from .models import PickupRequest, OrderItems, Orders, UserTransactionDetails, MyCartItems
from accounts.models import UserModel
from rest_framework import serializers
import random
from .models import ItemRate

class ItemRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemRate
        fields = ['id', 'item_name', 'rate','image_url']

class PickupRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupRequestItem
        fields = '__all__'

class MyCartSerializer(serializers.ModelSerializer):
    items = ItemRateSerializer(source='item_id')
    class Meta:
        model = MyCartItems
        fields = '__all__'

class PickupRequestSerializer(serializers.ModelSerializer):
    items = ItemRateSerializer(many=True, read_only=True)

    class Meta:
        model = PickupRequest
        fields = '__all__'

    def create(self, validated_data):
        pickup_request_items_data = validated_data.pop('pickup_request_items', None)
        # user = self.context['request'].user
        # pickup_request = PickupRequest.objects.create(**validated_data)
        pickup_request = PickupRequest.objects.create(**validated_data)

        
        if pickup_request_items_data:
            for data in pickup_request_items_data:
                PickupRequestItem.objects.create(pickup_request=pickup_request, **data)
        user_id = pickup_request.user_id

        MyCartItems.objects.filter(user_id=user_id).delete()

        return pickup_request

class PickupRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupRequestItem
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        # fields = '__all__'
        exclude = ('order',)

class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    
class OrderRequestItemSerializer(serializers.ModelSerializer):
    pickup_request = PickupRequestSerializer
    user = UserModel

    class Meta:
        model = Orders
        fields = '__all__'
        
class OrdersPickupSerializer(serializers.ModelSerializer):
    order_request_items = OrderItemsSerializer(many=True, required=False)

    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        order_request_items_data = validated_data.pop('order_request_items', None)
        image_proof = self.context['request'].FILES.get('image_proof')
        order_request = Orders.objects.create(image_proof=image_proof,**validated_data)
        
        if order_request_items_data:
            for data in order_request_items_data:
                OrderItems.objects.create(order=order_request, **data)
        
        return order_request

class UserTransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransactionDetails
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    pickup_id = serializers.PrimaryKeyRelatedField(queryset=PickupRequest.objects.all())
    pickup_id__pickuprequestitem_set = PickupRequestItemSerializer(source='pickup_id.pickuprequestitem_set', many=True)

    class Meta:
        model = Orders
        fields = ('__all__')
