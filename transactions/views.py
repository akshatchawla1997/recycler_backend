from django.shortcuts import render
import requests
from rest_framework import viewsets
from .serializers import PayContactSerializer,BankDetailsSerializer,WalletSerializer,WalletHistorySerializer, UserAndWalletSerializer, CustomerReportSerializer
from accounts.models import UserModel
from .models import BankDetails,Wallet,WalletHistory, PayContact
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class BankDetailsView(viewsets.ModelViewSet):
    queryset = BankDetails.objects.all()
    serializer_class = BankDetailsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED)

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class UserAndWalletView(APIView):
    def get(self, request, format=None):
        wallets = Wallet.objects.all()
        serializer = UserAndWalletSerializer(wallets, many=True)
        return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)

class WalletDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

class WalletHistoryViewSet(viewsets.ModelViewSet):
    queryset = WalletHistory.objects.all()
    serializer_class = WalletHistorySerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        # Update the wallet balance based on transaction_type
        if instance.transaction_type == "dr":  # Deduct amount from wallet balance
            instance.wallet.wallet_amount -= instance.transaction_amount
        elif instance.transaction_type == "cr":  # Add amount to wallet balance
            instance.wallet.wallet_amount += instance.transaction_amount

        instance.wallet.save()

        return Response({"success":True,"data":serializer.data}, status=status.HTTP_201_CREATED)
    
    
    @action(detail=False, methods=['GET'])
    def get_history_by_wallet_id(self, request):
        wallet_id = request.query_params.get('wallet_id')
        if not wallet_id:
            return Response({"success":False,"error": "Please provide a valid 'wallet_id' parameter in the query string."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            wallet_history = WalletHistory.objects.filter(wallet=wallet_id)
            serializer = self.get_serializer(wallet_history, many=True)
            return Response({"success":True,"data":serializer.data}, status=status.HTTP_200_OK)
        except Wallet.DoesNotExist:
            return Response({"success":False,"error": "Wallet not found."}, status=status.HTTP_404_NOT_FOUND)
        
class PayContactView(viewsets.ModelViewSet):
    queryset = PayContact.objects.all()
    serializer_class = PayContactSerializer
    def create(self, request, *args, **kwargs):
        request.data['type'] = 'customer'
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        razorpay_response = self.create_razorpay_contact(request.data['name'], request.data['email'], request.data['contact'], request.data['type'])
        instance = serializer.instance
        instance.refrence_id = razorpay_response.get('id');
        instance.save()
        return Response({"success":True,"data":serializer.data}, status=201, headers=headers)
    
    def create_razorpay_contact(self, name, email, contact_number, contact_type):
        API_KEY = ""
        url = 'https://api.razorpay.com/v1/contacts'
        headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
        }
        data = {
            'name': name,
            'email': email,
            'contact': contact_number,
            'type': contact_type
    }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    # def update_pay_Contact(self,refrence_id):
class CustomerReportView(APIView):
    def get(self, request):
        combined_data = []
        # Assuming UserAndWallet and WalletHistory models exist
        user_wallets = Wallet.objects.all()

        for user_wallet in user_wallets:
            latest_history = WalletHistory.objects.filter(wallet=user_wallet.id).latest('wallet_updated')
            combined_serializer = CustomerReportSerializer({
                'user_wallet': user_wallet,
                'latest_wallet_history': latest_history
            })
            combined_data.append(combined_serializer.data)

        return Response({"success":True,"data":combined_data})
