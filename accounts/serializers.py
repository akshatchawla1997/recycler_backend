from datetime import timedelta
import random
from django.conf import settings
from rest_framework import serializers
from accounts.email import send_otp_via_email
from .models import UserModel
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer.

    Used in POST and GET
    """
    class Meta:
        model = UserModel
        fields = (
            "id",
            "phone_number",
            "email",
            "name",
            "upiId",
            "pickup_otp"
        )
        read_only_fields = ("id","name","upiId")
 
    def create(self, validated_data):
        """
        Create method.

        Used to create the user
        """
        otp = random.randint(1000, 9999)
        # otp_expiry = datetime.now() + timedelta(minutes = 10)
        otp_expiry = timezone.now() + timedelta(minutes=10)

        user = UserModel(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            otp=otp,
            pickup_otp = random.randint(1000,9999),
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY,
        )
        user.save()
        send_otp_via_email(validated_data["email"], otp)
        return user
 
 
class UserNameUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating the user's name.
    """
    class Meta:
        model = UserModel
        fields = ["name",'email','upiId']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id","phone_number", "email", "pincode", "is_vendor", "password", "name")
        