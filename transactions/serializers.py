from .models import BankDetails, Wallet, WalletHistory , PayContact
from rest_framework import serializers
from accounts.serializers import UserSerializer
from accounts.models import UserModel

class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'
        
class WalletSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())

    class Meta:
        model = Wallet
        fields = '__all__'
    
        
class UserAndWalletSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Wallet
        fields = '__all__'

class WalletHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletHistory
        fields = '__all__'

class PayContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayContact
        fields = '__all__'


class CustomerReportSerializer(serializers.ModelSerializer):
    user_wallet = UserAndWalletSerializer()
    latest_wallet_history = WalletHistorySerializer
    class Meta:
        model = Wallet
        fields = ('user_wallet', 'latest_wallet_history')